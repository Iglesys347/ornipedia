<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card class="d-flex align-center justify-center text-center" height="300px">
          <v-row align="center" justify="center">
            <v-col cols="12">
              <v-icon size="x-large" color="primary">mdi-progress-clock</v-icon>
              <v-card-title class="text-h4" prepend-icon="mdi-progress-clock">{{ $t("quiz.coming_soon.title")
                }}</v-card-title>
              <v-card-text class="text-subtitle-1">
                {{ $t("quiz.coming_soon.desc") }}
              </v-card-text>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
// 
</script>