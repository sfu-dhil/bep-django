import { defineStore } from 'pinia'
import { _getPaginatedApiResources, _generateBookMap, _generateParishMap, _getItemsContainingBooks, _getParishItems } from './_utils.js'

export const useInventoriesStore = defineStore('data-inventories', {
  state: () => ({
    inventories: [],
  }),
  getters: {
    inventoriesMap: (state) => state.inventories.reduce((result, o) => result.set(o.id, o), new Map()),
    bookInventoriesMap: (state) => _generateBookMap(state.inventories),
    parishInventoriesMap: (state) => _generateParishMap(state.inventories),
  },
  actions: {
    getInventoriesContainingBooks(bookIds) {
      return _getItemsContainingBooks(bookIds, this.inventoriesMap, this.bookInventoriesMap)
    },
    getParishInventories(parishId) {
      return _getParishItems(parishId, this.inventoriesMap, this.parishInventoriesMap)
    },
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.inventories.length) {
        _getPaginatedApiResources('inventories').then((results) => ctx.store.$state.inventories = results)
      }
    }
  },
})