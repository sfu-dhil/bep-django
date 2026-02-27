<script setup>
const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: String,
  },
})
</script>

<template>
  <dt class="col col-lg-2 px-0">{{ label }}</dt>
  <dd class="col col-lg-10 px-0" v-html="value" />
</template>

<style scoped>
</style>