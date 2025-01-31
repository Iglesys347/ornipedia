<template>
  <v-container>
    <!-- Top Image Placeholder -->
    <v-row justify="center" class="mb-4">
      <v-img :src="getImageUrl(imageId)" alt="Placeholder Image" max-height="200" max-width="200"></v-img>
    </v-row>

    <!-- Caption under the image -->
    <v-row justify="center" class="mb-6">
      <v-typography class="text-center" variant="h6">
        Example Text
      </v-typography>
    </v-row>

    <!-- Circle in the center with thumbs -->
    <v-row justify="center" align="center">
      <div style="
          width: 150px;
          height: 150px;
          border-radius: 50%;
          background-color: #f0f0f0;
          display: flex;
          align-items: center;
          justify-content: center;
          position: absolute;
          z-index: 1;
        ">
        <v-icon v-if="answerState === 'correct'" color="green" size="48">mdi-thumb-up</v-icon>
        <v-icon v-if="answerState === 'wrong'" color="red" size="48">mdi-thumb-down</v-icon>
      </div>

      <v-col cols="12" md="6" class="d-flex justify-end">
        <v-card @click="checkAnswer(options[0].correct)" class="text-center bg-grey" width="350px">
          <v-card-title>Test</v-card-title>
          <v-card-text>
            subtitle
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" class="d-flex justify-start">
        <v-card @click="checkAnswer(options[1].correct)" class="text-center bg-grey" width="350px">
          <v-card-title>Test</v-card-title>
          <v-card-text>
            subtitle
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" class="d-flex justify-end">
        <v-card @click="checkAnswer(options[2].correct)" class="text-center bg-grey" width="350px">
          <v-card-title>Test</v-card-title>
          <v-card-text>
            subtitle
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" class="d-flex justify-start">
        <v-card @click="checkAnswer(options[3].correct)" class="text-center bg-grey" width="350px">
          <v-card-title>Test</v-card-title>
          <v-card-text>
            subtitle
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, Ref, defineProps } from 'vue';
import { getImageUrl } from '@/api/images';

const answerState: Ref<string | null> = ref(null);
const options: Ref<{ text: string; subtext: string; correct: boolean }[]> = ref([
  { text: 'Example text', subtext: 'example sub text', correct: false },
  { text: 'Example text', subtext: 'example sub text', correct: true },
  { text: 'Example text', subtext: 'example sub text', correct: false },
  { text: 'Example text', subtext: 'example sub text', correct: false },
]);

defineProps<{
  imageId: number
  options: number[]
}>()

function checkAnswer(isCorrect: boolean) {
  answerState.value = isCorrect ? 'correct' : 'wrong';
  // Add logic here for feedback or scoring if necessary
}
</script>

<style scoped>
.v-card {
  /* cursor: pointer; */
  transition: transform 0.3s;
}

.v-card:hover {
  transform: scale(1.02);
}
</style>
