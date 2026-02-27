<script setup>
import { useNationsStore } from '../../stores/data.js'
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

const object = await useNationsStore().getById(props.objectId)
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
      <ObjectModalLinkList label="Injunctions" modal-type="injunction" :objects="object.injunctions" v-if="object.injunctions.length > 0" objectLabelProperty="title" />
      <ObjectModalLinkList label="Provinces" modal-type="province" :objects="object.provinces" v-if="object.provinces.length > 0" />
      <ObjectLinkList label="Counties" :link-function="(id) => `/counties/${id}`" :objects="object.counties" v-if="object.counties.length > 0" />
    </dl>
  </div>
  <div class="modal-footer" v-if="useInfoModalStore().hasHistory()">
    <button type="button" class="btn btn-secondary me-auto" @click="() => useInfoModalStore().showPrevious()">Back</button>
  </div>
</template>

<style scoped>
</style>