import { defineStore } from 'pinia'
import { isSameObjectArrayById } from '../helpers/utils'
import { useNationsStore } from './api/nations'
import { useCountiesStore } from './api/counties'
import { useTownsStore } from './api/towns'
import { useProvincesStore } from './api/provinces'
import { useDiocesesStore } from './api/dioceses'
import { useArchdeaconriesStore } from './api/archdeaconries'
import { useParishesStore } from './api/parishes'
import { useMonarchsStore } from './api/monarchs'
import { useBooksStore } from './api/books'
import { useTransactionsStore } from './api/transactions'
import { useInventoriesStore } from './api/inventories'
import { useHoldingsStore } from './api/holdings'

export const useFilterStore = defineStore('filter', {
  state: () => ({
    selectedNations: [],
    selectedCounties: [],
    selectedTowns: [],
    selectedProvinces: [],
    selectedDioceses: [],
    selectedArchdeaconries: [],
    selectedParishes: [],
    selectedBooks: [],
    selectedMonarchs: [],
    countyProvincesToggle: 'province',
    bookRecordToggle: 'inventory',
    startYear: null,
    endYear: null,
  }),
  getters: {
    listedNations: () => useNationsStore().nations,
    listedCounties: (state) => useCountiesStore().counties.filter(state.nationFilter()),
    listedTowns: (state) => useTownsStore().towns.filter((o) => state.nationFilter()(o) && state.countyFilter()(o)),
    listedProvinces: (state) => useProvincesStore().provinces.filter(state.nationFilter()),
    listedDioceses: (state) => useDiocesesStore().dioceses.filter((o) => state.nationFilter()(o) && state.provinceFilter()(o)),
    listedArchdeaconries: (state) => useArchdeaconriesStore().archdeaconries.filter((o) => state.nationFilter()(o) && state.provinceFilter()(o) && state.dioceseFilter()(o)),
    listedParishes: (state) => useParishesStore().parishes.filter((o) => state.nationFilter()(o) && state.provinceFilter()(o) && state.dioceseFilter()(o) && state.archdeaconryFilter()(o) && state.countyFilter()(o) && state.townFilter()(o) && state.parishBookRecordFilter()(o)),
    listedMonarchs: () => useMonarchsStore().monarchs,
    listedBooks: () => useBooksStore().books,
  },
  actions: {
    toggleSelectedMonarch(monarch) {
      if (this.isSelectedMonarch(monarch)) {
        this.selectedMonarchs = this.selectedMonarchs.filter((o) => o.id != monarch.id)
      } else {
        this.selectedMonarchs = this.selectedMonarchs.concat([monarch])
      }
    },
    isSelectedMonarch(monarch) {
      return this.selectedMonarchs.map((o) => o.id).includes(monarch.id)
    },
    nationFilter() {
      const nationIds = this.selectedNations.map((o) => o.id)
      return nationIds.length === 0 ? () => true : (o) => nationIds.includes(o.nation_id)
    },
    countyFilter() {
      const countyIds = this.selectedCounties.map((o) => o.id)
      return countyIds.length === 0 ? () => true : (o) => countyIds.includes(o.county_id)
    },
    townFilter() {
      const townIds = this.selectedTowns.map((o) => o.id)
      return townIds.length === 0 ? () => true : (o) => townIds.includes(o.town_id)
    },
    provinceFilter() {
      const provinceIds = this.selectedProvinces.map((o) => o.id)
      return provinceIds.length === 0 ? () => true : (o) => provinceIds.includes(o.province_id)
    },
    dioceseFilter() {
      const dioceseIds = this.selectedDioceses.map((o) => o.id)
      return dioceseIds.length === 0 ? () => true : (o) => dioceseIds.includes(o.diocese_id)
    },
    archdeaconryFilter() {
      const archdeaconryIds = this.selectedArchdeaconries.map((o) => o.id)
      return archdeaconryIds.length === 0 ? () => true : (o) => archdeaconryIds.includes(o.archdeaconry_id)
    },
    parishFilter() {
      const parishIds = this.selectedParishes.map((o) => o.id)
      return parishIds.length === 0 ? () => true : (o) => parishIds.includes(o.parish_id)
    },
    bookFilter() {
      if (this.selectedBooks.length > 0) {
          const bookIdsSet = new Set(this.selectedBooks.map((o) => o.id))
          return (o) => bookIdsSet.intersection(new Set(o.books)).size > 0
      }
      return () => true
    },
    parishBookRecordFilter() {
      if (this.selectedBooks.length > 0) {
        const bookIds = this.selectedBooks.map((o) => o.id)
        let dataset = []
        if (this.bookRecordToggle == 'transaction') {
          dataset = useTransactionsStore().getTransactionsContainingBooks(bookIds)
        } else if (this.bookRecordToggle == 'inventory') {
          dataset = useInventoriesStore().getInventoriesContainingBooks(bookIds)
        } else {
          dataset = useHoldingsStore().getHoldingsContainingBooks(bookIds)
        }
        const parishIds = dataset.map((o) => o.parish_id)
        return (o) => parishIds.includes(o.id)
      }
      return () => true
    },
    _updateFilter(selectedName, filterFunc) {
      const updated = this[selectedName].filter(filterFunc)
      if (!isSameObjectArrayById(this[selectedName], updated)) {
        this[selectedName] = updated
      }
    },
    updateFilters() {
      this._updateFilter('selectedCounties', this.nationFilter())
      this._updateFilter('selectedTowns', (o) => this.nationFilter()(o) && this.countyFilter()(o))
      this._updateFilter('selectedProvinces', this.nationFilter())
      this._updateFilter('selectedDioceses', (o) => this.nationFilter()(o) && this.provinceFilter()(o))
      this._updateFilter('selectedArchdeaconries', (o) => this.nationFilter()(o) && this.provinceFilter()(o) && this.dioceseFilter()(o))
      this._updateFilter('selectedParishes', (o) => this.nationFilter()(o) && this.provinceFilter()(o) && this.dioceseFilter()(o) && this.archdeaconryFilter()(o) && this.countyFilter()(o) && this.townFilter()(o) && this.parishBookRecordFilter()(o))
    },
  },
  persist: true,
})