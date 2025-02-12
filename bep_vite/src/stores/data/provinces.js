import { defineStore } from 'pinia'
import { _getPaginatedApiResources } from './_utils.js'

export const useProvincesStore = defineStore('data-provinces', {
  state: () => ({
    provinces: [],
  }),
  getters: {
    provincesMap: (state) => state.provinces.reduce((result, o) => result.set(o.id, o), new Map()),
  },
  persist: {
    storage: sessionStorage,
    afterHydrate: (ctx) => {
      if (0 === ctx.store.$state.provinces.length) {
        _getPaginatedApiResources('provinces').then((results) => ctx.store.$state.provinces = results)
      }
    }
  },
})