<template>
  <v-app :theme="appStore.getTheme()">
    <router-view />
  </v-app>
</template>

<script lang="ts" setup>
import { useAppStore } from './store/app';

const appStore = useAppStore()
</script>
