<template>
  <h1 class="text-center">Quiz</h1>
  <h2 class="text-center">Test your knowledge with customizable quiz!</h2>

  <div class="my-10"></div>

  <v-container fluid class="d-flex align-center justify-center">
    <v-card class="text-center" width="500px">
      <v-card-title>Configure your quiz</v-card-title>
      <v-card-text>
        <v-autocomplete v-model="selectedSpecies" clearable :items="species" item-title="value" item-value="key"
          :label="$t('speciesSelect')" @update:model-value="updateSubSpecies()" density="compact">
        </v-autocomplete>
        <v-autocomplete :disabled="subSpecies.length == 0" v-model="selectedSubSpecies" clearable :items="subSpecies"
          item-title="value" item-value="key" :label="$t('subSpeciesSelect')" density="compact">
        </v-autocomplete>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn variant="outlined" append-icon="mdi-arrow-right-thin" color="primary" @click="startQuizz()">Start
          quiz!</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>

  <QuizQuestion :imageId="quizImageId!" :options="quizOption!" />
</template>

<script setup lang="ts">
import { Ref, ref, onMounted } from 'vue';
import { useAppStore } from '@/store/app';
import { useSpeciesStore } from '@/store/species'
import { getQuiz } from '@/api/quiz';
import QuizQuestion from './QuizQuestion.vue';

const appStore = useAppStore()
const speciesStore = useSpeciesStore()

const species: Ref<{ key: string, value: string }[]> = ref([])
const subSpecies: Ref<{ key: string, value: string }[]> = ref([])

// const selectedSpecies: Ref<string[] | null> = ref(null)
// const selectedSubSpecies: Ref<string[] | null> = ref(null)

const selectedSpecies: Ref<string | null> = ref(null)
const selectedSubSpecies: Ref<string | null> = ref(null)

onMounted(async () => {
  let spcs = await speciesStore.getSpecies(appStore.locale)
  console.log(spcs)
  species.value = spcs.map(s => ({ key: s, value: capitalizeFirstLetter(s) }))
})

async function updateSubSpecies() {
  selectedSubSpecies.value = null
  subSpecies.value = []
  if (selectedSpecies.value != null && selectedSpecies.value.length > 0) {
    let spcs = await speciesStore.getSubSpecies(appStore.locale, selectedSpecies.value)
    subSpecies.value = spcs.map(s => ({ key: s, value: capitalizeFirstLetter(s) }))
  }
}

function capitalizeFirstLetter(str: string): string {
  return str[0].toUpperCase() + str.slice(1);
}

const quizImageId: Ref<null | number> = ref(null)
const quizOption: Ref<number[]> = ref([])
async function startQuizz() {
  const res = await getQuiz(appStore.locale, selectedSpecies.value, selectedSubSpecies.value)
  if (res.status != 200) {
    return null
  }
  console.log(res.data)
  quizImageId.value = res.data.quiz_image
  quizOption.value = res.data.options
}
</script>

<style scoped></style>
