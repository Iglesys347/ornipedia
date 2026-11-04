<template>
  <!-- searchable lists: usable with hundreds of groups and subgroups -->
  <v-row dense>
    <v-col cols="12" :md="stacked ? 12 : 6">
      <v-autocomplete :model-value="selectedGroup" :items="groups" item-title="value" item-value="key"
        :label="$t('groupSelect')" :density="density" :no-data-text="$t('image_gallery.no_result')" clearable
        hide-details auto-select-first @update:model-value="emit('update:group', $event ?? null)">
      </v-autocomplete>
    </v-col>
    <v-col cols="12" :md="stacked ? 12 : 6">
      <v-autocomplete :model-value="selectedSubgroup" :items="subgroups" item-title="value" item-value="key"
        :label="$t('subgroupSelect')" :density="density" :no-data-text="$t('image_gallery.no_result')"
        :disabled="!selectedGroup || subgroups.length == 0" clearable hide-details auto-select-first
        @update:model-value="emit('update:subgroup', $event ?? null)">
      </v-autocomplete>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
type Item = { key: string, value: string }

defineProps<{
  groups: Item[]
  subgroups: Item[]
  selectedGroup: string | null
  selectedSubgroup: string | null
  density?: "default" | "comfortable" | "compact"
  // one field per line (mobile panel)
  stacked?: boolean
}>()

const emit = defineEmits<{
  'update:group': [value: string | null]
  'update:subgroup': [value: string | null]
}>()
</script>
