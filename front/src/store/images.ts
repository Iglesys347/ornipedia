// Utilities
import { defineStore } from 'pinia'
import { Ref, ref } from 'vue'
import { ImageInfo, ImagesInfo } from '@/types/images'
import { getImageInfo as apiGetImageInfo } from '@/api/images'

export const useImagesStore = defineStore('images', () => {
  const imagesInfo: Ref<ImagesInfo> = ref({})

  function setImageInfo(imgId: number, lang: string, info: ImageInfo) {
    if (!(imgId in imagesInfo.value)) {
      imagesInfo.value[imgId] = {}
    }
    imagesInfo.value[imgId][lang] = info
  }

  function imageInfoExists(imgId: number, lang: string): boolean {
    if (!(imgId in imagesInfo.value) || !(lang in imagesInfo.value[imgId])) {
      return false
    }
    return true
  }

  function getImageInfo(imgId: number, lang: string): ImageInfo | null {
    if (!(imgId in imagesInfo.value) || !(lang in imagesInfo.value[imgId])) {
      return null
    }
    return imagesInfo.value[imgId][lang]
  }

  // the missing information is fetched in parallel, an image whose information
  // cannot be fetched is simply left without information
  async function fetchImageInfo(imgIds: number[], lang: string) {
    const missing = imgIds.filter(i => !imageInfoExists(i, lang))
    const results = await Promise.all(missing.map(i => apiGetImageInfo(i, lang).catch(() => null)))
    results.forEach((res, index) => {
      if (res && res.status == 200) {
        setImageInfo(missing[index], lang, res.data)
      }
    })
  }

  return { getImageInfo, fetchImageInfo }
})
