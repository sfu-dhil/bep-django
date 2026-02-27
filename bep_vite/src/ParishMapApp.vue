<script setup>
import ParishMap from './components/ParishMap.vue'
import LoadingDots from './components/LoadingDots.vue'

const props = defineProps({
  parishId: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <Suspense v-if="parishId">
    <ParishMap :parishId="parseInt(parishId)"></ParishMap>
    <template #fallback>
      <LoadingDots :show="true"></LoadingDots>
    </template>
  </Suspense>
</template>

<style scoped>
</style>