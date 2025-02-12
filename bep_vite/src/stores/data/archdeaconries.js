import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useArchdeaconriesStore = defineStore('data-archdeaconries', {
  state: () => ({
    archdeaconries: [],
  }),
  getters: {
    archdeaconriesMap: (state) => state.archdeaconries.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.archdeaconries.length) {
        _getPaginatedApiResources('archdeaconries').then((results) => ctx.store.$state.archdeaconries = results)
      }
    }
  },
})