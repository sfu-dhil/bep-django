<script setup>
const props = defineProps({
  links: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <dt class="col col-lg-2 px-0">Links:</dt>
  <dd class="col col-lg-10 px-0">
    <div v-for="link in links">
      <a target="_blank" :href="link" v-html="link" />
    </div>
  </dd>
</template>

<style scoped>
</style>