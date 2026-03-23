<script setup>
import { useInfoModalStore } from '../../stores/info_modal.js'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  linkFunction: {
    type: Function,
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
      <a
        class="list-group-item list-group-item-action"
        :href="linkFunction(object.id)" target="_blank"
        v-for="object in objects"
      >
        <div class="row">
          <div class="col-auto"><i class="bi bi-link"></i></div>
          <div class="col" v-html="object[objectLabelProperty]" />
        </div>
      </a>
    </div>
  </dd>
</template>

<style scoped>
</style>