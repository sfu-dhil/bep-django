<script setup>
import InventoryListItem from './InventoryListItem.vue'
const props = defineProps({
  inventories: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <table class="table table-striped table-hover">
    <caption>List of parish inventory records</caption>
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Date (as written)</th>
        <th scope="col">Books</th>
        <th scope="col"></th>
      </tr>
    </thead>
    <tbody>
      <InventoryListItem v-for="inventory in inventories" :inventory="inventory"></InventoryListItem>
    </tbody>
  </table>
</template>

<style scoped>
</style>