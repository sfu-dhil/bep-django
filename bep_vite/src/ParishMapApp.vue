<script setup>
import ParishMap from './components/ParishMap.vue'

const props = defineProps({
  parishId: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <ParishMap :parish-id="parseInt(parishId)"></ParishMap>
</template>

<style scoped>
</style>