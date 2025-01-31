export type Image = {
    id: number
    bird_id: number
}

export type PaginatedSpecies = {
    total: number
    page: number
    per_page: number
    items: string[]
}

export type Quiz = {
    quiz_id: string
    quiz_image: number
    options: number[]
}
