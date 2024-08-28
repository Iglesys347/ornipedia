// Utilities
import { defineStore } from 'pinia'
import { Ref, ref } from 'vue'
import { getSpecies as apiGetSpecies } from '@/api/species';


export const useSpeciesStore = defineStore('species', () => {
  const species: Ref<{ [id: string]: string[] }> = ref({})


  async function getSpecies(lang: string): Promise<string[]> {
    if (!species.value[lang] || species.value[lang].length == 0) {
      await fetchSpecies(lang)
    }
    return species.value[lang]
  }

  async function fetchSpecies(lang: string) {
    if (!species.value[lang]) {
      species.value[lang] = []
    }
    // looping to retrieve all the species
    let nextPage = true
    let page = 1
    while (nextPage) {
      const res = await apiGetSpecies(lang, page)
      if (res.status != 200) {
        return null
      }
      species.value[lang] = species.value[lang].concat(res.data.items)
      if (species.value[lang].length == res.data.total) {
        nextPage = false
      }
      page += 1
    }
  }

  return { getSpecies }
})
