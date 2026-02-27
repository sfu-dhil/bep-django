import { defineStore } from 'pinia'

export const useInfoModalStore = defineStore('info-modal', {
  state: () => ({
    objectId: null,
    objectType: null,
    open: false,
    history: [],
  }),
  getters: {},
  actions: {
    hasHistory() { return this.history.length > 0 },
    showPrevious() {
      if (!this.hasHistory()) { return }
      const {objectType, objectId} = this.history.pop()
      this.showModal(objectType, objectId)
    },
    showModal(objectType, objectId, storeHistory) {
      if (storeHistory && this.objectType && this.objectId && this.open) {
        this.history.push({objectType: this.objectType, objectId: this.objectId})
      }
      this.objectType = objectType
      this.objectId = objectId
      this.open = true
    },
    reset() {
      this.$reset()
    },
  },
  persist: false,
})