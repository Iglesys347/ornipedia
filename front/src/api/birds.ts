import instance from "./axios_instance"
import { MAX_PER_PAGE } from "./types"

export type BirdSummary = {
    id: number
    latin_name: string
    name: string
    species: string
    sub_species: string
}

export function getBirds(lang: string, page = 1, perPage = 25) {
    return instance.get<{ items: BirdSummary[], total: number }>("/birds", {
        params: { language: lang, page: page, per_page: perPage },
    })
}

// all the birds having a translation in this language
export async function getAllBirds(lang: string): Promise<BirdSummary[]> {
    const birds: BirdSummary[] = []
    for (let page = 1; ; page++) {
        const res = await getBirds(lang, page, MAX_PER_PAGE)
        birds.push(...res.data.items)
        if (res.data.items.length == 0 || birds.length >= res.data.total) {
            return birds
        }
    }
}
