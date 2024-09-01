// Utilities
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useTheme, useLocale } from 'vuetify'

export const useAppStore = defineStore('app', () => {
  const theme = useTheme()
  function getTheme() {
    return theme.global.name.value
  }
  function switchTheme() {
    theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  }

  const showNavBar = ref(false)
  function switchNavBar() {
    showNavBar.value = !showNavBar.value
  }

  const { current } = useLocale()
  const locale = current
  function changeLocale(locale: string) {
    current.value = locale
  }

  return { theme, switchTheme, getTheme, locale, changeLocale, showNavBar, switchNavBar }
})