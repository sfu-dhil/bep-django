import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useMonarchsStore = defineStore('data-monarchs', {
  state: () => ({
    monarchs: [],
  }),
  getters: {
    monarchsMap: (state) => state.monarchs.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.monarchs.length) {
        _getPaginatedApiResources('/api/monarchs').then((results) => ctx.store.$state.monarchs = results)
      }
    }
  },
})