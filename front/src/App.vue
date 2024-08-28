<template>
  <v-app :theme="appStore.getTheme()">
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { useAppStore } from './store/app';

const appStore = useAppStore()
</script>
