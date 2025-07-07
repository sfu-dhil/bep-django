import { defineStore } from 'pinia'
import { _getPaginatedApiResources, _getApiResource } from './_utils.js'

export const useHoldingsStore = defineStore('data-holdings', {
  state: () => ({
    loadedHoldings: [],
    loadedForBookIds: [],
  }),
  getters: {
    holdingsMap: (state) => state.loadedHoldings.reduce((result, o) => result.set(o.id, o), new Map()),
    parishHoldingsMap: (state) => state.loadedHoldings.reduce((result, o) => {
      if (!result.has(o.parish_id)) { result.set(o.parish_id, []) }
      result.get(o.parish_id).push(o)
      return result
    }, new Map()),
    loadedForBookIdsSet: (state) => new Set(state.loadedForBookIds.map((id) => id)),
    bookHoldingsMap: (state) => state.loadedHoldings.reduce((result, o) => {
      o.books.forEach(bookId => {
        if (!result.has(bookId)) { result.set(bookId, []) }
        result.get(bookId).push(o)
      })
      return result
    }, new Map()),
    getHoldingById: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return null }
        if (state.holdingsMap.has(id)) { return state.holdingsMap.get(id) }

        const resource = await _getApiResource(`/api/holdings/${id}`)
        state.loadedHoldings.push(resource)
        return resource
      }
    },
    getHoldingsByParishId: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return [] }
        if (state.parishHoldingsMap.has(id)) { return state.parishHoldingsMap.get(id) }

        const resources = await _getPaginatedApiResources(`/api/parishes/${id}/holdings`)
        resources.filter((o) => !state.holdingsMap.has(o.id)).forEach((o) => state.loadedHoldings.push(o))
        return resources
      }
    },
    getHoldingsByBookId: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return [] }
        if (state.loadedForBookIdsSet.has(id)) { return state.bookHoldingsMap.get(id) }

        const resources = await _getPaginatedApiResources(`/api/books/${id}/holdings`)
        resources.filter((o) => !state.holdingsMap.has(o.id)).forEach((o) => state.loadedHoldings.push(o))
        state.loadedForBookIds.push(id)
        return resources
      }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})