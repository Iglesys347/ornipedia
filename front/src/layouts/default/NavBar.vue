<template>
    <v-navigation-drawer v-model="appStore.showNavBar" temporary>
        <v-list density="compact" nav>
            <v-list-item v-for="item in navigationItems" :key="item.to" :prepend-icon="item.icon"
                :title="$t(item.title)" :to="item.soon ? undefined : item.to" :disabled="item.soon">
                <template v-if="item.soon" v-slot:append>
                    <v-chip size="x-small" variant="tonal">{{ $t('soon') }}</v-chip>
                </template>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script setup lang="ts">
import { useAppStore } from '@/store/app';
import { navigationItems } from './navigation';
const appStore = useAppStore()
</script>
