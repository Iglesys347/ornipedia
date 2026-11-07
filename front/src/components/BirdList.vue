<template>
  <div class="px-2 px-sm-4 pt-2">
    <h1 class="text-h5 px-3 pt-3 pb-1">{{ $t("image_gallery.title") }}</h1>

    <v-row class="ma-0" align="center">
      <v-col :cols="smallScreen ? undefined : 12" md="4">
        <v-text-field v-model="searchInput" append-inner-icon="mdi-magnify" :label="$t('search')" hide-details
          :density="density" clearable @update:model-value="onSearchInput"></v-text-field>
      </v-col>

      <!-- desktop: filters next to the search field -->
      <v-col v-if="!smallScreen" cols="12" md="8">
        <GroupFilters :groups="groups" :subgroups="subgroups" :selected-group="selectedGroup"
          :selected-subgroup="selectedSubgroup" :density="density" @update:group="selectGroup"
          @update:subgroup="selectSubgroup"></GroupFilters>
      </v-col>

      <!-- mobile: a button opening the filters at the bottom of the screen -->
      <v-col v-else cols="auto">
        <v-badge :model-value="activeFiltersCount > 0" :content="activeFiltersCount" color="primary">
          <v-btn icon="mdi-filter-variant" variant="outlined" :aria-label="$t('image_gallery.filters')"
            @click="filtersSheet = true"></v-btn>
        </v-badge>
      </v-col>
    </v-row>

    <v-bottom-sheet v-model="filtersSheet">
      <v-card :title="$t('image_gallery.filters')">
        <v-card-text>
          <GroupFilters :groups="groups" :subgroups="subgroups" :selected-group="selectedGroup"
            :selected-subgroup="selectedSubgroup" stacked @update:group="selectGroup"
            @update:subgroup="selectSubgroup"></GroupFilters>
        </v-card-text>
        <v-card-actions class="px-4 pb-4">
          <v-btn v-if="activeFiltersCount > 0" variant="text" @click="clearGroupFilters">
            {{ $t("image_gallery.clear_filters") }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn variant="flat" color="primary" :loading="loading" @click="filtersSheet = false">
            {{ $t("image_gallery.show_results", total) }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-bottom-sheet>

    <!-- active filters, whatever the number of groups -->
    <div v-if="activeFiltersCount > 0" class="d-flex flex-wrap ga-2 px-3 pt-1">
      <v-chip v-if="selectedGroup" closable size="small" color="primary" variant="tonal"
        :close-label="$t('image_gallery.remove_filter')" @click:close="selectGroup(null)">
        {{ $t("image_gallery.group_chip", { name: capitalizeFirstLetter(selectedGroup) }) }}
      </v-chip>
      <v-chip v-if="selectedSubgroup" closable size="small" color="primary" variant="tonal"
        :close-label="$t('image_gallery.remove_filter')" @click:close="selectSubgroup(null)">
        {{ $t("image_gallery.subgroup_chip", { name: capitalizeFirstLetter(selectedSubgroup) }) }}
      </v-chip>
    </div>

    <div class="d-flex align-center flex-wrap px-3 py-1 results-bar">
      <span class="text-body-2 text-medium-emphasis" aria-live="polite">
        <template v-if="!loadError && (!loading || imagesIds.length > 0)">
          {{ $t("image_gallery.count", total) }}
        </template>
      </span>
      <v-btn v-if="hasFilters" class="ms-2" variant="text" size="small" prepend-icon="mdi-filter-remove-outline"
        @click="clearFilters">
        {{ $t("image_gallery.clear_filters") }}
      </v-btn>
    </div>
    <v-progress-linear class="mx-3" :active="loading" indeterminate height="2"
      style="width: auto;"></v-progress-linear>
  </div>

  <!-- first load: placeholders with the shape of the tiles -->
  <v-row v-if="loading && imagesIds.length == 0" class="mx-2 mx-sm-4">
    <v-col v-for="n in perPage" :key="n" cols="6" sm="4" md="3">
      <v-skeleton-loader type="image, list-item-two-line" class="bg-transparent"></v-skeleton-loader>
    </v-col>
  </v-row>

  <div v-else-if="imagesIds.length > 0" :class="{ 'reloading': loading }">
    <v-row class="mx-2 mx-sm-4">
      <v-col v-for="i in imagesIds" :key="i" cols="6" sm="4" md="3">
        <BirdTile :img-id="i" :name="getImgBirdName(i)" :latin-name="getImgBirdLatinName(i)"
          @click="openPhoto(i)"></BirdTile>
      </v-col>
    </v-row>
    <v-pagination class="mb-5 mt-2" :model-value="page" :length="totalPages" rounded="circle"
      @update:model-value="setPage"></v-pagination>
  </div>

  <v-container v-else-if="!loading">
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card class="d-flex align-center justify-center text-center" height="300px">
          <v-row align="center" justify="center">
            <v-col cols="12" v-if="loadError">
              <v-icon size="40" class="mb-2">mdi-cloud-alert-outline</v-icon>
              <v-card-title class="text-h5 text-wrap">{{ $t("image_gallery.error.title") }}</v-card-title>
              <v-card-text class="text-subtitle-1">{{ $t("image_gallery.error.desc") }}</v-card-text>
              <v-btn prepend-icon="mdi-refresh" @click="loadImages">{{ $t("image_gallery.error.retry") }}</v-btn>
            </v-col>
            <v-col cols="12" v-else>
              <v-card-title class="text-h5 text-wrap">{{ $t("image_gallery.no_match.title") }}</v-card-title>
              <v-card-text class="text-subtitle-1">{{ $t("image_gallery.no_match.desc") }}</v-card-text>
              <v-btn v-if="hasFilters" prepend-icon="mdi-filter-remove-outline" @click="clearFilters">
                {{ $t("image_gallery.clear_filters") }}
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <!-- the URL drives the dialog: the back button is handled by the router, not by the dialog -->
  <v-dialog v-model="photoVisible" max-width="900px" :close-on-back="false">
    <v-card v-if="photo !== null" v-touch="{ left: () => showSiblingPhoto(1), right: () => showSiblingPhoto(-1) }">
      <div class="d-flex align-center px-4 pt-2">
        <span class="text-caption text-medium-emphasis">
          <template v-if="photoPosition">{{ photoPosition }} / {{ total }}</template>
        </span>
        <v-spacer></v-spacer>
        <v-btn icon="mdi-close" variant="text" size="small" :aria-label="$t('a11y.close')"
          @click="closePhoto"></v-btn>
      </div>

      <div class="position-relative px-4">
        <v-img :key="photo" :src="getImageUrl(photo, 1280)" :alt="getImgBirdName(photo) || $t('a11y.bird_photo')" contain
          max-height="65vh" rounded="xl">
          <template v-slot:placeholder>
            <div class="d-flex align-center justify-center fill-height">
              <v-progress-circular indeterminate></v-progress-circular>
            </div>
          </template>
        </v-img>
        <v-btn v-if="hasPrevPhoto" class="photo-nav photo-nav-prev" icon="mdi-chevron-left" size="small"
          variant="elevated" elevation="4" :aria-label="$t('photo.previous')" @click="showSiblingPhoto(-1)"></v-btn>
        <v-btn v-if="hasNextPhoto" class="photo-nav photo-nav-next" icon="mdi-chevron-right" size="small"
          variant="elevated" elevation="4" :aria-label="$t('photo.next')" @click="showSiblingPhoto(1)"></v-btn>
      </div>

      <v-card-item class="text-center">
        <v-card-title class="text-wrap">{{ getImgBirdName(photo) }}</v-card-title>
        <v-card-subtitle class="font-italic">{{ getImgBirdLatinName(photo) }}</v-card-subtitle>
      </v-card-item>

      <v-card-text class="text-center pt-0">
        <div v-if="getImgAuthorName(photo)" class="text-caption text-medium-emphasis credits mb-3">
          {{ $t("photo.credit") }}
          <a :href="getImgAuthorLink(photo)" target="_blank" rel="noopener">{{ getImgAuthorName(photo) }}</a>
          ·
          <a :href="getImgCopyrightLink(photo)" target="_blank" rel="noopener">{{ getImgCopyrightName(photo) }}</a>
          ·
          <a :href="getImageUrl(photo)" target="_blank" rel="noopener">{{ $t("photo.full_size") }}</a>
        </div>
        <v-btn v-if="getImgBirdName(photo)" variant="tonal" size="small" prepend-icon="mdi-image-multiple-outline"
          @click="showAllPhotosOfBird(photo)">
          {{ $t("photo.all_of_bird") }}
        </v-btn>
      </v-card-text>

      <!-- administration: delete the photo, after a confirmation -->
      <v-card-actions v-if="adminStore.loggedIn" class="justify-center pt-0 pb-4">
        <v-btn color="error" variant="text" size="small" prepend-icon="mdi-delete-outline"
          @click="confirmDelete = true">
          {{ $t("admin.delete.button") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="confirmDelete" max-width="420px">
    <v-card :title="$t('admin.delete.title')" :text="$t('admin.delete.desc')">
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="confirmDelete = false">{{ $t("admin.delete.cancel") }}</v-btn>
        <v-btn color="error" variant="flat" :loading="deleting" @click="deleteCurrentPhoto">
          {{ $t("admin.delete.confirm") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="deleteError" color="error" timeout="5000">{{ $t("admin.delete.error") }}</v-snackbar>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch, Ref } from 'vue';
import { useRoute, useRouter, LocationQuery } from 'vue-router';
import { useDisplay } from 'vuetify'
import { getImageUrl, getImages } from '@/api/images';
import BirdTile from '@/components/BirdTile.vue'
import { useAppStore } from '@/store/app';
import { useImagesStore } from '@/store/images'
import { useGroupsStore } from '@/store/groups'
import { useAdminStore } from '@/store/admin'
import { deletePhoto } from '@/api/admin'
import GroupFilters from '@/components/GroupFilters.vue'

const appStore = useAppStore()
const imgStore = useImagesStore()
const groupsStore = useGroupsStore()

// The state of the gallery (search, filters, page and opened photo) is kept in the URL,
// so that it survives a reload, works with the back button and can be shared.
const route = useRoute()
const router = useRouter()

// links shared before the renaming of species to groups (?species=...&sub_species=...)
if (route.query.species !== undefined || route.query.sub_species !== undefined) {
  const { species, sub_species: subSpecies, ...query } = route.query
  router.replace({
    query: { ...query, ...(species ? { group: species } : {}), ...(subSpecies ? { subgroup: subSpecies } : {}) },
  })
}

function queryValue(name: string): string | null {
  const value = route.query[name]
  const first = Array.isArray(value) ? value[0] : value
  return first ? String(first) : null
}

function queryNumber(name: string): number | null {
  const value = parseInt(queryValue(name) ?? "")
  return Number.isFinite(value) && value > 0 ? value : null
}

const search = computed(() => queryValue("q") ?? "")
const selectedGroup = computed(() => queryValue("group"))
const selectedSubgroup = computed(() => queryValue("subgroup"))
const page = computed(() => queryNumber("page") ?? 1)
const photo = computed(() => queryNumber("photo"))

// a null/empty value removes the parameter from the URL
function updateQuery(changes: Record<string, string | number | null>, replace = false) {
  const query: LocationQuery = { ...route.query }
  for (const [key, value] of Object.entries(changes)) {
    if (value === null || value === "") {
      delete query[key]
    } else {
      query[key] = String(value)
    }
  }
  return replace ? router.replace({ query }) : router.push({ query })
}

const hasFilters = computed(() => !!(search.value || selectedGroup.value || selectedSubgroup.value))

function clearFilters() {
  updateQuery({ q: null, group: null, subgroup: null, page: null })
}

function setPage(newPage: number) {
  updateQuery({ page: newPage == 1 ? null : newPage })
}

// search: the URL is updated once the user stops typing
const searchInput: Ref<string | null> = ref(search.value)
let searchTimer: ReturnType<typeof setTimeout> | undefined
function onSearchInput(value: string | null) {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    updateQuery({ q: value?.trim() || null, page: null }, true)
  }, 300)
}
// the URL can also change from outside the field (back button, "all photos of this bird")
watch(search, (value) => {
  if (value != (searchInput.value ?? "").trim()) {
    searchInput.value = value
  }
})

// images
const perPage = 12
const imagesIds: Ref<number[]> = ref([])
const total = ref(0)
const totalPages = computed(() => Math.ceil(total.value / perPage))
const loading = ref(false)
const loadError = ref(false)

// only the response of the latest request is used (the user may type faster than the API answers)
let lastRequest = 0
async function loadImages() {
  const request = ++lastRequest
  loading.value = true
  loadError.value = false
  try {
    const res = await getImages(appStore.locale, selectedGroup.value, selectedSubgroup.value, search.value,
      page.value, perPage)
    if (request != lastRequest) {
      return
    }
    imagesIds.value = res.data.items
    total.value = res.data.total
    // the captions are filled as soon as the information arrives
    imgStore.fetchImageInfo(imagesIds.value, appStore.locale)
  } catch {
    if (request == lastRequest) {
      imagesIds.value = []
      loadError.value = true
    }
  } finally {
    if (request == lastRequest) {
      loading.value = false
    }
  }
}
watch([search, selectedGroup, selectedSubgroup, page, () => appStore.locale], loadImages, { immediate: true })
watch(page, () => window.scrollTo({ top: 0, behavior: "smooth" }))

// group filters
const groups: Ref<{ key: string, value: string }[]> = ref([])
const subgroups: Ref<{ key: string, value: string }[]> = ref([])

function toItems(values: string[]) {
  return values.filter(v => v).map(v => ({ key: v, value: capitalizeFirstLetter(v) }))
}

async function loadGroups() {
  try {
    groups.value = toItems(await groupsStore.getGroups(appStore.locale))
  } catch {
    groups.value = []
  }
}

async function loadSubgroups() {
  subgroups.value = []
  if (selectedGroup.value) {
    try {
      subgroups.value = toItems(await groupsStore.getSubgroups(appStore.locale, selectedGroup.value))
    } catch {
      subgroups.value = []
    }
  }
}

function selectGroup(value: string | null) {
  updateQuery({ group: value, subgroup: null, page: null })
}

function selectSubgroup(value: string | null) {
  updateQuery({ subgroup: value, page: null })
}

function clearGroupFilters() {
  updateQuery({ group: null, subgroup: null, page: null })
}

const activeFiltersCount = computed(() => (selectedGroup.value ? 1 : 0) + (selectedSubgroup.value ? 1 : 0))
const filtersSheet = ref(false)

onMounted(loadGroups)
watch(selectedGroup, loadSubgroups, { immediate: true })
// the group names depend on the language, the group filters are thus reset
watch(() => appStore.locale, async () => {
  if (selectedGroup.value || selectedSubgroup.value) {
    await updateQuery({ group: null, subgroup: null, page: null }, true)
  }
  await loadGroups()
  await loadSubgroups()
})

// photo dialog
const photoVisible = computed({
  get: () => photo.value !== null,
  set: (visible: boolean) => {
    if (!visible) {
      closePhoto()
    }
  },
})

// opening a photo adds an history entry, so that the back button closes it
let photoOpenedHere = false
function openPhoto(imgId: number) {
  photoOpenedHere = true
  updateQuery({ photo: imgId })
}
function closePhoto() {
  if (photoOpenedHere) {
    photoOpenedHere = false
    router.back()
  } else {
    updateQuery({ photo: null }, true)
  }
}
watch(photo, (imgId) => {
  if (imgId === null) {
    photoOpenedHere = false
  } else {
    // the photo may not be on the current page (shared link)
    imgStore.fetchImageInfo([imgId], appStore.locale)
  }
}, { immediate: true })

const photoIndex = computed(() => photo.value === null ? -1 : imagesIds.value.indexOf(photo.value))
const photoPosition = computed(() => photoIndex.value < 0 ? null : (page.value - 1) * perPage + photoIndex.value + 1)
const hasPrevPhoto = computed(() => photoIndex.value > 0 || (photoIndex.value == 0 && page.value > 1))
const hasNextPhoto = computed(() => photoIndex.value >= 0
  && (photoIndex.value < imagesIds.value.length - 1 || page.value < totalPages.value))

// previous/next photo, possibly on the previous/next page
async function showSiblingPhoto(delta: 1 | -1) {
  if ((delta < 0 && !hasPrevPhoto.value) || (delta > 0 && !hasNextPhoto.value)) {
    return
  }
  const index = photoIndex.value + delta
  if (index >= 0 && index < imagesIds.value.length) {
    updateQuery({ photo: imagesIds.value[index] }, true)
    return
  }
  const newPage = page.value + delta
  try {
    const res = await getImages(appStore.locale, selectedGroup.value, selectedSubgroup.value, search.value,
      newPage, perPage)
    const ids: number[] = res.data.items
    if (ids.length > 0) {
      updateQuery({ page: newPage == 1 ? null : newPage, photo: delta > 0 ? ids[0] : ids[ids.length - 1] }, true)
    }
  } catch {
    // stay on the current photo
  }
}

function onKeydown(event: KeyboardEvent) {
  if (photo.value === null) {
    return
  }
  if (event.key == "ArrowLeft") {
    showSiblingPhoto(-1)
  } else if (event.key == "ArrowRight") {
    showSiblingPhoto(1)
  }
}
onMounted(() => window.addEventListener("keydown", onKeydown))
onUnmounted(() => {
  window.removeEventListener("keydown", onKeydown)
  clearTimeout(searchTimer)
})

// administration
const adminStore = useAdminStore()
const confirmDelete = ref(false)
const deleting = ref(false)
const deleteError = ref(false)

async function deleteCurrentPhoto() {
  if (photo.value === null) {
    return
  }
  deleting.value = true
  try {
    await deletePhoto(adminStore.password, photo.value)
    confirmDelete.value = false
    // the photo does not exist anymore: no history entry to go back to
    photoOpenedHere = false
    await updateQuery({ photo: null }, true)
    await loadImages()
  } catch (err: unknown) {
    if ((err as { response?: { status?: number } }).response?.status == 401) {
      adminStore.logout()
    }
    deleteError.value = true
  } finally {
    deleting.value = false
  }
}

function showAllPhotosOfBird(imgId: number) {
  const birdInfo = imgStore.getImageInfo(imgId, appStore.locale)
  if (birdInfo) {
    photoOpenedHere = false
    updateQuery({ q: birdInfo.bird.name, group: null, subgroup: null, page: null, photo: null })
  }
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

const { name } = useDisplay()
const smallScreen = computed(() => name.value == "xs" || name.value == "sm")
const density = computed(() => name.value == "xs" ? "compact" : "default")

function capitalizeFirstLetter(str: string): string {
  return str ? str[0].toUpperCase() + str.slice(1) : str;
}
</script>

<style scoped>
.results-bar {
  min-height: 36px;
}

.reloading {
  opacity: 0.6;
  transition: opacity 0.2s;
}

.photo-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.photo-nav-prev {
  left: 24px;
}

.photo-nav-next {
  right: 24px;
}

.credits a {
  color: inherit;
}
</style>
