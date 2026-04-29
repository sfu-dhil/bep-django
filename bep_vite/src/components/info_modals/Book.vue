<script setup>
import { useBooksStore } from '../../stores/data.js'
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

const object = await useBooksStore().getById(props.objectId)
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1 v-if="object.full_title" v-html="object.full_title" />
          <h1 v-if="!object.full_title" v-html="object.title" />
        </blockquote>
        <figcaption class="blockquote-footer" v-if="object.title && object.full_title" v-html="object.title" />
        <figcaption class="blockquote-footer" v-for="variant_title in object.variant_titles" v-html="variant_title" />
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body py-0">
    <div class="pt-3" v-if="object.description" v-html="object.description" />

    <dl class="row gy-3 m-0 row-cols-1 row-cols-lg-2">
      <ObjectModalLinkList label="Monarch" modal-type="monarch" :objects="[object.monarch]" v-if="object.monarch" />
      <BasicDetail label="Author" :value="object.author" v-if="object.author" />
      <BasicDetail label="Imprint" :value="object.imprint" v-if="object.imprint" />
      <BasicDetail label="Variant Imprint" :value="object.variant_imprint" v-if="object.variant_imprint" />
      <BasicDetail label="Date" :value="object.date" v-if="object.date" />
      <BasicDetail label="Estc" :value="object.estc" v-if="object.estc" />
      <BasicDetail label="Physical Description" :value="object.physical_description" v-if="object.physical_description" />
      <BasicDetail label="Notes" :value="object.notes" v-if="object.notes" />
      <LinksList :links="object.links" v-if="object.links.length > 0" />
    </dl>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-secondary me-auto" v-if="useInfoModalStore().hasHistory()" @click="() => useInfoModalStore().showPrevious()">Back</button>
    <a :href="`/transactions?book=${object.id}`" class="btn btn-primary ms-auto">View All Transactions</a>
  </div>
</template>

<style scoped>
</style>