<template>
  <v-row class="ma-2" align="center">
    <v-col cols="12" md="">
      <h1 class="text-h5">{{ $t("image_gallery.title") }}</h1>
    </v-col>
    <v-col cols="10" md="3" sm="6">
      <v-text-field v-model="search" class="mt-2" append-inner-icon="mdi-magnify" :label="$t('search')"
        @update:model-value="updateImages(true)" hide-details :density="density" clearable></v-text-field>
    </v-col>
    <v-col cols="2" md="1">
      <v-menu v-model="filterMenu" :close-on-content-click="false" location="end">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon="mdi-filter-menu-outline" variant="outlined" class="mt-3" :size="btnSize"
            :aria-label="$t('a11y.filters')"> </v-btn>
        </template>

        <v-card min-width="300" elevation="1">
          <v-list>
            <v-list-item :title="$t('filter')">
            </v-list-item>
          </v-list>

          <v-divider></v-divider>

          <v-card-text>
            <v-autocomplete v-model="selectedSpecies" clearable :items="species" item-title="value" item-value="key"
              :label="$t('speciesSelect')" @update:model-value="updateSubSpecies()" density="compact">
            </v-autocomplete>
            <v-autocomplete :disabled="subSpecies.length == 0" v-model="selectedSubSpecies" clearable
              :items="subSpecies" item-title="value" item-value="key" :label="$t('subSpeciesSelect')"
              @update:model-value="updateImages()" density="compact">
            </v-autocomplete>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="filterMenu = false">
              {{ $t("close") }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-menu>
    </v-col>
  </v-row>


  <div v-if="imagesIds.length > 0">
    <v-row class="mx-2 mx-sm-4">
      <v-col v-for="i in imagesIds" :key="i" cols="6" sm="4" md="3">
        <v-card class="bird-tile" @click="showCarousel(i)">
          <v-img :src="getImageUrl(i)" :alt="getImgBirdName(i) || $t('a11y.bird_photo')" :aspect-ratio="4 / 3" cover
            rounded="xl"></v-img>
          <div class="pa-2">
            <div class="text-body-2 text-sm-subtitle-1 font-weight-medium text-truncate">
              {{ getImgBirdName(i) || "\u00a0" }}
            </div>
            <div class="text-caption font-italic text-medium-emphasis text-truncate">
              {{ getImgBirdLatinName(i) || "\u00a0" }}
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-pagination class="mb-5 mt-2" v-model="page" :length="totalPages" rounded="circle"
      @update:model-value="updateImages()"></v-pagination>
  </div>




  <v-container v-else>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card class="d-flex align-center justify-center text-center" height="300px">
          <v-row align="center" justify="center">
            <v-col cols="12">
              <v-card-title class="text-h5 text-wrap">{{ $t("image_gallery.no_match.title") }}</v-card-title>
              <v-card-text class="text-subtitle-1">{{ $t("image_gallery.no_match.desc") }}</v-card-text>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <v-dialog v-model="carouselVisible" width="600px">
    <v-card class="pa-4 text-center">
      <v-btn icon class="close-button" @click="closeCarousel" variant="flat" size="small"
        :aria-label="$t('a11y.close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-img :src="getImageUrl(carouselIndex)" :alt="getImgBirdName(carouselIndex) || $t('a11y.bird_photo')" contain
        max-height="500px" rounded="xl"></v-img>
      <v-card-title>
        {{ getImgBirdName(carouselIndex) }}
      </v-card-title>
      <v-card-text class="pt-0">
        <span class="text-subtitle-2 font-italic"> {{ getImgBirdLatinName(carouselIndex) }}</span>
      </v-card-text>
      <v-card-subtitle>
        <a :href="getImgAuthorLink(carouselIndex)" target="_blank" rel="noopener">{{ getImgAuthorName(carouselIndex) }}</a>
        |
        <a :href="getImgCopyrightLink(carouselIndex)" target="_blank" rel="noopener">{{ getImgCopyrightName(carouselIndex) }}</a>
      </v-card-subtitle>
    </v-card>
  </v-dialog>

</template>

<script setup lang="ts">
import { onMounted, ref, watch, Ref } from 'vue';
import { getImageUrl, getImages } from '@/api/images';
import { useAppStore } from '@/store/app';
import { useImagesStore } from '@/store/images'
import { useSpeciesStore } from '@/store/species'
import { computed } from 'vue';
import { useDisplay } from 'vuetify'

const appStore = useAppStore()
const imgStore = useImagesStore()
const speciesStore = useSpeciesStore()

const carouselVisible = ref(false)
const carouselIndex = ref(0)
function showCarousel(imgIndex: number) {
  carouselIndex.value = imgIndex
  carouselVisible.value = true
}
function closeCarousel() {
  carouselVisible.value = false
}

const selectedSpecies: Ref<string | null> = ref(null)
const selectedSubSpecies: Ref<string | null> = ref(null)
const search: Ref<string> = ref("")

const page = ref(1)
const perPage = 12
const total = ref(1)
const totalPages = computed(() => {
  let res = Math.floor(total.value / perPage)
  if (total.value % perPage > 0) {
    res += 1
  }
  return res
})

const imagesIds = ref([])
onMounted(async () => {
  page.value = 1

  await updateImages()

  let spcs = await speciesStore.getSpecies(appStore.locale)
  species.value = spcs.map(s => ({ key: s, value: capitalizeFirstLetter(s) }))
})

async function updateSubSpecies() {
  selectedSubSpecies.value = null
  subSpecies.value = []
  if (selectedSpecies.value != null) {
    let spcs = await speciesStore.getSubSpecies(appStore.locale, selectedSpecies.value)
    subSpecies.value = spcs.map(s => ({ key: s, value: capitalizeFirstLetter(s) }))
  }
  await updateImages()
}

async function updateImages(resetPages = false) {
  if (resetPages) {
    page.value = 1
  }
  window.scrollTo(0, 0)
  const res = await getImages(appStore.locale, selectedSpecies.value, selectedSubSpecies.value, search.value, page.value, perPage)
  imagesIds.value = res.data.items
  await imgStore.fetchImageInfo(imagesIds.value, appStore.locale)
  total.value = res.data.total
}
// the information of an image may not be loaded yet
function getImgBirdName(imgId: number) {
  const birdInfo = imgStore.getImageInfo(imgId, appStore.locale)
  return birdInfo ? capitalizeFirstLetter(birdInfo.bird.name) : ""
}
function getImgBirdLatinName(imgId: number) {
  const birdInfo = imgStore.getImageInfo(imgId, appStore.locale)
  return birdInfo?.bird.latin_name
}
function getImgCopyrightName(imgId: number) {
  const birdInfo = imgStore.getImageInfo(imgId, appStore.locale)
  return birdInfo?.license.short_name
}
function getImgCopyrightLink(imgId: number) {
  const birdInfo = imgStore.getImageInfo(imgId, appStore.locale)
  return birdInfo?.license.link
}
function getImgAuthorName(imgId: number) {
  const birdInfo = imgStore.getImageInfo(imgId, appStore.locale)
  return birdInfo?.author.name
}
function getImgAuthorLink(imgId: number) {
  const birdInfo = imgStore.getImageInfo(imgId, appStore.locale)
  return birdInfo?.author.link
}

const locale = computed(() => {
  return appStore.locale
})
watch(locale, async (newLocale: string, oldLocale: string) => {
  if (newLocale != oldLocale) {
    page.value = 1
    await updateImages()
    let spcs = await speciesStore.getSpecies(appStore.locale)
    species.value = spcs.map(s => ({ key: s, value: capitalizeFirstLetter(s) }))
  }
})

const species: Ref<{ key: string, value: string }[]> = ref([])
const subSpecies: Ref<{ key: string, value: string }[]> = ref([])


const filterMenu = ref(false)

const { name } = useDisplay()
const density = computed(() => {
  switch (name.value) {
    case 'xs': return "compact"
    default: return "default"
  }
})
const btnSize = computed(() => {
  switch (name.value) {
    case 'xs': return "x-small"
    default: return undefined
  }
})

function capitalizeFirstLetter(str: string): string {
  return str ? str[0].toUpperCase() + str.slice(1) : str;
}
</script>

<style scoped>
.position-relative {
  position: relative;
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 1;
}

.capitalize {
  text-transform: capitalize;
}

.bird-tile {
  background: transparent;
}
</style>