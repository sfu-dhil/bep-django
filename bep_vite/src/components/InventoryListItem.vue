<script setup>
import { ref, computed } from 'vue'
import { useData } from '../stores/data.js'

const {
  bookMap,
} = useData()

const props = defineProps({
  inventory: {
    type: Object,
    required: true,
  },
})

const showMoreBooks = ref(false)
const bookLimit = 5

const bookCount = computed(() => props.inventory.books.length )
const books = computed(() => {
  const books = props.inventory.books.map((bookId) => bookMap.get(bookId))
  return books.length > bookLimit && !showMoreBooks.value ? books.slice(0, bookLimit) : books
})
</script>

<template>
  <tr>
    <td>{{ inventory.id }}</td>
    <td>
      {{ (new Date(inventory.start_date)).getFullYear() }}
      <span v-if="inventory.written_date"><br />({{ inventory.written_date }})</span>
    </td>
    <td>
      <div class="badge text-bg-success m-1" v-for="book in books">
        {{ book?.title }}
      </div>
      <button class="badge text-bg-secondary" v-if="bookCount > bookLimit && !showMoreBooks" @click="showMoreBooks = true">
        + {{ bookCount - bookLimit }} more
      </button>
    </td>
    <td>+details</td>
  </tr>
</template>

<style scoped>
</style>