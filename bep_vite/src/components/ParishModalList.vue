<script setup>
import ParishModalListItem from './ParishModalListItem.vue'
const props = defineProps({
  list: {
    type: Array,
    required: true,
  },
  caption: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <table class="table table-striped table-hover">
    <caption>{{ caption }}</caption>
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Date (as written)</th>
        <th scope="col">Books</th>
        <th scope="col"></th>
      </tr>
    </thead>
    <tbody>
      <ParishModalListItem v-for="item in list" :item="item"></ParishModalListItem>
    </tbody>
  </table>
</template>

<style scoped>
</style>