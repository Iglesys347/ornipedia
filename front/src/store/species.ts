// Utilities
import { defineStore } from 'pinia'
import { Ref, ref } from 'vue'
import { getSpecies as apiGetSpecies, getSubSpecies as apiGetSubSpecies } from '@/api/species';


export const useSpeciesStore = defineStore('species', () => {
  const species: Ref<{ [id: string]: string[] }> = ref({})


  async function getSpecies(lang: string): Promise<string[]> {
    if (!species.value[lang] || species.value[lang].length == 0) {
      await fetchSpecies(lang)
    }

    return species.value[lang]
  }

  async function fetchSpecies(lang: string) {
    species.value[lang] = []
    // looping to retrieve all the species
    let nextPage = true
    let page = 1
    while (nextPage) {
      const res = await apiGetSpecies(lang, page)
      if (res.status != 200) {
        return null
      }
      species.value[lang] = species.value[lang].concat(res.data.items)
      if (res.data.items.length == 0 || species.value[lang].length >= res.data.total) {
        nextPage = false
      }
      page += 1
    }
  }


  // sub-species are cached by language and species
  const subSpecies: Ref<{ [id: string]: string[] }> = ref({})

  async function getSubSpecies(lang: string, species: string): Promise<string[]> {
    const key = `${lang}:${species}`
    if (!subSpecies.value[key] || subSpecies.value[key].length == 0) {
      await fetchSubSpecies(lang, species)
    }

    return subSpecies.value[key]
  }

  async function fetchSubSpecies(lang: string, species: string) {
    const key = `${lang}:${species}`
    subSpecies.value[key] = []
    // looping to retrieve all the sub-species
    let nextPage = true
    let page = 1
    while (nextPage) {
      const res = await apiGetSubSpecies(lang, species, page)
      if (res.status != 200) {
        return null
      }
      subSpecies.value[key] = subSpecies.value[key].concat(res.data.items)
      if (res.data.items.length == 0 || subSpecies.value[key].length >= res.data.total) {
        nextPage = false
      }
      page += 1
    }
  }


  // to call when a bird is added (its species may be new)
  function clear() {
    species.value = {}
    subSpecies.value = {}
  }

  return { getSpecies, getSubSpecies, clear }
})
