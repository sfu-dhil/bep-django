<script setup>
import { useArchivesStore } from '../../stores/data.js'
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

const object = await useArchivesStore().getById(props.objectId)
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
      <LinksList :links="object.links" v-if="object.links.length > 0" />
    </dl>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-secondary me-auto" v-if="useInfoModalStore().hasHistory()" @click="() => useInfoModalStore().showPrevious()">Back</button>
  </div>
</template>

<style scoped>
</style>