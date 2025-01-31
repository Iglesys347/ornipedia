import instance from "./axios_instance"
import { Quiz } from "./types"

export function getQuiz(lang: string | null = null, species: string | null = null, subSpecies: string | null = null) {
    return instance.get<Quiz>(`/quiz`, { params: { language: lang, species: species, sub_species: subSpecies } })
}
