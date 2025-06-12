<script setup>
import { computed } from 'vue'
import { useTransactionsStore } from '../../stores/data/transactions.js'
import { useInventoriesStore } from '../../stores/data/inventories.js'
import { useHoldingsStore } from '../../stores/data/holdings.js'
import LoadingDots from '../LoadingDots.vue'

const props = defineProps({
  parish: {
    type: Object,
    required: true,
  },
})

const getDates = (objects) => objects.map((o) => o.start_date).filter((o) => o != null && o != '1000-01-01').map((date) => new Date(date))
const formattedDateRange = (objects) => {
  const dates = getDates(objects)
  if (dates.length == 0) { return null }

  const startDate = dates.length > 0 ? new Date(Math.min(...dates)) : null
  const endDate = dates.length > 0 ? new Date(Math.max(...dates)) : null
  if (startDate.getFullYear() != endDate.getFullYear()) {
    return `${startDate.toLocaleString('en-CA', { year: 'numeric' })}-${endDate.toLocaleString('en-CA', { year: 'numeric' })}`
  } else if (startDate.getMonth() != endDate.getMonth()) {
    return `${startDate.toLocaleString('en-CA', { year: 'numeric', month: 'long' })} to ${endDate.toLocaleString('en-CA', { year: 'numeric', month: 'long' })}`
  } else {
    return `${startDate.toLocaleString('en-CA', { year: 'numeric', month: 'long' })}`
  }
}
const inventories = computed(() => useInventoriesStore().getParishInventories(props.parish.id))
const inventoriesUniqueBooks = computed(() => [...inventories.value.reduce((result, o) => result.union(new Set(o.books)), new Set())])
const inventoriesDateRange = computed(() => formattedDateRange(inventories.value))
const transactions = computed(() => useTransactionsStore().getParishTransactions(props.parish.id))
const transactionsUniqueBooks = computed(() => [...transactions.value.reduce((result, o) => result.union(new Set(o.books)), new Set())])
const transactionsDateRange = computed(() => formattedDateRange(transactions.value))
const holdings = computed(() => useHoldingsStore().getParishHoldings(props.parish.id))
const holdingsUniqueBooks = computed(() => [...holdings.value.reduce((result, o) => result.union(new Set(o.books)), new Set())])
const holdingsDateRange = computed(() => formattedDateRange(holdings.value))
const allUniqueBooks = computed(() => [...new Set([...inventoriesUniqueBooks.value, ...transactionsUniqueBooks.value, ...holdingsUniqueBooks.value])])

const isLoadingData = computed(() => useInventoriesStore().inventoriesMap.size === 0 || useTransactionsStore().transactionsMap.size === 0 || useHoldingsStore().holdingsMap.size === 0)
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1>{{ parish.label }}</h1>
        </blockquote>
        <figcaption class="blockquote-footer" v-if="parish.address">
          {{ parish.address }}
        </figcaption>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body pt-3">
    <div v-html="parish.description"></div>

    <dl class="row" v-if="parish.links.length > 0">
      <dt class="col-auto">Links:</dt>
      <dd class="col">
        <div v-for="link in parish.links">
          <a :href="link" target="_blank">{{ link }}</a>
        </div>
      </dd>
    </dl>

    <dl class="row" v-if="transactions.length > 0">
      <dt class="col-auto">{{ transactions.length }} Transactions:</dt>
      <dd class="col">
        Covering {{ transactionsUniqueBooks.length }} unique books<span v-if="transactionsDateRange"> from {{ transactionsDateRange }}</span>
      </dd>
    </dl>
    <dl class="row" v-if="inventories.length > 0">
      <dt class="col-auto">{{ inventories.length }} Inventories:</dt>
      <dd class="col">
        Covering {{ inventoriesUniqueBooks.length }} unique books<span v-if="inventoriesDateRange"> from {{ inventoriesDateRange }}</span>
      </dd>
    </dl>
    <dl class="row" v-if="holdings.length > 0">
      <dt class="col-auto">{{ holdings.length }} Surviving Texts:</dt>
      <dd class="col">
        Covering {{ holdingsUniqueBooks.length }} unique books<span v-if="holdingsDateRange"> from {{ holdingsDateRange }}</span>
      </dd>
    </dl>
  </div>
  <div class="modal-footer">
    <a :href="`/parishes/${parish.id}`" class="btn btn-secondary ms-auto">View Parish Details</a>
  </div>
  <LoadingDots :show="isLoadingData"></LoadingDots>
</template>

<style scoped>
#parish-modal .modal-title .blockquote-footer::before {
  content: none;
}
</style>