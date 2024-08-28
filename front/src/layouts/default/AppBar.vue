<template>
    <v-app-bar flat elevation="1">
        <v-btn v-if="!showToolbar" icon="mdi-menu" @click="appStore.switchNavBar"></v-btn>
        <v-spacer></v-spacer>

        <v-toolbar-items v-if="showToolbar">
            <v-btn variant="text" rounded="0" href="/">{{ $t("navigation.home.title") }}</v-btn>
            <v-divider vertical></v-divider>
            <v-btn variant="text" rounded="0" href="/birds">{{ $t("navigation.image_gallery.title") }}</v-btn>
            <v-divider vertical></v-divider>
            <v-btn variant="text" rounded="0" href="/bird-finder">{{ $t("navigation.bird_finder.title") }}</v-btn>
            <v-divider vertical></v-divider>
            <v-btn variant="text" rounded="0" href="/quiz">{{ $t("navigation.quiz.title") }}</v-btn>
        </v-toolbar-items>

        <v-spacer></v-spacer>


        <v-menu v-model="menu" :close-on-content-click="false" location="end">
            <template v-slot:activator="{ props }">
                <v-btn v-bind="props" icon="mdi-cogs"> </v-btn>
            </template>

            <v-card max-width="350px" elevation="5">
                <v-list class="text-center">
                    <v-list-item>
                        <v-icon class="me-4">mdi-cogs</v-icon>
                        {{ $t('settings') }}
                    </v-list-item>
                </v-list>

                <v-divider></v-divider>

                <v-list class="text-center">
                    <v-list-item>
                        <p class="ma-2">{{ $t('settingsTheme') }}</p>
                        <v-btn-toggle class="ma-2">
                            <v-btn width="100px" append-icon="mdi-weather-sunny"
                                :active="appStore.getTheme() == 'light'" @click="appStore.switchTheme" class="me-2">
                                {{ $t('settingsThemeLight') }}
                            </v-btn>
                            <v-btn width="100px" append-icon="mdi-weather-night" :active="appStore.getTheme() == 'dark'"
                                @click="appStore.switchTheme">
                                {{ $t('settingsThemeDark') }}
                            </v-btn>
                        </v-btn-toggle>
                    </v-list-item>

                    <v-list-item>
                        <p class="ma-2">{{ $t('settingsLanguage') }}</p>
                        <v-btn-toggle mandatory class="ma-2">
                            <v-btn width="100px" @click="appStore.changeLocale('en')" :active="appStore.locale == 'en'"
                                class="me-2">
                                EN 🇬🇧
                            </v-btn>

                            <v-btn width="100px" @click="appStore.changeLocale('fr')" :active="appStore.locale == 'fr'">
                                FR 🇫🇷
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

const appStore = useAppStore()

const menu = ref(false)

const { name } = useDisplay()
const showToolbar = computed(() => {
    return name.value != "xs" && name.value != "sm"
}) 
</script>
