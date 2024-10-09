import { defineStore } from 'pinia'
import { useData } from './data'
import { useFilterStore } from './filter'

const {
  monarchMap,
} = useData()

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
    timelineFeatures: () => {
        // const filterStore = useFilterStore()
        // const monarchs = filterStore.selectedMonarchs.length > 0 ? filterStore.selectedMonarchs : filterStore.listedMonarchs
        return [...monarchMap.values()]
            .filter((o) => new Date(o.start_date) > new Date('1000-01-01'))
            .sort((a, b) => new Date(a.start_date) - new Date(b.end_date))
    },
    timelinePlaybackStartDate: (state) => {
        const filterStore = useFilterStore()
        if (filterStore.selectedMonarchs.length > 0) {
            const dates = state.timelineFeatures.map((o) => new Date(o.start_date))
            return new Date(Math.min.apply(null, dates))
        } else if (filterStore.startYear) {
            return new Date(`${filterStore.startYear}-01-01`)
        }
        return new Date(`1506-01-01`)
    },
    timelinePlaybackEndDate: (state) => {
        const filterStore = useFilterStore()
        if (filterStore.selectedMonarchs.length > 0) {
            const dates = state.timelineFeatures.map((o) => new Date(o.end_date))
            return new Date(Math.max.apply(null, dates))
        } else if (filterStore.endYear) {
            return new Date(`${filterStore.endYear}-12-31`)
        }
        return new Date(`1686-12-31`)
    },
  },
  actions: {},
  persist: true,
})
