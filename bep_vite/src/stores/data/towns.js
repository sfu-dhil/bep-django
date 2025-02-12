import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useTownsStore = defineStore('data-towns', {
  state: () => ({
    towns: [],
  }),
  getters: {
    townsMap: (state) => state.towns.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.towns.length) {
        _getPaginatedApiResources('towns').then((results) => ctx.store.$state.towns = results)
      }
    }
  },
})