<template>
  <!-- searchable lists: usable with hundreds of species and sub-species -->
  <v-row dense>
    <v-col cols="12" :md="stacked ? 12 : 6">
      <v-autocomplete :model-value="selectedSpecies" :items="species" item-title="value" item-value="key"
        :label="$t('speciesSelect')" :density="density" :no-data-text="$t('image_gallery.no_species')" clearable
        hide-details auto-select-first @update:model-value="emit('update:species', $event ?? null)">
      </v-autocomplete>
    </v-col>
    <v-col cols="12" :md="stacked ? 12 : 6">
      <v-autocomplete :model-value="selectedSubSpecies" :items="subSpecies" item-title="value" item-value="key"
        :label="$t('subSpeciesSelect')" :density="density" :no-data-text="$t('image_gallery.no_species')"
        :disabled="!selectedSpecies || subSpecies.length == 0" clearable hide-details auto-select-first
        @update:model-value="emit('update:subSpecies', $event ?? null)">
      </v-autocomplete>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
type Item = { key: string, value: string }

defineProps<{
  species: Item[]
  subSpecies: Item[]
  selectedSpecies: string | null
  selectedSubSpecies: string | null
  density?: "default" | "comfortable" | "compact"
  // one field per line (mobile panel)
  stacked?: boolean
}>()

const emit = defineEmits<{
  'update:species': [value: string | null]
  'update:subSpecies': [value: string | null]
}>()
</script>
