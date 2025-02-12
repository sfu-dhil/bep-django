import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useCountiesStore = defineStore('data-counties', {
  state: () => ({
    counties: [],
  }),
  getters: {
    countiesMap: (state) => state.counties.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.counties.length) {
        _getPaginatedApiResources('counties').then((results) => ctx.store.$state.counties = results)
      }
    }
  },
})