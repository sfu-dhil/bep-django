<script setup>
import { watch, ref, onMounted, onUnmounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useInfoModalStore } from '../../stores/info_modals.js'
import ParishDetailModal from './ParishDetailModal.vue'

const store = useInfoModalStore()
const {
  objectId,
  objectType,
  object,
  open,
} = storeToRefs(store)

const modal = ref(null)

watch(open, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (open.value) {
      modal.value?.show()
    } else {
      modal.value?.hide()
      objectId.value = null
    }
  }
})
watch(objectId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    nextTick(() => modal.value?.handleUpdate())
  }
})
watch(objectType, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    nextTick(() => modal.value?.handleUpdate())
  }
})
const modalShown = () => open.value = true
const modalHidden = () => open.value = false

onMounted(() => {
  nextTick(() => {
    const modalEl = document.getElementById('info-modal')
    modalEl.addEventListener('hidden.bs.modal', modalHidden)
    modalEl.addEventListener('shown.bs.modal', modalShown)
    modal.value = new bootstrap.Modal(modalEl)
    if (open.value) { modal.value.show() }
  })
})
onUnmounted(() => {
  const modalEl = document.getElementById('info-modal')
  modalEl.removeEventListener('hidden.bs.modal', modalHidden)
  modalEl.addEventListener('shown.bs.modal', modalShown)
  modal.value.dispose()
  modal.value = null
  open.value = false
})
</script>

<template>
  <div id="info-modal" class="modal fade" data-bs-backdrop="static" tabindex="-1">
    <div class="modal-dialog modal-fullscreen-lg-down modal-lg modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <ParishDetailModal :parish="object" v-if="objectType == 'parish'"></ParishDetailModal>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>