<template>
  <v-row>
    <v-col v-for="(imgId, s) in species" :key="s" class="d-flex child-flex" cols="4">
      <v-img :src="getImageUrl(imgId as number)" aspect-ratio="1" cover class="cursor-pointer">
        <v-slide-y-reverse-transition>
          <v-card class="d-flex flex-column bg-transparent" elevation="0" rounded="0" style="height: 100%;">
            <v-spacer></v-spacer>
            <v-card-actions class="justify-center text-white" style="background-color: rgba(0, 0, 0, 0.3);">
              <span>{{ s }}</span>
            </v-card-actions>
          </v-card>
        </v-slide-y-reverse-transition>
      </v-img>

    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { getRandomImage, getImageUrl } from '@/api/images';
import { getSpecies } from '@/api/species';
import { useAppStore } from '@/store/app';
import { Ref, onMounted, ref } from 'vue';

const appStore = useAppStore()

const species: Ref<{ [species: string]: number }> = ref({})

onMounted(async () => {
  let sp: string[] = []
  const res = await getSpecies(appStore.locale)
  if (res.status == 200) {
    sp = res.data.items
  }
  for (const s of sp) {
    const imgId = await getRandomImage(s)
    species.value[s] = imgId.data.id
  }
})
</script>
