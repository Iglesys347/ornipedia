// Utilities
import { defineStore } from 'pinia'
import { Ref, ref } from 'vue'
import { getGroups as apiGetGroups, getSubgroups as apiGetSubgroups } from '@/api/groups';


export const useGroupsStore = defineStore('groups', () => {
  const groups: Ref<{ [id: string]: string[] }> = ref({})


  async function getGroups(lang: string): Promise<string[]> {
    if (!groups.value[lang] || groups.value[lang].length == 0) {
      await fetchGroups(lang)
    }

    return groups.value[lang]
  }

  async function fetchGroups(lang: string) {
    groups.value[lang] = []
    // looping to retrieve all the groups
    let nextPage = true
    let page = 1
    while (nextPage) {
      const res = await apiGetGroups(lang, page)
      if (res.status != 200) {
        return null
      }
      groups.value[lang] = groups.value[lang].concat(res.data.items)
      if (res.data.items.length == 0 || groups.value[lang].length >= res.data.total) {
        nextPage = false
      }
      page += 1
    }
  }


  // subgroups are cached by language and group
  const subgroups: Ref<{ [id: string]: string[] }> = ref({})

  async function getSubgroups(lang: string, group: string): Promise<string[]> {
    const key = `${lang}:${group}`
    if (!subgroups.value[key] || subgroups.value[key].length == 0) {
      await fetchSubgroups(lang, group)
    }

    return subgroups.value[key]
  }

  async function fetchSubgroups(lang: string, group: string) {
    const key = `${lang}:${group}`
    subgroups.value[key] = []
    // looping to retrieve all the subgroups
    let nextPage = true
    let page = 1
    while (nextPage) {
      const res = await apiGetSubgroups(lang, group, page)
      if (res.status != 200) {
        return null
      }
      subgroups.value[key] = subgroups.value[key].concat(res.data.items)
      if (res.data.items.length == 0 || subgroups.value[key].length >= res.data.total) {
        nextPage = false
      }
      page += 1
    }
  }


  // to call when a bird is added (its group may be new)
  function clear() {
    groups.value = {}
    subgroups.value = {}
  }

  return { getGroups, getSubgroups, clear }
})
