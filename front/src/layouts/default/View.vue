<template>
  <v-main class="d-flex flex-column">
    <div class="flex-grow-1">
      <router-view />
    </div>

    <v-footer class="justify-center text-center text-caption text-medium-emphasis py-6" color="transparent">
      <div>
        <div class="d-flex align-center justify-center mb-1">
          <v-icon color="primary" size="18" class="me-1">mdi-bird</v-icon>
          <span class="font-weight-medium">Ornipedia</span>
        </div>
        {{ $t("footer.credits") }}
      </div>
    </v-footer>
  </v-main>
</template>
