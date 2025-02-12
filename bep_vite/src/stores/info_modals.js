import { defineStore } from 'pinia'
import { useParishesStore } from './data/parishes.js'

export const useInfoModalStore = defineStore('info-modals', {
  state: () => ({
    objectId: null,
    objectType: null,
    open: false,
  }),
  getters: {
    object: (state) => {
      switch (state.objectType) {
        case 'parish': return useParishesStore().parishesMap.get(state.objectId)
        default: return null
      }
    },
  },
  actions: {
    showModal(objectType, objectId) {
      this.objectType = objectType
      this.objectId = objectId
      if (this.object) { this.open = true }
    },
    hideModal() {
      this.$reset()
    },
  },
  persist: false,
})