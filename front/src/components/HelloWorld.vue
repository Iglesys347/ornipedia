<template>
  <v-parallax src="/banner.jpg" height="600">
    <v-row class="d-flex flex-column fill-height justify-center text-white mx-10">
      <h1 class="text-h3 font-weight-thin mb-4">
        {{ $t("title") }}
      </h1>
      <h2 class="text-h5">
        {{ $t("subtitle") }}
      </h2>
    </v-row>
  </v-parallax>

  <v-container align="center" justify="center">
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4 align-center justify-center text-center" max-width="800">
          <v-row align="center" justify="center">
            <v-col cols="12" md="6">
              <v-card-title>
                {{ $t("navigation.image_gallery.title") }}
              </v-card-title>
              <v-card-text>
                {{ $t("navigation.image_gallery.desc") }}
              </v-card-text>
              <v-card-actions v-if="name != 'sm' && name != 'xs'">
                <v-spacer></v-spacer>
                <v-btn to="/birds" variant="outlined" size="small" append-icon="mdi-arrow-right-thin">{{
                  $t("navigation.image_gallery.title") }}</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-col>
            <v-col cols="12" md="6">
              <v-carousel show-arrows="hover" cycle hide-delimiter-background height="280">
                <v-carousel-item v-for=" i in [1, 2, 3, 4, 5]" :key="i">
                  <v-img :src="getImageUrl(i)" rounded="xl" cover height="280"></v-img>
                </v-carousel-item>
              </v-carousel>
            </v-col>
            <v-card-actions v-if="name == 'sm' || name == 'xs'">
              <v-spacer></v-spacer>
              <v-btn to="/birds" variant="outlined" size="small" append-icon="mdi-arrow-right-thin">{{
                $t("navigation.image_gallery.title") }}</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <!-- <v-row class="d-flex align-center justify-center">
    <v-card>
      <v-card-title class="text-center">
        {{ $t("navigation.quiz.title") }}
      </v-card-title>
      <v-card-text class="text-center">
        {{ $t("navigation.quiz.desc") }}
      </v-card-text>
    </v-card>
  </v-row>
  <v-row class="d-flex align-center justify-center">
    <v-card>
      <v-card-title class="text-center">
        {{ $t("navigation.bird_finder.title") }}
      </v-card-title>
      <v-card-text class="text-center">
        {{ $t("navigation.bird_finder.desc") }}
      </v-card-text>
    </v-card>
  </v-row> -->
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'
import { getImageUrl } from '@/api/images';
const { name } = useDisplay()
</script>

<style scoped>
.grow {
  transition: all .2s ease-in-out;
}

.grow:hover {
  transform: scale(1.05);
}
</style>
