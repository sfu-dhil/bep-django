<script setup>
import { computed } from 'vue'
import { formattedDateRange } from '../../helpers/utils.js'
import { useMonarchsStore } from '../../stores/data.js'
import { useInfoModalStore } from '../../stores/info_modal.js'
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

const object = await useMonarchsStore().getById(props.objectId)
const getDate = (d) => d !== null && d != '1000-01-01' ? new Date(d) : null
const reignDateRange = computed(() => formattedDateRange([getDate(object.start_date), getDate(object.end_date)]))
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1 v-html="object.label" />
        </blockquote>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body py-0">
    <div class="pt-3" v-if="object.description" v-html="object.description" />

    <dl class="row gy-3 m-0 row-cols-1 row-cols-lg-2">
      <BasicDetail label="Reign" :value="`From ${reignDateRange}`" v-if="object.start_date || object.end_date" />
      <ObjectModalLinkList label="Books" modal-type="book" :objects="object.books" v-if="object.books.length > 0" objectLabelProperty="title" />
    </dl>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-secondary me-auto" v-if="useInfoModalStore().hasHistory()" @click="() => useInfoModalStore().showPrevious()">Back</button>
    <a :href="`/transactions?monarch=${object.id}`" class="btn btn-primary ms-auto">View All Transactions</a>
  </div>
</template>

<style scoped>
</style>