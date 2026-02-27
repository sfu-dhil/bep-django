<script setup>
import { useInfoModalStore } from './stores/info_modal.js'

const props = defineProps({
  objectType: {
    type: String,
    required: true,
  },
  objectId: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
})

const openModal = () => useInfoModalStore().showModal(props.objectType, parseInt(props.objectId))
</script>

<template>
  <div @click="openModal" v-html="label"></div>
</template>

<style scoped>
</style>