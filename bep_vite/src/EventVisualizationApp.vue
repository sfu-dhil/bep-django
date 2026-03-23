<script setup>
import { computed } from 'vue'
import EventVisualization from './components/EventVisualization.vue'
import LoadingDots from './components/LoadingDots.vue'

const props = defineProps({
  parishIds: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <Suspense v-if="parishIds">
    <EventVisualization :parishIds="parishIds" />
    <template #fallback><LoadingDots /></template>
  </Suspense>
</template>

<style scoped>
.transaction_visualization_wrapper {
 height: 600px;
}
</style>
