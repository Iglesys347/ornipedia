import instance from "./axios_instance"
import { PaginatedGroups } from "./types"

export function getGroups(lang: string, page: number = 1, perPage: number = 25) {
    return instance.get<PaginatedGroups>(`/groups`, { params: { language: lang, page: page, per_page: perPage } })
}

export function getSubgroups(lang: string, group: string, page: number = 1, perPage: number = 25) {
    return instance.get<PaginatedGroups>(`/groups/${encodeURIComponent(group)}`, { params: { language: lang, page: page, per_page: perPage } })
}
