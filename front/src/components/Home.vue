<template>
  <!-- hero: what the site is, and the two ways to start (search or browse) -->
  <v-img src="/banner.jpg" :alt="$t('home.banner_alt')" cover class="hero" height="min(70vh, 560px)"
    gradient="to right, rgba(10, 25, 15, 0.75) 0%, rgba(10, 25, 15, 0.35) 55%, rgba(10, 25, 15, 0.05) 100%">
    <v-container class="fill-height">
      <div class="hero-content text-white">
        <h1 class="text-h3 text-md-h2 font-weight-light mb-2">{{ $t("title") }}</h1>
        <p class="text-h6 text-md-h5 font-weight-light mb-6">{{ $t("subtitle") }}</p>

        <v-text-field v-model="heroSearch" :label="$t('home.search')" bg-color="surface" variant="solo" flat
          hide-details append-inner-icon="mdi-magnify" class="mb-4" @keydown.enter="searchGallery"
          @click:append-inner="searchGallery"></v-text-field>

        <div class="d-flex flex-wrap align-center ga-4">
          <v-btn to="/birds" color="primary" variant="flat" size="large" append-icon="mdi-arrow-right">
            {{ $t("home.explore") }}
          </v-btn>
          <span v-if="stats" class="text-body-1">
            {{ $t("home.stats", { photos: stats.photos, species: stats.species }) }}
          </span>
        </div>
      </div>
    </v-container>
  </v-img>

  <v-container class="py-10">
    <!-- a few photos, different at each visit -->
    <section v-if="highlights.length > 0" class="mb-12">
      <div class="d-flex align-end justify-space-between flex-wrap ga-2 mb-4">
        <h2 class="text-h5">{{ $t("home.highlights") }}</h2>
        <v-btn to="/birds" variant="text" color="primary" append-icon="mdi-arrow-right">
          {{ $t("home.see_gallery") }}
        </v-btn>
      </div>
      <v-row>
        <v-col v-for="imgId in highlights" :key="imgId" cols="6" sm="4" md="3">
          <BirdTile :img-id="imgId" :name="birdName(imgId)" :latin-name="birdLatinName(imgId)"
            :to="{ path: '/birds', query: { photo: imgId } }"></BirdTile>
        </v-col>
      </v-row>
    </section>

    <!-- entry points by species -->
    <section v-if="speciesCards.length > 0" class="mb-12">
      <h2 class="text-h5 mb-4">{{ $t("home.by_species") }}</h2>
      <v-row>
        <v-col v-for="card in speciesCards" :key="card.species" cols="6" sm="4" md="2">
          <v-card :to="{ path: '/birds', query: { species: card.species } }" class="species-card" rounded="xl">
            <v-img :src="getImageUrl(card.imgId, 320)" :alt="capitalize(card.species)" :aspect-ratio="1" cover
              gradient="to top, rgba(0, 0, 0, 0.65) 0%, rgba(0, 0, 0, 0) 55%">
              <template v-slot:placeholder>
                <div class="species-placeholder fill-height"></div>
              </template>
              <div class="d-flex fill-height align-end pa-3">
                <span class="text-white font-weight-medium">{{ capitalize(card.species) }}</span>
              </div>
            </v-img>
          </v-card>
        </v-col>
      </v-row>
    </section>

    <!-- upcoming functionalities -->
    <section>
      <h2 class="text-h5 mb-4">{{ $t("home.coming") }}</h2>
      <v-row>
        <v-col v-for="feature in comingFeatures" :key="feature.title" cols="12" sm="6">
          <v-card variant="tonal" color="secondary" class="fill-height">
            <v-card-item :prepend-icon="feature.icon">
              <v-card-title>{{ $t(feature.title) }}</v-card-title>
              <template v-slot:append>
                <v-chip size="small" variant="flat" color="secondary">{{ $t("soon") }}</v-chip>
              </template>
            </v-card-item>
            <v-card-text>{{ $t(feature.desc) }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </section>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref, Ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getImages, getImageUrl, getRandomImage } from '@/api/images';
import { useAppStore } from '@/store/app';
import { useImagesStore } from '@/store/images';
import { useSpeciesStore } from '@/store/species';
import BirdTile from '@/components/BirdTile.vue';

const appStore = useAppStore()
const imgStore = useImagesStore()
const speciesStore = useSpeciesStore()
const router = useRouter()

const HIGHLIGHTS_COUNT = 8
const SPECIES_COUNT = 6

const comingFeatures = [
  { title: "navigation.bird_finder.title", desc: "bird_finder.coming_soon.desc", icon: "mdi-magnify-expand" },
  { title: "navigation.quiz.title", desc: "quiz.coming_soon.desc", icon: "mdi-chat-question-outline" },
]

const heroSearch = ref("")
function searchGallery() {
  const q = heroSearch.value.trim()
  router.push({ path: "/birds", query: q ? { q } : {} })
}

const stats: Ref<{ photos: number, species: number } | null> = ref(null)
const highlights: Ref<number[]> = ref([])
const speciesCards: Ref<{ species: string, imgId: number }[]> = ref([])

function shuffle<T>(values: T[]): T[] {
  const result = [...values]
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]]
  }
  return result
}

// random images, without duplicates (there may be fewer images than requested)
async function randomImages(count: number, species: string | null = null): Promise<number[]> {
  const results = await Promise.allSettled(Array.from({ length: count }, () => getRandomImage(species)))
  const ids = results.flatMap(r => r.status == "fulfilled" ? [r.value.data.id as number] : [])
  return [...new Set(ids)]
}

// each section is loaded independently, a failing one is simply not shown
async function load() {
  const locale = appStore.locale
  const species = speciesStore.getSpecies(locale).catch(() => [] as string[])

  getImages(locale, null, null, "", 1, 1).then(async res => {
    stats.value = { photos: res.data.total, species: (await species).length }
  }).catch(() => { stats.value = null })

  // more draws than needed, as the same image may be drawn twice
  randomImages(HIGHLIGHTS_COUNT + 4).then(ids => {
    highlights.value = ids.slice(0, HIGHLIGHTS_COUNT)
    imgStore.fetchImageInfo(ids, locale)
  })

  const picked = shuffle((await species).filter(s => s)).slice(0, SPECIES_COUNT)
  const cards = await Promise.all(picked.map(async s => {
    const ids = await randomImages(1, s).catch(() => [])
    return ids.length > 0 ? { species: s, imgId: ids[0] } : null
  }))
  speciesCards.value = cards.filter((c): c is { species: string, imgId: number } => c !== null)
}

onMounted(load)
watch(() => appStore.locale, load)

function birdName(imgId: number) {
  return capitalize(imgStore.getImageInfo(imgId, appStore.locale)?.bird.name ?? "")
}
function birdLatinName(imgId: number) {
  return imgStore.getImageInfo(imgId, appStore.locale)?.bird.latin_name ?? ""
}
function capitalize(str: string) {
  return str ? str[0].toUpperCase() + str.slice(1) : str
}
</script>

<style scoped>
.hero-content {
  max-width: 560px;
}

.species-card {
  overflow: hidden;
}

.species-placeholder {
  background: rgba(var(--v-theme-on-surface), 0.08);
}
</style>
