<script setup>
import { computed } from 'vue'
import {
  useParishesStore,
  useTransactionsStore,
  useInventoriesStore,
  useHoldingsStore,
} from '../../stores/data.js'
import { formattedDateRange } from '../../helpers/utils.js'

const props = defineProps({
  objectId: {
    type: Number,
    required: true,
  },
})

const object = await useParishesStore().getById(props.objectId)
const inventories = await useInventoriesStore().getByParishId(props.objectId)
const transactions = await useTransactionsStore().getByParishId(props.objectId)
const holdings = await useHoldingsStore().getByParishId(props.objectId)

const getDates = (objects) => objects.map((o) => o.start_date).filter((o) => o != null && o != '1000-01-01').map((date) => new Date(date))
const inventoriesDateRange = computed(() => formattedDateRange(getDates(inventories)))
const transactionsDateRange = computed(() => formattedDateRange(getDates(transactions)))
const holdingsDateRange = computed(() => formattedDateRange(getDates(holdings)))
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1>{{ object.label }}</h1>
        </blockquote>
        <figcaption class="blockquote-footer" v-if="object.address">
          {{ object.address }}
        </figcaption>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body pt-3">
    <div v-html="object.description"></div>

    <dl class="row" v-if="object.links.length > 0">
      <dt class="col-auto">Links:</dt>
      <dd class="col">
        <div v-for="link in object.links">
          <a :href="link" target="_blank">{{ link }}</a>
        </div>
      </dd>
    </dl>
    <dl class="row" v-if="transactions.length > 0">
      <dt class="col-auto">{{ transactions.length }} Transactions:</dt>
      <dd class="col" v-if="transactionsDateRange">
        From {{ transactionsDateRange }}
      </dd>
    </dl>
    <dl class="row" v-if="inventories.length > 0">
      <dt class="col-auto">{{ inventories.length }} Inventories:</dt>
      <dd class="col" v-if="inventoriesDateRange">
        from {{ inventoriesDateRange }}
      </dd>
    </dl>
    <dl class="row" v-if="holdings.length > 0">
      <dt class="col-auto">{{ holdings.length }} Surviving Texts:</dt>
      <dd class="col" v-if="holdingsDateRange">
        From {{ holdingsDateRange }}
      </dd>
    </dl>
  </div>
  <div class="modal-footer">
    <a :href="`/parishes/${object.id}`" class="btn btn-secondary ms-auto">View Parish Details</a>
  </div>
</template>

<style scoped>
.blockquote-footer::before {
  content: none;
}
</style>