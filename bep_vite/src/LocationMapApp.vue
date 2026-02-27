<script setup>
import LocationMap from './components/LocationMap.vue'
import LoadingDots from './components/LoadingDots.vue'
</script>

<template>
  <Suspense>
    <LocationMap></LocationMap>
    <template #fallback>
      <LoadingDots :show="true"></LoadingDots>
    </template>
  </Suspense>
</template>

<style scoped>
</style>