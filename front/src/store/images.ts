// Utilities
import { defineStore } from 'pinia'
import { Ref, ref } from 'vue'
import { ImageInfo } from '@/types/images'
import { BirdInfo } from '@/types/birds'
import { getImageBird } from '@/api/images'

export const useImagesStore = defineStore('images', () => {
  const imageInfo: Ref<ImageInfo> = ref({})

  function setImageInfo(imgId: number, lang: string, info: BirdInfo) {
    if (!(imgId in imageInfo.value)) {
      imageInfo.value[imgId] = {}
    }
    imageInfo.value[imgId][lang] = info
  }

  function imageInfoExists(imgId: number, lang: string): boolean {
    if (!(imgId in imageInfo.value) || !(lang in imageInfo.value[imgId])) {
      return false
    }
    return true
  }

  // async function getImageInfo(imgId: number, lang: string): Promise<BirdInfo | null> {
  //   if (!(imgId in imageInfo.value)) {
  //     imageInfo.value[imgId] = {}
  //   }
  //   if (!(lang in imageInfo.value[imgId])) {
  //     const res = await getImageBird(imgId, lang)
  //     if (res.status != 200) {
  //       return null
  //     }
  //     setImageInfo(imgId, lang, res.data)
  //   }
  //   return imageInfo.value[imgId][lang]
  // }
  function getImageInfo(imgId: number, lang: string): BirdInfo | null {
    if (!(imgId in imageInfo.value) || !(lang in imageInfo.value[imgId])) {
      return null
    }
    return imageInfo.value[imgId][lang]
  }

  async function fetchImageInfo(imgIds: number[], lang: string) {
    for (const i of imgIds) {
      if (imageInfoExists(i, lang)) {
        continue
      }
      const res = await getImageBird(i, lang)
      if (res.status != 200) {
        return null
      }
      setImageInfo(i, lang, res.data)
    }
  }

  return { getImageInfo, fetchImageInfo }
})
