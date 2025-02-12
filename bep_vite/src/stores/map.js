import { defineStore } from 'pinia'
import { useFilterStore } from './filter'

export const useMapStore = defineStore('map', {
  state: () => ({
    center: [0, 52.5],
    zoom: 7.5,
    projection: 'EPSG:3857',
    rotation: 0,
  }),
  getters: {
    parishes: () => {
        const filterStore = useFilterStore()
        const points = filterStore.selectedParishes.length > 0 ? filterStore.selectedParishes : filterStore.listedParishes
        return points.sort((a, b) => b.latitude - a.latitude || a.longitude - b.longitude)
    },
  },
  actions: {},
  persist: true,
})
