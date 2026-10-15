// Utilities
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useTheme, useLocale } from 'vuetify'
import { supportedLanguages } from '@/translations/i18n'

const THEME_KEY = 'ornipedia.theme'
const LOCALE_KEY = 'ornipedia.locale'

// the storage may be unavailable (private browsing, blocked cookies...)
function readPreference(key: string): string | null {
  try {
    return window.localStorage.getItem(key)
  } catch {
    return null
  }
}

function writePreference(key: string, value: string) {
  try {
    window.localStorage.setItem(key, value)
  } catch {
    // the preference is only kept for the current visit
  }
}

function isSupportedLocale(locale: string | null): locale is string {
  return supportedLanguages.some(l => l.code == locale)
}

// saved choice, then language of the browser, then english
function initialLocale(): string {
  const saved = readPreference(LOCALE_KEY)
  if (isSupportedLocale(saved)) {
    return saved
  }
  for (const language of navigator.languages ?? [navigator.language]) {
    const code = language.split('-')[0].toLowerCase()
    if (isSupportedLocale(code)) {
      return code
    }
  }
  return 'en'
}

// saved choice, then theme of the system
function initialTheme(): string {
  const saved = readPreference(THEME_KEY)
  if (saved == 'light' || saved == 'dark') {
    return saved
  }
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export const useAppStore = defineStore('app', () => {
  const theme = useTheme()
  function getTheme() {
    return theme.global.name.value
  }
  function setTheme(name: string) {
    theme.global.name.value = name
    writePreference(THEME_KEY, name)
  }

  const showNavBar = ref(false)
  function switchNavBar() {
    showNavBar.value = !showNavBar.value
  }

  const { current } = useLocale()
  const locale = current
  function applyLocale(locale: string) {
    current.value = locale
    document.documentElement.lang = locale
  }
  function changeLocale(locale: string) {
    applyLocale(locale)
    writePreference(LOCALE_KEY, locale)
  }

  theme.global.name.value = initialTheme()
  applyLocale(initialLocale())

  return { theme, setTheme, getTheme, locale, changeLocale, showNavBar, switchNavBar }
})
