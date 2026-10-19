/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import { createVueI18nAdapter } from 'vuetify/locale/adapters/vue-i18n'
import { useI18n } from 'vue-i18n'
import { i18n } from '../translations/i18n'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
// "Nature" palette: forest green (primary) and lake blue (secondary).
// All text/background pairs below reach the WCAG AA contrast ratio (4.5:1).
const light = {
  dark: false,
  colors: {
    primary: '#2F6B45',
    secondary: '#2E6F95',
    background: '#F6F7F2',
    surface: '#FFFFFF',
    'surface-variant': '#E7ECE4',
    'on-surface-variant': '#2B332D',
    'on-background': '#1C221E',
    'on-surface': '#1C221E',
  },
}

const dark = {
  dark: true,
  colors: {
    primary: '#8FD1A4',
    'on-primary': '#0F2417',
    secondary: '#8EC5E8',
    'on-secondary': '#0B2433',
    background: '#111613',
    surface: '#19201B',
    'surface-variant': '#2A332C',
    'on-surface-variant': '#DCE5DC',
    'on-background': '#E3E8E3',
    'on-surface': '#E3E8E3',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: { light, dark },
  },
  locale: {
    adapter: createVueI18nAdapter({ i18n, useI18n }),
  },
  defaults: {
    VBtn: {
      style: 'text-transform: unset;',
      elevation: 0,
      variant: "tonal",
      rounded: 'pill'
    },
    VCard: {
      elevation: 0,
      rounded: 'xl'
    },
    VAutocomplete: {
      rounded: 'pill',
      variant: "outlined"
    },
    VTextField: {
      rounded: "pill",
      variant: "outlined",
      elevation: 0
    },
  },
})
