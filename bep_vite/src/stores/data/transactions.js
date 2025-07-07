import { defineStore } from 'pinia'
import { _getPaginatedApiResources, _getApiResource } from './_utils.js'

export const useTransactionsStore = defineStore('data-transactions', {
  state: () => ({
    loadedTransactions: [],
    loadedForBookIds: [],
  }),
  getters: {
    transactionsMap: (state) => state.loadedTransactions.reduce((result, o) => result.set(o.id, o), new Map()),
    parishTransactionsMap: (state) => state.loadedTransactions.reduce((result, o) => {
      if (!result.has(o.parish_id)) { result.set(o.parish_id, []) }
      result.get(o.parish_id).push(o)
      return result
    }, new Map()),
    loadedForBookIdsSet: (state) => new Set(state.loadedForBookIds.map((id) => id)),
    bookTransactionsMap: (state) => state.loadedTransactions.reduce((result, o) => {
      o.books.forEach(bookId => {
        if (!result.has(bookId)) { result.set(bookId, []) }
        result.get(bookId).push(o)
      })
      return result
    }, new Map()),
    getTransactionById: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return null }
        if (state.transactionsMap.has(id)) { return state.transactionsMap.get(id) }

        const resource = await _getApiResource(`/api/transactions/${id}`)
        state.loadedTransactions.push(resource)
        return resource
      }
    },
    getTransactionsByParishId: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return [] }
        if (state.parishTransactionsMap.has(id)) { return state.parishTransactionsMap.get(id) }

        const resources = await _getPaginatedApiResources(`/api/parishes/${id}/transactions`)
        resources.filter((o) => !state.transactionsMap.has(o.id)).forEach((o) => state.loadedTransactions.push(o))
        return resources
      }
    },
    getTransactionsByBookId: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return [] }
        if (state.loadedForBookIdsSet.has(id)) { return state.bookTransactionsMap.get(id) }

        const resources = await _getPaginatedApiResources(`/api/books/${id}/transactions`)
        resources.filter((o) => !state.transactionsMap.has(o.id)).forEach((o) => state.loadedTransactions.push(o))
        state.loadedForBookIds.push(id)
        return resources
      }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})