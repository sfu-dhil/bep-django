import { defineStore } from 'pinia'

export const useInfoModalStore = defineStore('info-modal', {
  state: () => ({
    objectId: null,
    objectType: null,
    open: false,
  }),
  getters: {},
  actions: {
    showModal(objectType, objectId) {
      this.objectType = objectType
      this.objectId = objectId
      this.open = true
    },
    hideModal() {
      this.$reset()
    },
  },
  persist: false,
})