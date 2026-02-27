import { defineStore } from 'pinia'
import { _generateBasicApiResourceStore, _generateParishDependantApiResourceStore } from './_utils.js'

export const useMonarchsStore = defineStore('data-monarchs', _generateBasicApiResourceStore('/api/monarchs'))
// export const useBooksStore = defineStore('data-books', _generateBasicApiResourceStore('/api/books'))

export const useNationsStore = defineStore('data-nations', _generateBasicApiResourceStore('/api/nations'))
export const useProvincesStore = defineStore('data-provinces', _generateBasicApiResourceStore('/api/provinces'))
export const useDiocesesStore = defineStore('data-dioceses', _generateBasicApiResourceStore('/api/dioceses'))
export const useArchdeaconriesStore = defineStore('data-archdeaconries', _generateBasicApiResourceStore('/api/archdeaconries'))
export const useCountiesStore = defineStore('data-counties', _generateBasicApiResourceStore('/api/counties'))
export const useTownsStore = defineStore('data-towns', _generateBasicApiResourceStore('/api/towns'))
export const useParishesStore = defineStore('data-parishes', _generateBasicApiResourceStore('/api/parishes'))

export const useTransactionsStore = defineStore('data-transactions', _generateParishDependantApiResourceStore(
  (id) => `/api/transactions/${id}`,
  (id) => `/api/parishes/${id}/transactions`)
)
export const useHoldingsStore = defineStore('data-holdings', _generateParishDependantApiResourceStore(
  (id) => `/api/holdings/${id}`,
  (id) => `/api/parishes/${id}/holdings`)
)
export const useInventoriesStore = defineStore('data-inventories', _generateParishDependantApiResourceStore(
  (id) => `/api/inventories/${id}`,
  (id) => `/api/parishes/${id}/inventories`)
)



