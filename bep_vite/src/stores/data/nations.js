import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useNationsStore = defineStore('data-nations', {
  state: () => ({
    nations: [],
  }),
  getters: {
    nationsMap: (state) => state.nations.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.nations.length) {
        _getPaginatedApiResources('nations').then((results) => ctx.store.$state.nations = results)
      }
    }
  },
})