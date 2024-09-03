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

  async function fetchImageInfo(imgIds: number[], lang: string) {
    for (const i of imgIds) {
      if (imageInfoExists(i, lang)) {
        continue
      }
      const res = await apiGetImageInfo(i, lang)
      if (res.status != 200) {
        return null
      }
      setImageInfo(i, lang, res.data)
    }
  }

  return { getImageInfo, fetchImageInfo }
})
