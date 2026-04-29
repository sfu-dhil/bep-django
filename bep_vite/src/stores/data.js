import { defineStore } from 'pinia'
import {
  _generateSingleFetchApiResourceStore,
  _generateApiResourceStore,
  _generateParishDependantApiResourceStore
} from './_utils.js'

export const useMonarchsStore = defineStore('data-monarchs', _generateApiResourceStore((id) => `/api/monarchs/${id}`, '/api/monarchs'))
export const useBooksStore = defineStore('data-books', _generateApiResourceStore((id) => `/api/books/${id}`, '/api/books'))
export const useArchivesStore = defineStore('data-archives', _generateApiResourceStore((id) => `/api/archives/${id}`, '/api/archives'))
export const useTransactionActionsStore = defineStore('data-transaction-actions', _generateApiResourceStore((id) => `/api/transaction/actions/${id}`, '/api/transaction/actions'))
export const useTransactionMediumsStore = defineStore('data-transaction-mediums', _generateApiResourceStore((id) => `/api/transaction/mediums/${id}`, '/api/transaction/mediums'))
export const usePrintSourcesStore = defineStore('data-print-sources', _generateApiResourceStore((id) => `/api/print/sources/${id}`, '/api/print/sources'))
export const useManuscriptSourcesStore = defineStore('data-manuscript-sources', _generateApiResourceStore((id) => `/api/manuscript/sources/${id}`, '/api/manuscript/sources'))
export const useSourceCategoriesStore = defineStore('data-source-categories', _generateApiResourceStore((id) => `/api/source/categories/${id}`, '/api/source/categories'))
export const useInjunctionStore = defineStore('data-injunctions', _generateApiResourceStore((id) => `/api/injunctions/${id}`, '/api/injunctions'))

export const useNationsStore = defineStore('data-nations', _generateApiResourceStore((id) => `/api/nations/${id}`, '/api/nations'))
export const useProvincesStore = defineStore('data-provinces', _generateApiResourceStore((id) => `/api/provinces/${id}`, '/api/provinces'))
export const useDiocesesStore = defineStore('data-dioceses', _generateApiResourceStore((id) => `/api/dioceses/${id}`, '/api/dioceses'))
export const useArchdeaconriesStore = defineStore('data-archdeaconries', _generateApiResourceStore((id) => `/api/archdeaconries/${id}`, '/api/archdeaconries'))
export const useCountiesStore = defineStore('data-counties', _generateApiResourceStore((id) => `/api/counties/${id}`, '/api/counties'))
export const useTownsStore = defineStore('data-towns', _generateApiResourceStore((id) => `/api/towns/${id}`, '/api/towns'))
export const useParishesStore = defineStore('data-parishes', _generateApiResourceStore((id) => `/api/parishes/${id}`, '/api/parishes'))

export const useParishTransactionsStore = defineStore('data-parish-transactions', _generateParishDependantApiResourceStore((id) => `/api/parishes/${id}/transactions`))
export const useParishHoldingsStore = defineStore('data-parish-holdings', _generateParishDependantApiResourceStore((id) => `/api/parishes/${id}/holdings`))
export const useParishInventoriesStore = defineStore('data-parish-inventories', _generateParishDependantApiResourceStore((id) => `/api/parishes/${id}/inventories`))

