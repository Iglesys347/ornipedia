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

// maximum page size accepted by the API
export const MAX_PER_PAGE = 100
