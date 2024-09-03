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


  const subSpecies: Ref<{ [id: string]: string[] }> = ref({})

  async function getSubSpecies(lang: string, species: string): Promise<string[]> {
    if (!subSpecies.value[lang] || subSpecies.value[lang].length == 0) {
      await fetchSubSpecies(lang, species)
    }

    return subSpecies.value[lang]
  }

  async function fetchSubSpecies(lang: string, species: string) {
    if (!subSpecies.value[lang]) {
      subSpecies.value[lang] = []
    }
    // looping to retrieve all the species
    let nextPage = true
    let page = 1
    while (nextPage) {
      const res = await apiGetSubSpecies(lang, species, page)
      if (res.status != 200) {
        return null
      }
      subSpecies.value[lang] = subSpecies.value[lang].concat(res.data.items)
      if (subSpecies.value[lang].length == res.data.total) {
        nextPage = false
      }
      page += 1
    }
  }


  return { getSpecies, getSubSpecies }
})
