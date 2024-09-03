import instance from "./axios_instance"
import { PaginatedSpecies } from "./types"

export function getSpecies(lang: string, page: number = 1, perPage: number = 25) {
    return instance.get<PaginatedSpecies>(`/species`, { params: { language: lang, page: page, per_page: perPage } })
}

export function getSubSpecies(lang: string, species: string, page: number = 1, perPage: number = 25) {
    return instance.get<PaginatedSpecies>(`/species/${species}`, { params: { language: lang, page: page, per_page: perPage } })
}
