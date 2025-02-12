import { defineStore } from 'pinia'
import { _getPaginatedApiResources, _generateBookMap, _generateParishMap, _getItemsContainingBooks, _getParishItems } from './_utils.js'

export const useTransactionsStore = defineStore('data-transactions', {
  state: () => ({
    transactions: [],
  }),
  getters: {
    transactionsMap: (state) => state.transactions.reduce((result, o) => result.set(o.id, o), new Map()),
    bookTransactionsMap: (state) => _generateBookMap(state.transactions),
    parishTransactionsMap: (state) => _generateParishMap(state.transactions),
  },
  actions: {
    getTransactionsContainingBooks(bookIds) {
      return _getItemsContainingBooks(bookIds, this.transactionsMap, this.bookTransactionsMap)
    },
    getParishTransactions(parishId) {
      return _getParishItems(parishId, this.transactionsMap, this.parishTransactionsMap)
    },
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.transactions.length) {
        _getPaginatedApiResources('transactions').then((results) => ctx.store.$state.transactions = results)
      }
    }
  },
})