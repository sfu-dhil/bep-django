<script setup>
import { ref, computed } from 'vue'
import { useData } from '../stores/data.js'

const {
  bookMap,
} = useData()

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const showMoreBooks = ref(false)
const bookLimit = 5

const bookCount = computed(() => props.item.books.length )
const books = computed(() => {
  const books = props.item.books.map((bookId) => bookMap.get(bookId))
  return books.length > bookLimit && !showMoreBooks.value ? books.slice(0, bookLimit) : books
})
</script>

<template>
  <tr>
    <td>{{ item.id }}</td>
    <td>
      {{ (new Date(item.start_date)).getFullYear() }}
      <span v-if="item.written_date"><br />({{ item.written_date }})</span>
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