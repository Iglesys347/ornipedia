import instance from "./axios_instance"

export type QuizDifficulty = "easy" | "hard"

export type QuizChoice = {
    bird_id: number
    name: string
    latin_name: string
    group: string
    subgroup: string | null
    // a photo of the bird, with its credits
    image: {
        id: number
        author: { name: string | null, link: string | null }
        license: { short_name: string, full_name: string, link: string }
    }
}

export type QuizQuestion = {
    // the bird to find, one of the choices
    answer_id: number
    choices: QuizChoice[]
}

// a question with up to 4 choices, the birds in `exclude` are not asked while possible
export function getQuizQuestion(lang: string, difficulty: QuizDifficulty, exclude: number[] = []) {
    return instance.get<QuizQuestion>("/quiz/question", {
        params: { language: lang, difficulty: difficulty, exclude: exclude },
        // `exclude=1&exclude=2` (and not `exclude[]=1...`)
        paramsSerializer: { indexes: null },
    })
}
