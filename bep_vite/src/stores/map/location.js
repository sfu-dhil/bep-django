import { defineStore } from 'pinia'
import { useNationsStore } from '../data/nations'
import { useProvincesStore } from '../data/provinces'
import { useDiocesesStore } from '../data/dioceses'
import { useArchdeaconriesStore } from '../data/archdeaconries'
import { useParishesStore } from '../data/parishes'
import {
    filterByNationId,
    filterByProvinceId,
    filterByDioceseId,
    filterByArchdeaconryId,
} from './_utils.js'

export const useLocationMapStore = defineStore('map-location', {
  state: () => ({
    center: [0, 52.5],
    zoom: 5.5,
    projection: 'EPSG:3857',
    rotation: 0,
    diocesePre1541Visible: false,
    diocesePost1541Visible: true,
    selectedNationId: 5, // England by default
    selectedCountyId: null,
    selectedTownId: null,
    selectedProvinceId: null,
    selectedDioceseId: null,
    selectedArchdeaconryId: null,
    selectedParishId: null,
  }),
  getters: {
    listedNations: () => useNationsStore().nations,
    listedProvinces: (state) => useProvincesStore().provinces.filter(filterByNationId(state.selectedNationId)),
    listedDioceses: (state) => useDiocesesStore().dioceses.filter((o) => filterByNationId(state.selectedNationId)(o) && filterByProvinceId(state.selectedProvinceId)(o)),
    listedArchdeaconries: (state) => useArchdeaconriesStore().archdeaconries.filter((o) => filterByNationId(state.selectedNationId)(o) && filterByProvinceId(state.selectedProvinceId)(o) && filterByDioceseId(state.selectedDioceseId)(o)),
    listedParishes: (state) => useParishesStore().parishes.filter((o) => filterByNationId(state.selectedNationId)(o) && filterByProvinceId(state.selectedProvinceId)(o) && filterByDioceseId(state.selectedDioceseId)(o) && filterByArchdeaconryId(state.selectedArchdeaconryId)(o)),
    // points: () => useParishesStore().parishes.sort((a, b) => b.coordinates[1] - a.coordinates[1] || a.coordinates[0] - b.coordinates[0]),
  },
  actions: {
    updateFilters() {
      if (this.selectedNationId && !this.listedNations.map((o) => o.id).includes(this.selectedNationId)) { this.selectedNationId = null }
      if (this.selectedCountyId && !this.listedCounties.map((o) => o.id).includes(this.selectedCountyId)) { this.selectedCountyId = null }
      if (this.selectedTownId && !this.listedTowns.map((o) => o.id).includes(this.selectedTownId)) { this.selectedTownId = null }
      if (this.selectedProvinceId && !this.listedProvinces.map((o) => o.id).includes(this.selectedProvinceId)) { this.selectedProvinceId = null }
      if (this.selectedDioceseId && !this.listedDioceses.map((o) => o.id).includes(this.selectedDioceseId)) { this.selectedDioceseId = null }
      if (this.selectedArchdeaconryId && !this.listedArchdeaconries.map((o) => o.id).includes(this.selectedArchdeaconryId)) { this.selectedArchdeaconryId = null }
      if (this.selectedParishId && !this.listedParishes.map((o) => o.id).includes(this.selectedParishId)) { this.selectedParishId = null }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})