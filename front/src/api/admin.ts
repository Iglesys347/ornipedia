import type { AxiosProgressEvent } from "axios"
import instance from "./axios_instance"

// calls of the administration, authenticated with the admin password

export type TranslationIn = {
    language_code: string
    name: string
    species: string
    sub_species: string | null
    details: string | null
}

export type Author = { id: number, name: string | null, link: string | null }
export type License = { id: number, short_name: string, full_name: string, link: string }

export type PhotoForm = {
    author_name: string
    author_link: string
    license_short_name: string
    license_full_name: string
    license_link: string
    original_url: string
}

function auth(password: string) {
    return { headers: { Authorization: `Bearer ${password}` } }
}

export function checkPassword(password: string) {
    return instance.get("/admin/check", auth(password))
}

export function getAuthors(password: string) {
    return instance.get<Author[]>("/admin/authors", auth(password))
}

export function getLicenses(password: string) {
    return instance.get<License[]>("/admin/licenses", auth(password))
}

export function createBird(password: string, latinName: string, translations: TranslationIn[]) {
    return instance.post<{ id: number, latin_name: string }>(
        "/admin/birds", { latin_name: latinName, translations }, auth(password))
}

export function uploadPhoto(password: string, birdId: number, file: File, form: PhotoForm,
    onProgress: (percent: number) => void) {
    const data = new FormData()
    data.append("file", file)
    for (const [key, value] of Object.entries(form)) {
        data.append(key, value)
    }
    return instance.post<{ id: number, bird_id: number }>(`/admin/birds/${birdId}/images`, data, {
        ...auth(password),
        onUploadProgress: (event: AxiosProgressEvent) => {
            if (event.total) {
                onProgress(Math.round(100 * event.loaded / event.total))
            }
        },
    })
}

export function deletePhoto(password: string, imgId: number) {
    return instance.delete(`/admin/images/${imgId}`, auth(password))
}
