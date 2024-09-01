<template>
    <v-navigation-drawer v-model="appStore.showNavBar" temporary>
        <v-list density="compact" nav>
            <v-list-item prepend-icon="mdi-home" :title='$t("navigation.home.title")' to="/"></v-list-item>
            <v-list-item prepend-icon="mdi-bird" :title='$t("navigation.image_gallery.title")'
                to="/birds"></v-list-item>
            <v-list-item prepend-icon="mdi-bird" :title='$t("navigation.bird_finder.title")' to="/birds"></v-list-item>
            <v-list-item prepend-icon="mdi-chat-question-outline" :title='$t("navigation.quiz.title")'
                to="/quiz"></v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script setup lang="ts">
import { useAppStore } from '@/store/app';
const appStore = useAppStore()
</script>