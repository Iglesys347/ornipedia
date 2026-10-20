<template>
  <v-container class="py-8 admin">
    <h1 class="text-h4 font-weight-light mb-6">{{ $t("admin.title") }}</h1>

    <!-- login -->
    <v-card v-if="!adminStore.loggedIn" max-width="440" class="mx-auto">
      <v-form @submit.prevent="submitLogin">
        <v-card-text>
          <p class="mb-4">{{ $t("admin.login.desc") }}</p>
          <v-text-field v-model="loginPassword" :label="$t('admin.login.password')" type="password"
            autocomplete="current-password" autofocus
            :error-messages="loginError ? [$t(`admin.login.errors.${loginError}`)] : []"></v-text-field>
        </v-card-text>
        <v-card-actions class="px-4 pb-4">
          <v-spacer></v-spacer>
          <v-btn type="submit" color="primary" variant="flat" :loading="loggingIn" :disabled="!loginPassword">
            {{ $t("admin.login.submit") }}
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>

    <template v-else>
      <div class="d-flex align-center flex-wrap mb-4">
        <v-tabs v-model="tab" color="primary">
          <v-tab value="photo" prepend-icon="mdi-image-plus-outline">
            {{ $t(xs ? "admin.photo.tab_short" : "admin.photo.tab") }}
          </v-tab>
          <v-tab value="bird" prepend-icon="mdi-bird">
            {{ $t(xs ? "admin.bird.tab_short" : "admin.bird.tab") }}
          </v-tab>
        </v-tabs>
        <v-spacer></v-spacer>
        <v-btn variant="text" prepend-icon="mdi-logout" @click="adminStore.logout()">{{ $t("admin.logout") }}</v-btn>
      </div>

      <v-window v-model="tab">
        <!-- add a photo to an existing bird -->
        <v-window-item value="photo">
          <v-card class="mb-4">
            <v-card-text>
              <v-autocomplete v-model="photoBird" :items="birds" item-value="id" :item-title="birdTitle"
                :label="$t('admin.photo.bird')" :loading="birdsLoading" hide-details
                :no-data-text="$t('image_gallery.no_species')" prepend-inner-icon="mdi-bird"></v-autocomplete>
            </v-card-text>
          </v-card>

          <!-- photos of Wikimedia Commons, their author and license are fetched by the API -->
          <v-card class="mb-4">
            <v-card-item prepend-icon="mdi-image-search-outline" :title="$t('admin.commons.title')"
              :subtitle="$t('admin.commons.subtitle')"></v-card-item>
            <v-card-text>
              <v-form @submit.prevent="searchCommons()">
                <v-text-field v-model="commonsQuery" :label="$t('admin.commons.search')"
                  :hint="$t('admin.commons.search_hint')" persistent-hint append-inner-icon="mdi-magnify"
                  :loading="commonsLoading" @click:append-inner="searchCommons()"></v-text-field>
              </v-form>

              <v-alert v-if="commonsError" type="error" variant="tonal" class="mt-4">{{ commonsError }}</v-alert>
              <p v-else-if="commonsSearched && commonsResults.length == 0 && !commonsLoading"
                class="text-medium-emphasis mt-4">
                {{ $t("admin.commons.no_result") }}
              </p>

              <v-row v-if="commonsResults.length > 0" class="mt-2">
                <v-col v-for="photo in commonsResults" :key="photo.title" cols="6" sm="4" md="3">
                  <v-card class="commons-photo" :disabled="photo.already_added || importing" variant="flat"
                    :class="{ 'commons-selected': selectedTitles.includes(photo.title) }"
                    :aria-pressed="selectedTitles.includes(photo.title)" @click="toggleCommonsPhoto(photo)">
                    <v-img :src="photo.thumbnail_url" :alt="photo.description" :aspect-ratio="4 / 3" cover
                      rounded="lg">
                      <template v-slot:placeholder>
                        <div class="commons-placeholder fill-height"></div>
                      </template>
                      <div class="d-flex justify-space-between pa-1">
                        <v-icon v-if="selectedTitles.includes(photo.title)" color="primary"
                          class="bg-surface rounded-circle">mdi-check-circle</v-icon>
                        <v-chip v-else-if="photo.already_added" size="x-small" variant="flat">
                          {{ $t("admin.commons.already_added") }}
                        </v-chip>
                        <span v-else></span>
                        <v-btn :href="photo.page_url" target="_blank" rel="noopener" icon="mdi-open-in-new"
                          size="x-small" variant="flat" :aria-label="$t('admin.commons.open')"
                          @click.stop></v-btn>
                      </div>
                    </v-img>
                    <div class="pa-1 text-caption">
                      <div class="text-truncate" :title="photo.author_name">{{ photo.author_name }}</div>
                      <div class="text-truncate text-medium-emphasis">
                        {{ photo.license_short_name }} · {{ photo.width }}×{{ photo.height }}
                      </div>
                    </div>
                  </v-card>
                </v-col>
              </v-row>

              <div v-if="commonsNextOffset !== null" class="text-center mt-2">
                <v-btn variant="text" :loading="commonsLoading" @click="searchCommons(true)">
                  {{ $t("admin.commons.more") }}
                </v-btn>
              </div>
              <v-progress-linear v-if="importing" :model-value="importProgress" color="primary" height="6"
                rounded class="mt-4"></v-progress-linear>
            </v-card-text>
            <v-card-actions class="px-4 pb-4">
              <span class="text-body-2 text-medium-emphasis">
                {{ $t("admin.commons.selected", selectedTitles.length) }}
              </span>
              <v-spacer></v-spacer>
              <v-btn color="primary" variant="flat" prepend-icon="mdi-download" :loading="importing"
                :disabled="selectedTitles.length == 0" @click="importSelected">
                {{ $t("admin.commons.import", selectedTitles.length) }}
              </v-btn>
            </v-card-actions>
          </v-card>

          <v-expansion-panels>
            <v-expansion-panel :title="$t('admin.photo.upload_title')">
              <v-expansion-panel-text>
                <v-form ref="photoFormRef" @submit.prevent="submitPhoto">
                  <v-card variant="flat">
                    <v-card-text class="px-0">
                      <v-file-input v-model="photoFile" accept="image/jpeg,image/png,image/webp"
                        :label="$t('admin.photo.file')" :hint="$t('admin.photo.file_hint')" persistent-hint show-size
                        prepend-icon="" prepend-inner-icon="mdi-camera-outline" :rules="[requiredFile, maxSize]"
                        class="mb-2"></v-file-input>
                      <v-img v-if="previewUrl" :src="previewUrl" max-height="280" class="mb-4" rounded="lg"
                        :alt="$t('admin.photo.preview')"></v-img>

                      <v-row dense>
                        <v-col cols="12" sm="6">
                          <v-combobox v-model="authorName" :items="authorNames" :label="$t('admin.photo.author')"
                            :rules="[required]" @update:model-value="fillAuthor"></v-combobox>
                        </v-col>
                        <v-col cols="12" sm="6">
                          <v-text-field v-model="authorLink" :label="$t('admin.photo.author_link')"
                            type="url"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="4">
                          <v-combobox v-model="licenseShortName" :items="licenseNames" :label="$t('admin.photo.license')"
                            :rules="[required]" @update:model-value="fillLicense"></v-combobox>
                        </v-col>
                        <v-col cols="12" sm="8">
                          <v-text-field v-model="licenseFullName" :label="$t('admin.photo.license_full')"
                            :rules="[required]"></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-text-field v-model="licenseLink" :label="$t('admin.photo.license_link')" type="url"
                            :rules="[required]"></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-text-field v-model="originalUrl" :label="$t('admin.photo.original_url')"
                            type="url"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-progress-linear v-if="uploading" :model-value="uploadProgress" color="primary" height="6"
                        rounded></v-progress-linear>
                    </v-card-text>
                    <v-card-actions class="px-0">
                      <v-spacer></v-spacer>
                      <v-btn type="submit" color="primary" variant="flat" prepend-icon="mdi-upload" :loading="uploading">
                        {{ $t("admin.photo.submit") }}
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-form>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-window-item>

        <!-- add a bird, with a translation per language -->
        <v-window-item value="bird">
          <v-form ref="birdFormRef" @submit.prevent="submitBird">
            <v-card>
              <v-card-text>
                <v-text-field v-model="latinName" :label="$t('admin.bird.latin_name')"
                  :rules="[required]"></v-text-field>

                <div v-for="lang in supportedLanguages" :key="lang.code" class="mt-2">
                  <h2 class="text-subtitle-1 font-weight-medium mb-2" :lang="lang.code">{{ lang.name }}</h2>
                  <v-row dense>
                    <v-col cols="12" sm="6">
                      <v-text-field v-model="translations[lang.code].name" :label="$t('admin.bird.name')"
                        :rules="[required]"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-combobox v-model="translations[lang.code].species" :items="speciesOptions[lang.code]"
                        :label="$t('admin.bird.species')" :hint="$t('admin.bird.species_hint')" :rules="[required]"
                        @update:model-value="loadSubSpecies(lang.code)"></v-combobox>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-combobox v-model="translations[lang.code].sub_species" :items="subSpeciesOptions[lang.code]"
                        :label="$t('admin.bird.sub_species')"></v-combobox>
                    </v-col>
                    <v-col cols="12">
                      <v-textarea v-model="translations[lang.code].details" :label="$t('admin.bird.details')"
                        rows="2" auto-grow></v-textarea>
                    </v-col>
                  </v-row>
                </div>
              </v-card-text>
              <v-card-actions class="px-4 pb-4">
                <v-spacer></v-spacer>
                <v-btn type="submit" color="primary" variant="flat" prepend-icon="mdi-plus" :loading="creatingBird">
                  {{ $t("admin.bird.submit") }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-form>
        </v-window-item>
      </v-window>
    </template>

    <v-snackbar v-model="snackbar.show" :color="snackbar.error ? 'error' : 'primary'" timeout="6000">
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn v-if="snackbar.to" :to="snackbar.to" variant="text">{{ $t("admin.see") }}</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onUnmounted, reactive, ref, Ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useDisplay } from 'vuetify';
import type { RouteLocationRaw } from 'vue-router';
import {
  createBird, getAuthors, getLicenses, importFromCommons, searchCommons as apiSearchCommons, uploadPhoto,
  Author, CommonsPhoto, License,
} from '@/api/admin';
import { getAllBirds, BirdSummary } from '@/api/birds';
import { useAdminStore, LoginError } from '@/store/admin';
import { useAppStore } from '@/store/app';
import { useSpeciesStore } from '@/store/species';
import { supportedLanguages } from '@/translations/i18n';

const { t } = useI18n()
const { xs } = useDisplay()
const adminStore = useAdminStore()
const appStore = useAppStore()
const speciesStore = useSpeciesStore()

// same limit as the API
const MAX_UPLOAD_SIZE = 25 * 1024 * 1024

type Form = { validate: () => Promise<{ valid: boolean }>, resetValidation: () => void }

const required = (value: unknown) => (value !== null && value !== undefined && String(value).trim() != "")
  || t("admin.errors.required")
const requiredFile = () => !!selectedFile.value || t("admin.errors.required")
const maxSize = () => !selectedFile.value || selectedFile.value.size <= MAX_UPLOAD_SIZE || t("admin.errors.too_big")

const snackbar = reactive({ show: false, text: "", error: false, to: null as RouteLocationRaw | null })
function notify(text: string, error = false, to: RouteLocationRaw | null = null) {
  Object.assign(snackbar, { show: true, text, error, to })
}

// message for a failed request; a refused password logs out
function requestError(err: unknown): string {
  const response = (err as { response?: { status?: number, data?: { detail?: unknown } } }).response
  if (!response) {
    return t("admin.errors.network")
  }
  if (response.status == 401) {
    adminStore.logout()
    return t("admin.errors.session")
  }
  if (response.status == 413) {
    return t("admin.errors.too_big")
  }
  if (response.status == 502) {
    return t("admin.errors.commons")
  }
  const detail = response.data?.detail
  return typeof detail == "string" ? detail : t("admin.errors.invalid")
}

// login
const loginPassword = ref("")
const loginError: Ref<LoginError | null> = ref(null)
const loggingIn = ref(false)
async function submitLogin() {
  loggingIn.value = true
  loginError.value = await adminStore.login(loginPassword.value)
  loggingIn.value = false
  if (!loginError.value) {
    loginPassword.value = ""
  }
}

const tab = ref("photo")

// data used by the forms
const birds: Ref<BirdSummary[]> = ref([])
const birdsLoading = ref(false)
const authors: Ref<Author[]> = ref([])
const licenses: Ref<License[]> = ref([])
const authorNames = computed(() => [...new Set(authors.value.map(a => a.name).filter((n): n is string => !!n))])
const licenseNames = computed(() => [...new Set(licenses.value.map(l => l.short_name))])

async function loadBirds() {
  birdsLoading.value = true
  try {
    birds.value = await getAllBirds(appStore.locale)
  } catch (err) {
    notify(requestError(err), true)
  } finally {
    birdsLoading.value = false
  }
}

async function loadAuthorsAndLicenses() {
  try {
    const [authorsRes, licensesRes] = await Promise.all([
      getAuthors(adminStore.password), getLicenses(adminStore.password)])
    authors.value = authorsRes.data
    licenses.value = licensesRes.data
  } catch (err) {
    notify(requestError(err), true)
  }
}

function capitalize(str: string) {
  return str ? str[0].toUpperCase() + str.slice(1) : str
}
function birdTitle(bird: BirdSummary) {
  return `${capitalize(bird.name)} (${bird.latin_name})`
}

// photo form
const photoFormRef: Ref<Form | null> = ref(null)
const photoBird: Ref<number | null> = ref(null)
const photoFile: Ref<File | File[] | null> = ref(null)
const selectedFile = computed(() => Array.isArray(photoFile.value) ? photoFile.value[0] ?? null : photoFile.value)
const authorName: Ref<string | null> = ref(null)
const authorLink = ref("")
const licenseShortName: Ref<string | null> = ref(null)
const licenseFullName = ref("")
const licenseLink = ref("")
const originalUrl = ref("")
const uploading = ref(false)
const uploadProgress = ref(0)

const previewUrl = ref("")
watch(selectedFile, (file) => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  previewUrl.value = file ? URL.createObjectURL(file) : ""
})
onUnmounted(() => previewUrl.value && URL.revokeObjectURL(previewUrl.value))

// an existing author or license fills the other fields
function fillAuthor(name: string | null) {
  const author = authors.value.find(a => a.name == name)
  if (author) {
    authorLink.value = author.link ?? ""
  }
}
function fillLicense(shortName: string | null) {
  const license = licenses.value.find(l => l.short_name == shortName)
  if (license) {
    licenseFullName.value = license.full_name
    licenseLink.value = license.link
  }
}

async function submitPhoto() {
  if (photoBird.value === null) {
    notify(t("admin.photo.choose_bird"), true)
    return
  }
  if (!(await photoFormRef.value?.validate())?.valid || !selectedFile.value) {
    return
  }
  uploading.value = true
  uploadProgress.value = 0
  try {
    const res = await uploadPhoto(adminStore.password, photoBird.value, selectedFile.value, {
      author_name: authorName.value ?? "",
      author_link: authorLink.value,
      license_short_name: licenseShortName.value ?? "",
      license_full_name: licenseFullName.value,
      license_link: licenseLink.value,
      original_url: originalUrl.value,
    }, (percent) => uploadProgress.value = percent)
    notify(t("admin.photo.added"), false, { path: "/birds", query: { photo: res.data.id } })
    // the bird, author and license are kept to add several photos in a row
    photoFile.value = null
    originalUrl.value = ""
    photoFormRef.value?.resetValidation()
    loadAuthorsAndLicenses()
  } catch (err) {
    notify(requestError(err), true)
  } finally {
    uploading.value = false
  }
}

// photos of Wikimedia Commons
const commonsQuery = ref("")
const commonsResults: Ref<CommonsPhoto[]> = ref([])
const commonsNextOffset: Ref<number | null> = ref(null)
const commonsLoading = ref(false)
const commonsSearched = ref(false)
const commonsError = ref("")
const selectedTitles: Ref<string[]> = ref([])
const importing = ref(false)
const importProgress = ref(0)

// only the answer of the latest search is used
let lastSearch = 0
async function searchCommons(more = false) {
  const query = commonsQuery.value.trim()
  if (!query) {
    return
  }
  const request = ++lastSearch
  commonsLoading.value = true
  commonsError.value = ""
  if (!more) {
    commonsResults.value = []
    selectedTitles.value = []
    commonsNextOffset.value = null
  }
  try {
    const res = await apiSearchCommons(adminStore.password, query, more ? commonsNextOffset.value ?? 0 : 0)
    if (request != lastSearch) {
      return
    }
    const known = new Set(commonsResults.value.map(p => p.title))
    commonsResults.value = [...commonsResults.value, ...res.data.items.filter(p => !known.has(p.title))]
    commonsNextOffset.value = res.data.next_offset ?? null
    commonsSearched.value = true
  } catch (err) {
    if (request == lastSearch) {
      commonsError.value = requestError(err)
    }
  } finally {
    if (request == lastSearch) {
      commonsLoading.value = false
    }
  }
}

function toggleCommonsPhoto(photo: CommonsPhoto) {
  if (photo.already_added) {
    return
  }
  const index = selectedTitles.value.indexOf(photo.title)
  if (index < 0) {
    selectedTitles.value.push(photo.title)
  } else {
    selectedTitles.value.splice(index, 1)
  }
}

function markAdded(title: string) {
  const photo = commonsResults.value.find(p => p.title == title)
  if (photo) {
    photo.already_added = true
  }
}

// the selected photos are imported one after the other
async function importSelected() {
  if (photoBird.value === null) {
    notify(t("admin.photo.choose_bird"), true)
    return
  }
  const birdId = photoBird.value
  const titles = [...selectedTitles.value]
  importing.value = true
  importProgress.value = 0
  let added = 0
  let failed = 0
  let lastError = ""
  for (const [index, title] of titles.entries()) {
    try {
      await importFromCommons(adminStore.password, birdId, title)
      added++
      markAdded(title)
    } catch (err) {
      const status = (err as { response?: { status?: number } }).response?.status
      if (status == 409) {
        markAdded(title)
      } else {
        failed++
        lastError = requestError(err)
        if (status == 401) {
          break
        }
      }
    }
    importProgress.value = Math.round(100 * (index + 1) / titles.length)
  }
  selectedTitles.value = []
  importing.value = false

  const bird = birds.value.find(b => b.id == birdId)
  const link = bird ? { path: "/birds", query: { q: bird.name } } : null
  if (failed > 0) {
    notify(`${t("admin.commons.import_failed", { added, failed })} ${lastError}`, true, added > 0 ? link : null)
  } else {
    notify(t("admin.commons.imported", added), false, link)
  }
  loadAuthorsAndLicenses()
}

// choosing a bird searches its photos (by latin name)
watch(photoBird, (birdId) => {
  const bird = birds.value.find(b => b.id == birdId)
  if (bird) {
    commonsQuery.value = bird.latin_name
    searchCommons()
  }
})

// bird form
type TranslationFields = { name: string, species: string | null, sub_species: string | null, details: string }
function emptyTranslations(): Record<string, TranslationFields> {
  return Object.fromEntries(supportedLanguages.map(l => [l.code, { name: "", species: null, sub_species: null, details: "" }]))
}
const birdFormRef: Ref<Form | null> = ref(null)
const latinName = ref("")
const translations: Ref<Record<string, TranslationFields>> = ref(emptyTranslations())
const speciesOptions: Ref<Record<string, string[]>> = ref({})
const subSpeciesOptions: Ref<Record<string, string[]>> = ref({})
const creatingBird = ref(false)

async function loadSpeciesOptions() {
  for (const lang of supportedLanguages) {
    speciesOptions.value[lang.code] = await speciesStore.getSpecies(lang.code).catch(() => [])
  }
}

async function loadSubSpecies(lang: string) {
  const species = translations.value[lang].species
  subSpeciesOptions.value[lang] = species
    ? (await speciesStore.getSubSpecies(lang, species).catch(() => [])).filter(s => s)
    : []
}

async function submitBird() {
  if (!(await birdFormRef.value?.validate())?.valid) {
    return
  }
  creatingBird.value = true
  try {
    const res = await createBird(adminStore.password, latinName.value, supportedLanguages.map(l => ({
      language_code: l.code,
      name: translations.value[l.code].name,
      species: translations.value[l.code].species ?? "",
      sub_species: translations.value[l.code].sub_species || null,
      details: translations.value[l.code].details || null,
    })))
    notify(t("admin.bird.added"))
    // the species of the new bird may be new
    speciesStore.clear()
    latinName.value = ""
    translations.value = emptyTranslations()
    birdFormRef.value?.resetValidation()
    // next step: its photos
    await loadBirds()
    photoBird.value = res.data.id
    tab.value = "photo"
    loadSpeciesOptions()
  } catch (err) {
    notify(requestError(err), true)
  } finally {
    creatingBird.value = false
  }
}

watch(() => adminStore.loggedIn, (loggedIn) => {
  if (loggedIn) {
    loadBirds()
    loadAuthorsAndLicenses()
    loadSpeciesOptions()
  }
}, { immediate: true })
watch(() => appStore.locale, () => adminStore.loggedIn && loadBirds())
</script>

<style scoped>
.admin {
  max-width: 900px;
}

.commons-photo {
  outline: 2px solid transparent;
  transition: outline-color 0.15s;
}

.commons-selected {
  outline-color: rgb(var(--v-theme-primary));
}

.commons-placeholder {
  background: rgba(var(--v-theme-on-surface), 0.08);
}
</style>
