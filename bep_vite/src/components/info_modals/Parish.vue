<script setup>
import { computed } from 'vue'
import {
  useParishesStore,
  useParishTransactionsStore,
  useParishInventoriesStore,
  useParishHoldingsStore,
} from '../../stores/data.js'
import { useInfoModalStore } from '../../stores/info_modal.js'
import { formattedYearRange } from '../../helpers/utils.js'
import ObjectLinkList from './_ObjectLinkList.vue'
import ObjectModalLinkList from './_ObjectModalLinkList.vue'
import BasicDetail from './_BasicDetail.vue'
import LinksList from './_LinksList.vue'

const props = defineProps({
  objectId: {
    type: Number,
    required: true,
  },
})

const object = await useParishesStore().getById(props.objectId)
const inventories = await useParishInventoriesStore().getByParishId(props.objectId)
const transactions = await useParishTransactionsStore().getByParishId(props.objectId)
const holdings = await useParishHoldingsStore().getByParishId(props.objectId)

const getYears = (objects) => objects.map((o) => o.sort_year).filter((o) => o != null)
const inventoriesYearRange = computed(() => formattedYearRange(getYears(inventories)))
const transactionsYearRange = computed(() => formattedYearRange(getYears(transactions)))
const holdingsYearRange = computed(() => formattedYearRange(getYears(holdings)))
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1 v-html="object.label" />
        </blockquote>
        <figcaption class="blockquote-footer" v-if="object.address" v-html="object.address" />
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body py-0">
    <div class="pt-3" v-if="object.description" v-html="object.description" />

    <dl class="row gy-3 m-0 row-cols-1 row-cols-lg-2">
      <LinksList :links="object.links" v-if="object.links.length > 0" />
      <BasicDetail :label="`${transactions.length} Transactions`" :value="`From ${transactionsYearRange}`" v-if="transactionsYearRange" />
      <BasicDetail :label="`${inventories.length} Inventories`" :value="`From ${inventoriesYearRange}`" v-if="inventoriesYearRange" />
      <BasicDetail :label="`${holdings.length} Surviving Texts`" :value="`From ${holdingsYearRange}`" v-if="holdingsYearRange" />
    </dl>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-secondary me-auto" v-if="useInfoModalStore().hasHistory()" @click="() => useInfoModalStore().showPrevious()">Back</button>
    <a :href="`/transactions?parish=${object.id}`" class="btn btn-primary ms-auto">View All Transactions</a>
    <a :href="`/parishes/${object.id}`" class="btn btn-primary">View Parish Details</a>
  </div>
</template>

<style scoped>
</style>