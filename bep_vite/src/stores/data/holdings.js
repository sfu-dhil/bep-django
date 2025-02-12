import { defineStore } from 'pinia'
import { _getPaginatedApiResources, _generateBookMap, _generateParishMap, _getItemsContainingBooks, _getParishItems } from './_utils.js'

export const useHoldingsStore = defineStore('data-holdings', {
  state: () => ({
    holdings: [],
  }),
  getters: {
    holdingsMap: (state) => state.holdings.reduce((result, o) => result.set(o.id, o), new Map()),
    bookHoldingsMap: (state) => _generateBookMap(state.holdings),
    parishHoldingsMap: (state) => _generateParishMap(state.holdings),
  },
  actions: {
    getHoldingsContainingBooks(bookIds) {
      return _getItemsContainingBooks(bookIds, this.holdingsMap, this.bookHoldingsMap)
    },
    getParishHoldings(parishId) {
      return _getParishItems(parishId, this.holdingsMap, this.parishHoldingsMap)
    },
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.holdings.length) {
        _getPaginatedApiResources('holdings').then((results) => ctx.store.$state.holdings = results)
      }
    }
  },
})