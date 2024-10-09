<script setup>
import { watch } from 'vue'
import SidebarFilter from './SidebarFilter.vue'
import { useFilterStore } from '../stores/filter.js'
import { storeToRefs } from 'pinia'

const store = useFilterStore()
const {
  selectedNations,
  selectedCounties,
  selectedTowns,
  selectedProvinces,
  selectedDioceses,
  selectedArchdeaconries,
  selectedParishes,
  selectedBooks,
  selectedMonarchs,

  bookRecordToggle,
  countyProvincesToggle,
  startYear,
  endYear,

  listedNations,
  listedCounties,
  listedTowns,
  listedProvinces,
  listedDioceses,
  listedArchdeaconries,
  listedParishes,
  listedBooks,
  listedMonarchs,
} = storeToRefs(store)

const resetStore = () => {
  if (confirm('Are you sure you want to reset the current settings?')) {
    store.$reset()
  }
}
watch(countyProvincesToggle, (newValue, oldValue) => {
  if (newValue != oldValue) {
    if (newValue === 'province') {
      selectedCounties.value = []
      selectedTowns.value = []
    } else if (newValue === 'county') {
      selectedProvinces.value = []
      selectedDioceses.value = []
      selectedArchdeaconries.value = []
    }
    store.updateFilters()
  }
})
</script>

<template>
  <div class="my-2 px-3 sidebar">
    <h3 class="w-100 text-center">
      Time Period
    </h3>
    <div class="input-group mb-3">
      <div class="input-group-text">Period</div>
      <input type="number" class="form-control" v-model.number="startYear" min="1508" max="1685" placeholder="Start Year" />
      <div class="input-group-text">to</div>
      <input type="number" class="form-control" v-model.number="endYear" min="1508" max="1685" placeholder="End Year" />
    </div>
    <div class="w-100 text-center my-1">
      - or -
    </div>
    <SidebarFilter v-model:selected="selectedMonarchs" v-model:listed="listedMonarchs" label="Monarch"></SidebarFilter>


    <h3 class="w-100 text-center mt-5">
      Books
    </h3>
    <SidebarFilter v-model:selected="selectedBooks" v-model:listed="listedBooks" label="Book" objectLabel="title"></SidebarFilter>
    <div class="btn-group mb-3 w-100" role="group">
      <label class="input-group-text">Records</label>

      <input type="radio" class="btn-check" autocomplete="off" name="book-record-toggle"
          id="inventory-radio" value="inventory"
          v-model="bookRecordToggle"
      />
      <label class="btn btn-outline-primary" for="inventory-radio">Inventories</label>

      <input type="radio" class="btn-check" autocomplete="off" name="book-record-toggle"
          id="transaction-radio" value="transaction"
          v-model="bookRecordToggle"
      />
      <label class="btn btn-outline-primary" for="transaction-radio">Transactions</label>

      <input type="radio" class="btn-check" autocomplete="off" name="book-record-toggle"
          id="holding-radio" value="holding"
          v-model="bookRecordToggle"
      />
      <label class="btn btn-outline-primary" for="holding-radio">Surviving Texts</label>
    </div>


    <h3 class="w-100 text-center mt-5">
      Parishes
    </h3>
    <SidebarFilter v-model:selected="selectedNations" v-model:listed="listedNations" label="Nation"></SidebarFilter>
    <div class="btn-group mb-3 w-100" role="group">
      <label class="input-group-text">Filter By</label>

      <input type="radio" class="btn-check" autocomplete="off" name="county-provinces-toggle"
          id="provinces-radio" value="province"
          v-model="countyProvincesToggle"
      />
      <label class="btn btn-outline-primary" for="provinces-radio">Province / Diocese / Archdeaconry</label>

      <input type="radio" class="btn-check" autocomplete="off" name="county-provinces-toggle"
          id="county-radio" value="county"
          v-model="countyProvincesToggle"
      />
      <label class="btn btn-outline-primary" for="county-radio">County / Town</label>
    </div>
    <SidebarFilter v-if="countyProvincesToggle === 'county'" v-model:selected="selectedCounties" v-model:listed="listedCounties" label="County"></SidebarFilter>
    <SidebarFilter v-if="countyProvincesToggle === 'county'" v-model:selected="selectedTowns" v-model:listed="listedTowns" label="Town"></SidebarFilter>
    <SidebarFilter v-if="countyProvincesToggle === 'province'" v-model:selected="selectedProvinces" v-model:listed="listedProvinces" label="Province"></SidebarFilter>
    <SidebarFilter v-if="countyProvincesToggle === 'province'" v-model:selected="selectedDioceses" v-model:listed="listedDioceses" label="Diocese"></SidebarFilter>
    <SidebarFilter v-if="countyProvincesToggle === 'province'" v-model:selected="selectedArchdeaconries" v-model:listed="listedArchdeaconries" label="Archdeaconry"></SidebarFilter>
    <SidebarFilter v-model:selected="selectedParishes" v-model:listed="listedParishes" label="Parish"></SidebarFilter>

    <div class="d-grid gap-2 w-100 mt-5">
      <button type="button" class="btn btn-danger" @click="resetStore">Reset</button>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  height: 100%;
  max-height: 100vh;
  overflow-y: auto;
}
</style>
