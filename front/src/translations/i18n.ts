import { createI18n } from 'vue-i18n'
import messages from './messages'


export const i18n = createI18n({
    legacy: false, // Vuetify does not support the legacy mode of vue-i18n
    locale: 'fr',
    fallbackLocale: 'en',
    messages,
})

export const supportedLanguages = [{ code: "en", name: "English" }, { code: "fr", name: "Français" }]