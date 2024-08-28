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
export default createVuetify({
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
