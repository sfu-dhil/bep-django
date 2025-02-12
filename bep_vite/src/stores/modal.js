import { defineStore } from 'pinia'
import { useFilterStore } from './filter'
import { useParishesStore } from './api/parishes'
import { useTransactionsStore } from './api/transactions'
import { useInventoriesStore } from './api/inventories'
import { useHoldingsStore } from './api/holdings'

export const useParishModalStore = defineStore('parishModal', {
  state: () => ({
    parishId: null,
    open: false,
  }),
  getters: {
    parish: (state) => {
      return useParishesStore().parishesMap.get(state.parishId) || null
    },
    inventories: (state) => {
        if (state.parishId) {
            const filterStore = useFilterStore()
            return useTransactionsStore().getParishTransactions(state.parishId)
                .filter(filterStore.bookFilter())
                .sort((a, b) => a.start_date - b.start_date)
        }
        return []
    },
    transactions: (state) => {
        if (state.parishId) {
            const filterStore = useFilterStore()
            return useInventoriesStore().getParishInventories(state.parishId)
                .filter(filterStore.bookFilter())
                .sort((a, b) => a.start_date - b.start_date)
        }
        return []
    },
    holdings: (state) => {
      if (state.parishId) {
          const filterStore = useFilterStore()
          return useHoldingsStore().getParishHoldings(state.parishId)
              .filter(filterStore.bookFilter())
              .sort((a, b) => a.start_date - b.start_date)
      }
      return []
    }
  },
  actions: {},
  persist: true,
})