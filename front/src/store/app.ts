// Utilities
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useLocale } from 'vuetify'

export const useAppStore = defineStore('app', () => {
  const theme = ref("light")
  function getTheme() {
    return theme.value
  }
  function switchTheme() {
    theme.value = theme.value == "dark" ? "light" : "dark"
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