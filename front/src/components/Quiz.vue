<template>
  <v-container class="quiz py-6" :class="{ 'quiz-playing': phase == 'playing' }">
    <!-- settings of the game -->
    <template v-if="phase == 'setup'">
      <h1 class="text-h4 mb-1">{{ $t("quiz.title") }}</h1>
      <p class="text-body-1 text-medium-emphasis mb-6">{{ $t("quiz.intro") }}</p>

      <h2 class="text-h6 mb-3">{{ $t("quiz.setup.format") }}</h2>
      <v-row class="mb-4">
        <v-col v-for="item in formats" :key="item.value" cols="12" sm="4">
          <v-card :variant="format == item.value ? 'flat' : 'outlined'"
            :color="format == item.value ? 'primary' : undefined" class="fill-height" role="radio"
            :aria-checked="format == item.value" @click="format = item.value">
            <v-card-item :prepend-icon="item.icon">
              <v-card-title class="text-wrap">{{ $t(`quiz.format.${item.value}.title`) }}</v-card-title>
            </v-card-item>
            <v-card-text>{{ $t(`quiz.format.${item.value}.desc`) }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mb-6">
        <v-col cols="12" sm="6">
          <h2 class="text-h6 mb-3">{{ $t("quiz.setup.difficulty") }}</h2>
          <v-btn-toggle v-model="difficulty" mandatory color="primary" variant="outlined" divided>
            <v-btn value="easy" prepend-icon="mdi-feather">{{ $t("quiz.difficulty.easy.title") }}</v-btn>
            <v-btn value="hard" prepend-icon="mdi-bird">{{ $t("quiz.difficulty.hard.title") }}</v-btn>
          </v-btn-toggle>
          <p class="text-body-2 text-medium-emphasis mt-2">{{ $t(`quiz.difficulty.${difficulty}.desc`) }}</p>
        </v-col>
        <v-col cols="12" sm="6">
          <h2 class="text-h6 mb-3">{{ $t("quiz.setup.length") }}</h2>
          <v-btn-toggle v-model="length" mandatory color="primary" variant="outlined" divided>
            <v-btn v-for="n in LENGTHS" :key="n" :value="n">{{ n }}</v-btn>
          </v-btn-toggle>
        </v-col>
      </v-row>

      <v-alert v-if="error" type="warning" variant="tonal" class="mb-4">{{ error }}</v-alert>
      <v-btn color="primary" variant="flat" size="large" append-icon="mdi-arrow-right" :loading="loading"
        @click="start">
        {{ $t("quiz.setup.start") }}
      </v-btn>
    </template>

    <!-- a question -->
    <template v-else-if="phase == 'playing'">
      <div class="d-flex align-center flex-wrap ga-2 mb-2">
        <span class="text-subtitle-1 font-weight-medium">
          {{ $t("quiz.progress", { n: answers.length + (answered ? 0 : 1), total: length }) }}
        </span>
        <v-chip size="small" variant="tonal" color="primary" prepend-icon="mdi-star-outline">
          {{ $t("quiz.score", { score }) }}
        </v-chip>
        <v-spacer></v-spacer>
        <v-btn variant="text" size="small" prepend-icon="mdi-close" @click="quit">{{ $t("quiz.quit") }}</v-btn>
      </div>
      <v-progress-linear :model-value="100 * answers.length / length" color="primary" rounded class="mb-6"
        :aria-label="$t('quiz.progress', { n: answers.length, total: length })"></v-progress-linear>

      <v-alert v-if="error" type="warning" variant="tonal" class="mb-4">
        {{ error }}
        <template v-slot:append>
          <v-btn variant="text" @click="loadQuestion">{{ $t("quiz.retry") }}</v-btn>
        </template>
      </v-alert>

      <template v-if="question && answer">
        <!-- photo -> name: which bird is it? -->
        <template v-if="kind == 'photo'">
          <h2 class="text-h5 mb-4">{{ $t("quiz.question.photo") }}</h2>
          <figure class="mb-4">
            <v-img :key="answer.image.id" :src="getImageUrl(answer.image.id, 1280)"
              :srcset="getImageSrcset(answer.image.id, [640, 1280])" sizes="(max-width: 959px) 100vw, 900px"
              :alt="$t('quiz.question.photo_alt')" class="question-photo rounded-xl" height="min(50vh, 480px)">
              <template v-slot:placeholder>
                <div class="photo-placeholder fill-height d-flex align-center justify-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </div>
              </template>
            </v-img>
            <figcaption class="text-caption text-medium-emphasis credits mt-1 text-center">
              <PhotoCredits :choice="answer"></PhotoCredits>
            </figcaption>
          </figure>
          <v-row dense>
            <v-col v-for="(choice, index) in question.choices" :key="choice.bird_id" cols="12" sm="6">
              <v-btn block size="x-large" class="choice text-none" :variant="choiceVariant(choice)"
                :color="choiceColor(choice)" :prepend-icon="choiceIcon(choice)"
                :class="{ 'not-chosen': answered && !isRevealed(choice) }"
                :aria-keyshortcuts="String(index + 1)" @click="choose(choice)">
                <span class="text-wrap">{{ capitalize(choice.name) }}</span>
              </v-btn>
            </v-col>
          </v-row>
        </template>

        <!-- name -> photo: where is the bird? -->
        <template v-else>
          <h2 class="text-h5 mb-1">{{ $t("quiz.question.name") }}</h2>
          <p class="text-h4 font-weight-medium mb-4 text-primary">{{ capitalize(answer.name) }}</p>
          <v-row dense class="photo-grid">
            <v-col v-for="(choice, index) in question.choices" :key="choice.bird_id" cols="6">
              <v-card class="photo-choice" :class="choiceBorder(choice)" rounded="xl"
                :aria-label="$t('quiz.question.photo_choice', { n: index + 1 })"
                :aria-keyshortcuts="String(index + 1)" @click="choose(choice)">
                <v-img :src="getImageUrl(choice.image.id, 640)" :srcset="getImageSrcset(choice.image.id)"
                  sizes="(max-width: 959px) 50vw, 450px" :aspect-ratio="4 / 3" cover
                  :alt="answered ? capitalize(choice.name) : $t('quiz.question.photo_choice', { n: index + 1 })">
                  <template v-slot:placeholder>
                    <div class="photo-placeholder fill-height"></div>
                  </template>
                  <div v-if="answered && isRevealed(choice)" class="d-flex justify-end pa-2">
                    <v-icon :color="choiceColor(choice)" class="result-icon" size="32">{{ choiceIcon(choice)
                      }}</v-icon>
                  </div>
                </v-img>
                <div class="pa-2">
                  <!-- the names are shown after the answer, to learn the other birds too -->
                  <div class="text-body-2 text-sm-subtitle-1 font-weight-medium text-truncate">
                    {{ answered ? capitalize(choice.name) : "\u00a0" }}
                  </div>
                  <div class="text-caption text-medium-emphasis text-truncate credits">
                    <PhotoCredits :choice="choice"></PhotoCredits>
                  </div>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </template>

        <!-- result of the answer -->
        <div v-if="answered" class="feedback d-flex align-center flex-wrap ga-4 pa-4 mt-4 rounded-xl"
          :class="lastAnswer?.correct ? 'feedback-correct' : 'feedback-wrong'" aria-live="polite">
          <div class="flex-grow-1">
            <div class="text-h6 d-flex align-center ga-2">
              <v-icon :color="lastAnswer?.correct ? 'success' : 'error'">
                {{ lastAnswer?.correct ? "mdi-check-circle" : "mdi-close-circle" }}
              </v-icon>
              {{ lastAnswer?.correct ? $t("quiz.feedback.correct") : $t("quiz.feedback.wrong") }}
            </div>
            <div class="text-body-1">
              {{ $t("quiz.feedback.it_was") }}
              <strong>{{ capitalize(answer.name) }}</strong>
              <span class="font-italic"> ({{ answer.latin_name }})</span>
            </div>
          </div>
          <v-btn ref="nextButton" color="primary" variant="flat" size="large" append-icon="mdi-arrow-right"
            :loading="loading" @click="next">
            {{ answers.length >= length ? $t("quiz.see_result") : $t("quiz.next") }}
          </v-btn>
        </div>
        <p v-else class="text-caption text-medium-emphasis mt-4 d-none d-md-block">{{ $t("quiz.keyboard_hint") }}</p>
      </template>

      <div v-else-if="loading" class="d-flex justify-center py-12">
        <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
      </div>
    </template>

    <!-- result of the game -->
    <template v-else>
      <v-card class="text-center pa-6 mb-6" variant="tonal" color="primary" rounded="xl">
        <div class="text-h2 font-weight-light">{{ score }} / {{ answers.length }}</div>
        <div class="text-h6 mt-2">{{ $t(resultMessage) }}</div>
        <div class="text-body-2 text-medium-emphasis mt-1">
          {{ $t(`quiz.format.${format}.title`) }} · {{ $t(`quiz.difficulty.${difficulty}.title`) }}
        </div>
        <div class="d-flex justify-center flex-wrap ga-3 mt-6">
          <v-btn color="primary" variant="flat" prepend-icon="mdi-replay" :loading="loading" @click="start">
            {{ $t("quiz.play_again") }}
          </v-btn>
          <v-btn variant="outlined" prepend-icon="mdi-tune-variant" @click="quit">{{ $t("quiz.change_settings") }}</v-btn>
        </div>
      </v-card>

      <h2 class="text-h6 mb-3">{{ $t("quiz.review") }}</h2>
      <v-list lines="two" class="review bg-transparent">
        <v-list-item v-for="(item, index) in answers" :key="index" :to="{ path: '/birds', query: { q: item.answer.name } }">
          <template v-slot:prepend>
            <v-avatar size="56" rounded="lg" class="me-2">
              <v-img :src="getImageUrl(item.answer.image.id, 320)" cover :alt="capitalize(item.answer.name)"></v-img>
            </v-avatar>
          </template>
          <v-list-item-title>{{ capitalize(item.answer.name) }}
            <span class="text-medium-emphasis font-italic text-body-2">{{ item.answer.latin_name }}</span>
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ item.correct ? $t("quiz.feedback.correct") : $t("quiz.your_answer", { name: capitalize(item.chosen.name) })
            }}
          </v-list-item-subtitle>
          <template v-slot:append>
            <v-icon :color="item.correct ? 'success' : 'error'"
              :aria-label="item.correct ? $t('quiz.feedback.correct') : $t('quiz.feedback.wrong')">
              {{ item.correct ? "mdi-check-circle" : "mdi-close-circle" }}
            </v-icon>
          </template>
        </v-list-item>
      </v-list>
    </template>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ComponentPublicInstance, defineComponent, h, nextTick, onBeforeUnmount, onMounted, ref, Ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { isAxiosError } from 'axios';
import { getImageSrcset, getImageUrl } from '@/api/images';
import { getQuizQuestion, QuizChoice, QuizDifficulty, QuizQuestion } from '@/api/quiz';
import { useAppStore } from '@/store/app';

type QuizFormat = "photo" | "name" | "mixed"
type QuestionKind = "photo" | "name"
type Answer = { answer: QuizChoice, chosen: QuizChoice, correct: boolean }

const { t } = useI18n()
const appStore = useAppStore()

const LENGTHS = [5, 10, 20]
const SETTINGS_KEY = "ornipedia.quiz"
const formats: { value: QuizFormat, icon: string }[] = [
  { value: "photo", icon: "mdi-image-search-outline" },
  { value: "name", icon: "mdi-view-grid-outline" },
  { value: "mixed", icon: "mdi-shuffle-variant" },
]

// settings, the last ones are kept for the next visit
const format: Ref<QuizFormat> = ref("photo")
const difficulty: Ref<QuizDifficulty> = ref("easy")
const length = ref(10)
try {
  const saved = JSON.parse(window.localStorage.getItem(SETTINGS_KEY) ?? "{}")
  if (formats.some(f => f.value == saved.format)) format.value = saved.format
  if (saved.difficulty == "easy" || saved.difficulty == "hard") difficulty.value = saved.difficulty
  if (LENGTHS.includes(saved.length)) length.value = saved.length
} catch {
  // default settings
}
watch([format, difficulty, length], () => {
  try {
    window.localStorage.setItem(SETTINGS_KEY, JSON.stringify(
      { format: format.value, difficulty: difficulty.value, length: length.value }))
  } catch {
    // the settings are only kept for the current visit
  }
})

const phase: Ref<"setup" | "playing" | "finished"> = ref("setup")
const question: Ref<QuizQuestion | null> = ref(null)
const kind: Ref<QuestionKind> = ref("photo")
const answers: Ref<Answer[]> = ref([])
const answered = ref(false)
const loading = ref(false)
const error = ref("")
// the next question is loaded while the current one is answered
let nextQuestion: Promise<QuizQuestion> | null = null

const answer = computed(() => question.value?.choices.find(c => c.bird_id == question.value?.answer_id) ?? null)
const lastAnswer = computed(() => answers.value[answers.value.length - 1] ?? null)
const score = computed(() => answers.value.filter(a => a.correct).length)
const resultMessage = computed(() => {
  const ratio = answers.value.length ? score.value / answers.value.length : 0
  if (ratio == 1) return "quiz.result.perfect"
  if (ratio >= 0.7) return "quiz.result.good"
  if (ratio >= 0.4) return "quiz.result.average"
  return "quiz.result.bad"
})

function capitalize(str: string) {
  return str ? str[0].toUpperCase() + str.slice(1) : str
}

// the photos are downloaded before the question is shown
function preload(q: QuizQuestion, questionKind: QuestionKind) {
  const ids = questionKind == "photo"
    ? [q.choices.find(c => c.bird_id == q.answer_id)?.image.id]
    : q.choices.map(c => c.image.id)
  for (const id of ids) {
    if (id !== undefined) {
      new Image().src = getImageUrl(id, questionKind == "photo" ? 1280 : 640)
    }
  }
}

function drawKind(): QuestionKind {
  if (format.value == "mixed") {
    return Math.random() < 0.5 ? "photo" : "name"
  }
  return format.value
}
let upcomingKind: QuestionKind = "photo"

function fetchQuestion(): Promise<QuizQuestion> {
  // the birds already asked (the current one included) are not asked again
  const asked = new Set(answers.value.map(a => a.answer.bird_id))
  if (question.value) asked.add(question.value.answer_id)
  upcomingKind = drawKind()
  const kindOfQuestion = upcomingKind
  return getQuizQuestion(appStore.locale, difficulty.value, [...asked]).then(response => {
    preload(response.data, kindOfQuestion)
    return response.data
  })
}

function errorMessage(err: unknown) {
  if (isAxiosError(err) && err.response?.status == 404) {
    return t("quiz.error.not_enough")
  }
  return t("quiz.error.load")
}

async function loadQuestion() {
  loading.value = true
  error.value = ""
  try {
    const pending = nextQuestion ?? fetchQuestion()
    nextQuestion = null
    const q = await pending
    kind.value = upcomingKind
    question.value = q
    answered.value = false
    phase.value = "playing"
  } catch (err) {
    nextQuestion = null
    error.value = errorMessage(err)
  } finally {
    loading.value = false
  }
}

function start() {
  answers.value = []
  question.value = null
  nextQuestion = null
  loadQuestion()
}

const nextButton: Ref<ComponentPublicInstance | null> = ref(null)

function choose(choice: QuizChoice) {
  if (answered.value || !answer.value) return
  answered.value = true
  answers.value.push({ answer: answer.value, chosen: choice, correct: choice.bird_id == answer.value.bird_id })
  // Enter (or Space) goes to the next question, the result is announced with the button
  nextTick(() => (nextButton.value?.$el as HTMLElement | undefined)?.focus({ preventScroll: true }))
  if (answers.value.length < length.value) {
    nextQuestion = fetchQuestion()
    // an error is shown when the question is needed
    nextQuestion.catch(() => undefined)
  }
}

function next() {
  if (answers.value.length >= length.value) {
    phase.value = "finished"
    question.value = null
    window.scrollTo({ top: 0 })
    return
  }
  loadQuestion().then(() => window.scrollTo({ top: 0 }))
}

function quit() {
  phase.value = "setup"
  question.value = null
  nextQuestion = null
  error.value = ""
}

// the choices once answered: the right one, and the wrong one chosen
function isRevealed(choice: QuizChoice) {
  return choice.bird_id == question.value?.answer_id || choice.bird_id == lastAnswer.value?.chosen.bird_id
}
function choiceColor(choice: QuizChoice) {
  if (!answered.value) return undefined
  if (choice.bird_id == question.value?.answer_id) return "success"
  if (choice.bird_id == lastAnswer.value?.chosen.bird_id) return "error"
  return undefined
}
function choiceVariant(choice: QuizChoice) {
  return answered.value && isRevealed(choice) ? "flat" : "outlined"
}
function choiceIcon(choice: QuizChoice) {
  if (!answered.value) return undefined
  if (choice.bird_id == question.value?.answer_id) return "mdi-check-circle"
  if (choice.bird_id == lastAnswer.value?.chosen.bird_id) return "mdi-close-circle"
  return undefined
}
function choiceBorder(choice: QuizChoice) {
  const color = choiceColor(choice)
  return color ? `border-${color}` : answered.value ? "not-chosen" : ""
}

// keys 1 to 4 choose an answer, Enter goes to the next question
function onKeydown(event: KeyboardEvent) {
  if (phase.value != "playing" || !question.value || event.altKey || event.ctrlKey || event.metaKey) return
  const target = event.target as HTMLElement | null
  if (target && ["INPUT", "TEXTAREA"].includes(target.tagName)) return
  const index = Number(event.key) - 1
  if (!answered.value && index >= 0 && index < question.value.choices.length) {
    choose(question.value.choices[index])
  }
}
onMounted(() => window.addEventListener("keydown", onKeydown))
onBeforeUnmount(() => window.removeEventListener("keydown", onKeydown))

// a new language: the names of the current game are no longer right
watch(() => appStore.locale, () => {
  if (phase.value == "playing") quit()
})

// credits of a photo (free licenses), links open in a new tab
const PhotoCredits = defineComponent({
  props: { choice: { type: Object as () => QuizChoice, required: true } },
  setup(props) {
    return () => {
      const { author, license } = props.choice.image
      const link = (href: string | null, text: string) => href
        ? h("a", { href, target: "_blank", rel: "noopener", onClick: (e: Event) => e.stopPropagation() }, text)
        : text
      return h("span", [
        `${t("photo.credit")} `,
        link(author.link, author.name || t("quiz.unknown_author")),
        " · ",
        link(license.link, license.short_name),
      ])
    }
  },
})
</script>

<style scoped>
.quiz {
  max-width: 960px;
}

.question-photo {
  background: rgba(var(--v-theme-on-surface), 0.06);
}

.photo-placeholder {
  background: rgba(var(--v-theme-on-surface), 0.08);
}

.choice {
  height: auto !important;
  min-height: 56px;
  padding-top: 8px;
  padding-bottom: 8px;
  justify-content: flex-start;
}

/* the question, the photos and the result fit on a laptop screen */
.photo-grid {
  max-width: 640px;
  margin-left: auto;
  margin-right: auto;
}

.feedback-correct {
  background: rgba(var(--v-theme-success), 0.14);
}

.feedback-wrong {
  background: rgba(var(--v-theme-error), 0.12);
}

.not-chosen {
  opacity: 0.6;
}

.photo-choice {
  border: 3px solid transparent;
  overflow: hidden;
}

.photo-choice.border-success {
  border-color: rgb(var(--v-theme-success));
}

.photo-choice.border-error {
  border-color: rgb(var(--v-theme-error));
}

.result-icon {
  background: rgb(var(--v-theme-surface));
  border-radius: 50%;
}

/* the links are rendered by PhotoCredits */
.credits :deep(a) {
  color: inherit;
}
</style>
