import { defineStore } from 'pinia'
import { _getPaginatedApiResources, _getApiResource } from './_utils.js'

export const useBooksStore = defineStore('data-books', {
  state: () => ({
    loadedBooks: [],
  }),
  getters: {
    booksMap: (state) => state.loadedBooks.reduce((result, o) => result.set(o.id, o), new Map()),
    getBookByIds: (state) => {
      return async (ids) => {
        if (!ids || !Array.isArray(ids) || ids.length === 0) { return [] }
        return await ids.filter((id) => id && Number.isInteger(id) && id > 0).map(async (id) => await state.getBookById(id))
      }
    },
    getBookById: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return null }
        if (state.booksMap.has(id)) { return state.booksMap.get(id) }

        const resource = await _getApiResource(`/api/books/${id}`)
        state.loadedBooks.push(resource)
        return resource
      }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})