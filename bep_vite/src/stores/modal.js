import { defineStore } from 'pinia'
import { useData } from './data'
import { useFilterStore } from './filter'

const {
  parishMap,
  getParishTransactions,
  getParishInventories,
  getParishHoldings,
} = useData()

export const useParishModalStore = defineStore('parishModal', {
  state: () => ({
    parishId: null,
    open: false,
  }),
  getters: {
    parish: (state) => {
      return parishMap.get(state.parishId) || null
    },
    inventories: (state) => {
        if (state.parishId) {
            const filterStore = useFilterStore()
            return getParishTransactions(state.parishId)
                .filter(filterStore.bookFilter())
                .sort((a, b) => a.start_date - b.start_date)
        }
        return []
    },
    transactions: (state) => {
        if (state.parishId) {
            const filterStore = useFilterStore()
            return getParishInventories(state.parishId)
                .filter(filterStore.bookFilter())
                .sort((a, b) => a.start_date - b.start_date)
        }
        return []
    },
    holdings: (state) => {
      if (state.parishId) {
          const filterStore = useFilterStore()
          return getParishHoldings(state.parishId)
              .filter(filterStore.bookFilter())
              .sort((a, b) => a.start_date - b.start_date)
      }
      return []
    }
  },
  actions: {},
  persist: true,
})