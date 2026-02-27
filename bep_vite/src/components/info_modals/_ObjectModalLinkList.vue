<script setup>
import { useInfoModalStore } from '../../stores/info_modal.js'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  modalType: {
    type: String,
    required: true,
  },
  objects: {
    type: Array,
    required: true,
  },
  objectLabelProperty: {
    type: String,
    default: 'label',
  },
})
</script>

<template>
  <dt class="col col-lg-2 px-0"><div class="pt-2">{{ label }}:</div></dt>
  <dd class="col col-lg-10 px-0">
    <div class="list-group">
      <button
        type="button" class="list-group-item list-group-item-action"
        v-for="object in objects"
        @click="() => useInfoModalStore().showModal(modalType, object.id, true)"
      >
        <i class="bi bi-info-circle"></i> {{ object[objectLabelProperty] }}
      </button>
    </div>
  </dd>
</template>

<style scoped>
</style>