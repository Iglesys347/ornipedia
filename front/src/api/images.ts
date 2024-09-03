import instance from "./axios_instance"

export function getImages(
    lang: string | null = null,
    species: string | null = null, subSpecies: string | null = null, search: string = "",
    page: number | null = null, perPage: number | null = null
) {
    return instance.get("/images", { params: { language: lang, species: species, sub_species: subSpecies, search: search, page: page, per_page: perPage } })
}

export function getImageUrl(imgId: number) {
    return `${instance.getUri()}/images/${imgId}`
}

export function getImageInfo(imgId: number, lang: string) {
    return instance.get(`/images/${imgId}/info`, { params: { language: lang } })
}

export function getRandomImage(species: string | null = null, subSpecies: string | null = null) {
    return instance.get(`images/image/random`, { params: { species: species, sub_species: subSpecies } })
}
