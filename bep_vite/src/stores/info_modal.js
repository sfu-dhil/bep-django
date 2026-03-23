import { defineStore } from 'pinia'

export const useInfoModalStore = defineStore('info-modal', {
  state: () => ({
    objectId: null,
    objectType: null,
    open: false,
    params: {},
    history: [],
  }),
  getters: {},
  actions: {
    hasHistory() { return this.history.length > 0 },
    showPrevious() {
      if (!this.hasHistory()) { return }
      const {objectType, objectId, params} = this.history.pop()
      this.showModal(objectType, objectId, params, false, params)
    },
    showModal(objectType, objectId, params, storeHistory) {
      if (storeHistory && this.objectType && this.open) {
        this.history.push({objectType: this.objectType, objectId: this.objectId, params: this.params})
      }
      this.objectType = objectType
      this.objectId = objectId
      this.params = params || {}
      this.open = true
    },
    reset() {
      this.$reset()
    },
  },
  persist: false,
})