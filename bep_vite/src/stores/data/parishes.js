import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useParishesStore = defineStore('data-parishes', {
  state: () => ({
    parishes: [],
  }),
  getters: {
    parishesMap: (state) => state.parishes.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.parishes.length) {
        _getPaginatedApiResources('/api/parishes').then((results) => ctx.store.$state.parishes = results)
      }
    }
  },
})