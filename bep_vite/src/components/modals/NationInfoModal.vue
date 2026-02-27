<script setup>
import { useNationsStore } from '../../stores/data.js'

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
          <h1>{{ object.label }}</h1>
        </blockquote>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body pt-3">
    <div v-html="object.description"></div>
  </div>
</template>

<style scoped>
</style>