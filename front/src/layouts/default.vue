<template>
  <v-app>
    <DefaultBar />
    <DefaultNavBar />

    <DefaultView />
  </v-app>
</template>

<script lang="ts" setup>
import DefaultBar from './default/AppBar.vue'
import DefaultNavBar from './default/NavBar.vue'
import DefaultView from './default/View.vue'
</script>
