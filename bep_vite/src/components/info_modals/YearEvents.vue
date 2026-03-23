<script setup>
import { computed } from 'vue'
import { useInfoModalStore } from '../../stores/info_modal.js'
import { formattedDateRange } from '../../helpers/utils.js'
import ObjectLinkList from './_ObjectLinkList.vue'
import ObjectModalLinkList from './_ObjectModalLinkList.vue'
import BasicDetail from './_BasicDetail.vue'
import LinksList from './_LinksList.vue'

const props = defineProps({
  objectId: {
    type: [Number, null],
    required: true,
  },
  params: {
    type: Object,
    required: true,
  }
})
const yearLabel = props.objectId === null ? 'Unknown Year' : `Year ${props.objectId}`
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1 v-html="yearLabel" />
        </blockquote>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body py-0">
    <dl class="row gy-3 m-0 row-cols-1 row-cols-lg-2">
      <ObjectModalLinkList label="Injunctions" modal-type="injunction" :objects="params.injunctions" v-if="params.injunctions.length > 0" objectLabelProperty="title" />
      <ObjectLinkList label="Transactions" :link-function="(id) => `/transactions/${id}`" :objects="params.transactions" v-if="params.transactions.length > 0" objectLabelProperty="modern_transcription" />
      <ObjectLinkList label="Inventories" :link-function="(id) => `/inventories/${id}`" :objects="params.inventories" v-if="params.inventories.length > 0" objectLabelProperty="modifications" />
    </dl>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-secondary me-auto" v-if="useInfoModalStore().hasHistory()" @click="() => useInfoModalStore().showPrevious()">Back</button>
  </div>
</template>

<style scoped>
</style>