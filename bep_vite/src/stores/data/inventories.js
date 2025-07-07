import { defineStore } from 'pinia'
import { _getPaginatedApiResources, _getApiResource } from './_utils.js'

export const useInventoriesStore = defineStore('data-inventories', {
  state: () => ({
    loadedInventories: [],
    loadedForBookIds: [],
  }),
  getters: {
    inventoriesMap: (state) => state.loadedInventories.reduce((result, o) => result.set(o.id, o), new Map()),
    parishInventoriesMap: (state) => state.loadedInventories.reduce((result, o) => {
      if (!result.has(o.parish_id)) { result.set(o.parish_id, []) }
      result.get(o.parish_id).push(o)
      return result
    }, new Map()),
    loadedForBookIdsSet: (state) => new Set(state.loadedForBookIds.map((id) => id)),
    bookInventoriesMap: (state) => state.loadedInventories.reduce((result, o) => {
      o.books.forEach(bookId => {
        if (!result.has(bookId)) { result.set(bookId, []) }
        result.get(bookId).push(o)
      })
      return result
    }, new Map()),
    getInventoryById: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return null }
        if (state.inventoriesMap.has(id)) { return state.inventoriesMap.get(id) }

        const resource = await _getApiResource(`/api/inventories/${id}`)
        state.loadedInventories.push(resource)
        return resource
      }
    },
    getInventoriesByParishId: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return [] }
        if (state.parishInventoriesMap.has(id)) { return state.parishInventoriesMap.get(id) }

        const resources = await _getPaginatedApiResources(`/api/parishes/${id}/inventories`)
        resources.filter((o) => !state.inventoriesMap.has(o.id)).forEach((o) => state.loadedInventories.push(o))
        return resources
      }
    },
    getInventoriesByBookId: (state) => {
      return async (id) => {
        if (!id || !Number.isInteger(id) || id <= 0) { return [] }
        if (state.loadedForBookIdsSet.has(id)) { return state.bookInventoriesMap.get(id) }

        const resources = await _getPaginatedApiResources(`/api/books/${id}/inventories`)
        resources.filter((o) => !state.inventoriesMap.has(o.id)).forEach((o) => state.loadedInventories.push(o))
        state.loadedForBookIds.push(id)
        return resources
      }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})