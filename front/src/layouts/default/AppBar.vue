<template>
    <v-app-bar flat elevation="1">
        <v-btn v-if="!showToolbar" icon="mdi-menu" :aria-label="$t('a11y.menu')"
            @click="appStore.switchNavBar"></v-btn>
        <v-spacer></v-spacer>

        <v-toolbar-items v-if="showToolbar">
            <template v-for="(item, index) in navigationItems" :key="item.to">
                <v-divider v-if="index > 0" vertical></v-divider>
                <v-btn variant="text" rounded="0" :to="item.soon ? undefined : item.to" :disabled="item.soon">
                    {{ $t(item.title) }}
                    <v-chip v-if="item.soon" class="ms-2" size="x-small" variant="tonal">{{ $t('soon') }}</v-chip>
                </v-btn>
            </template>
        </v-toolbar-items>

        <v-spacer></v-spacer>


        <v-menu v-model="menu" :close-on-content-click="false" location="end">
            <template v-slot:activator="{ props }">
                <v-btn v-bind="props" icon="mdi-cog-outline" :aria-label="$t('settings')"> </v-btn>
            </template>

            <v-card max-width="350px" elevation="5">
                <v-list class="text-center">
                    <v-list-item>
                        <v-icon class="me-4">mdi-cog-outline</v-icon>
                        {{ $t('settings') }}
                    </v-list-item>
                </v-list>

                <v-divider></v-divider>

                <v-list class="text-center">
                    <v-list-item>
                        <p class="ma-2">{{ $t('settingsTheme') }}</p>
                        <v-btn-toggle mandatory class="ma-2">
                            <v-btn width="100px" append-icon="mdi-weather-sunny"
                                :active="appStore.getTheme() == 'light'" @click="appStore.setTheme('light')"
                                class="me-2">
                                {{ $t('settingsThemeLight') }}
                            </v-btn>
                            <v-btn width="100px" append-icon="mdi-weather-night" :active="appStore.getTheme() == 'dark'"
                                @click="appStore.setTheme('dark')">
                                {{ $t('settingsThemeDark') }}
                            </v-btn>
                        </v-btn-toggle>
                    </v-list-item>

                    <v-list-item>
                        <p class="ma-2">{{ $t('settingsLanguage') }}</p>
                        <v-btn-toggle mandatory class="ma-2">
                            <v-btn v-for="(language, index) in supportedLanguages" :key="language.code" width="100px"
                                :class="{ 'me-2': index < supportedLanguages.length - 1 }" :lang="language.code"
                                :active="appStore.locale == language.code" @click="appStore.changeLocale(language.code)">
                                {{ language.name }}
                            </v-btn>
                        </v-btn-toggle>
                    </v-list-item>
                </v-list>
            </v-card>
        </v-menu>

    </v-app-bar>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue';
import { useAppStore } from '@/store/app';
import { useDisplay } from 'vuetify'
import { supportedLanguages } from '@/translations/i18n';
import { navigationItems } from './navigation';

const appStore = useAppStore()

const menu = ref(false)

const { name } = useDisplay()
const showToolbar = computed(() => {
    return name.value != "xs" && name.value != "sm"
})
</script>
