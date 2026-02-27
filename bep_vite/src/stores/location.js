import { defineStore } from 'pinia'

export const useLocationMapStore = defineStore('map-location', {
  state: () => ({
    center: [-2, 53],
    zoom: 5.5,
    projection: 'EPSG:3857',
    rotation: 0,
    diocesePre1541Visible: false,
    diocesePost1541Visible: true,
    // selectedNationId: 5, // England by default
    selectedCountyId: null,
    // selectedTownId: null,
    // selectedProvinceId: null,
    // selectedDioceseId: null,
    // selectedArchdeaconryId: null,
    selectedParishId: null,
  }),
  persist: {
    storage: sessionStorage,
  },
})