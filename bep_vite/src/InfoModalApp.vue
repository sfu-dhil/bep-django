<script setup>
import { watch, ref, onMounted, onUnmounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useInfoModalStore } from './stores/info_modal.js'
import MonarchInfoModal from './components/modals/MonarchInfoModal.vue'
import NationInfoModal from './components/modals/NationInfoModal.vue'
import ParishInfoModal from './components/modals/ParishInfoModal.vue'
import LoadingDots from './components/LoadingDots.vue'
import { Modal } from 'bootstrap/dist/js/bootstrap.esm'

const store = useInfoModalStore()
const {
  objectId,
  objectType,
  open,
} = storeToRefs(store)

const bootstrapModal = ref(null)
const modalElRef = ref(null)

watch(open, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (open.value) {
      bootstrapModal.value?.show()
    } else {
      bootstrapModal.value?.hide()
      objectId.value = null
    }
  }
})
watch(objectId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    nextTick(() => bootstrapModal.value?.handleUpdate())
  }
})
watch(objectType, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    nextTick(() => bootstrapModal.value?.handleUpdate())
  }
})
const modalShown = () => open.value = true
const modalHidden = () => open.value = false

onMounted(() => {
  nextTick(() => {
    modalElRef.value.addEventListener('hidden.bs.modal', modalHidden)
    modalElRef.value.addEventListener('shown.bs.modal', modalShown)
    bootstrapModal.value = new Modal(modalElRef.value)
    if (open.value) { bootstrapModal.value.show() }
  })
})
onUnmounted(() => {
  modalElRef.value.removeEventListener('hidden.bs.modal', modalHidden)
  modalElRef.value.addEventListener('shown.bs.modal', modalShown)
  bootstrapModal.value.dispose()
  bootstrapModal.value = null
  open.value = false
})
</script>

<template>
  <div ref="modalElRef" class="modal fade" data-bs-backdrop="static" tabindex="-1">
    <div class="modal-dialog modal-fullscreen-lg-down modal-xl modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <Suspense v-if="objectType == 'monarch' && objectId">
          <MonarchInfoModal :objectId="objectId"></MonarchInfoModal>
          <template #fallback>
            <LoadingDots :show="true"></LoadingDots>
          </template>
        </Suspense>
        <Suspense v-if="objectType == 'nation' && objectId">
          <NationInfoModal :objectId="objectId"></NationInfoModal>
          <template #fallback>
            <LoadingDots :show="true"></LoadingDots>
          </template>
        </Suspense>
        <Suspense v-if="objectType == 'parish' && objectId">
          <ParishInfoModal :objectId="objectId"></ParishInfoModal>
          <template #fallback>
            <LoadingDots :show="true"></LoadingDots>
          </template>
        </Suspense>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>