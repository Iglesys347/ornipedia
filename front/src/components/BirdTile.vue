<template>
  <!-- photo of a bird with its name, used by the gallery and the home page -->
  <v-card class="bird-tile" :to="to" @click="emit('click')">
    <v-img :src="getImageUrl(imgId, 640)" :srcset="getImageSrcset(imgId)" :sizes="sizes"
      :alt="name || $t('a11y.bird_photo')" :aspect-ratio="4 / 3" cover rounded="xl">
      <template v-slot:placeholder>
        <div class="tile-placeholder fill-height"></div>
      </template>
      <template v-slot:error>
        <div class="tile-placeholder fill-height d-flex align-center justify-center">
          <v-icon color="medium-emphasis">mdi-image-off-outline</v-icon>
        </div>
      </template>
    </v-img>
    <div class="pa-2">
      <div class="text-body-2 text-sm-subtitle-1 font-weight-medium text-truncate">
        {{ name || "\u00a0" }}
      </div>
      <div class="text-caption font-italic text-medium-emphasis text-truncate">
        {{ latinName || "\u00a0" }}
      </div>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router';
import { getImageSrcset, getImageUrl } from '@/api/images';

withDefaults(defineProps<{
  imgId: number
  name?: string
  latinName?: string
  // displayed width of the tile (`sizes` attribute), by default 2 columns on mobile, 3 on tablet, 4 on desktop
  sizes?: string
  to?: RouteLocationRaw
}>(), {
  name: "",
  latinName: "",
  sizes: "(max-width: 599px) 50vw, (max-width: 959px) 33vw, 25vw",
  to: undefined,
})

const emit = defineEmits<{ click: [] }>()
</script>

<style scoped>
.bird-tile {
  background: transparent;
}

.tile-placeholder {
  background: rgba(var(--v-theme-on-surface), 0.08);
}
</style>
