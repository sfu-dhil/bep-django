import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useBooksStore = defineStore('data-books', {
  state: () => ({
    books: [],
  }),
  getters: {
    booksMap: (state) => state.books.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.books.length) {
        _getPaginatedApiResources('books').then((results) => ctx.store.$state.books = results)
      }
    }
  },
})