import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useDiocesesStore = defineStore('data-dioceses', {
  state: () => ({
    dioceses: [],
  }),
  getters: {
    diocesesMap: (state) => state.dioceses.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.dioceses.length) {
        _getPaginatedApiResources('dioceses').then((results) => ctx.store.$state.dioceses = results)
      }
    }
  },
})