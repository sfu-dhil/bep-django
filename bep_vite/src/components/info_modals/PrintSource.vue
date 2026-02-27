<script setup>
import { usePrintSourcesStore } from '../../stores/data.js'
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

const object = await usePrintSourcesStore().getById(props.objectId)
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1 v-html="object.title" />
        </blockquote>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body py-0">
    <dl class="row gy-3 m-0 row-cols-1 row-cols-lg-2">
      <ObjectModalLinkList label="Source Category" modal-type="source_category" :objects="[object.source_category]" v-if="object.source_category" />
      <BasicDetail label="Author" :value="object.author" v-if="object.author" />
      <BasicDetail label="Date" :value="object.date" v-if="object.date" />
      <BasicDetail label="Publisher" :value="object.publisher" v-if="object.publisher" />
      <BasicDetail label="Notes" :value="object.notes" v-if="object.notes" />
      <LinksList :links="object.links" v-if="object.links.length > 0" />
    </dl>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-secondary me-auto" v-if="useInfoModalStore().hasHistory()" @click="() => useInfoModalStore().showPrevious()">Back</button>
    <a :href="`/transactions?print_source=${object.id}`" class="btn btn-primary ms-auto">View All Transactions</a>
  </div>
</template>

<style scoped>
</style>