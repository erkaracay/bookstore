<template>
  <component :is="layout">
    <RouterView v-slot="{ Component }">
      <component :is="Component" />
    </RouterView>
  </component>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useRoute } from 'vue-router'

const layout = ref(DefaultLayout)
const route = useRoute()

watchEffect(() => {
  // Check for a custom layout property on the matched route's component
  const matchedComponent = route.matched[route.matched.length - 1]?.components?.default
  layout.value = matchedComponent?.layout || DefaultLayout
})
</script>
