<script setup>
import { watch, ref, onMounted, onUnmounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useInfoModalStore } from './stores/info_modal.js'
import Monarch from './components/info_modals/Monarch.vue'
import Nation from './components/info_modals/Nation.vue'
import Province from './components/info_modals/Province.vue'
import Archdeaconry from './components/info_modals/Archdeaconry.vue'
import Town from './components/info_modals/Town.vue'
import Parish from './components/info_modals/Parish.vue'
import TransactionAction from './components/info_modals/TransactionAction.vue'
import TransactionMedium from './components/info_modals/TransactionMedium.vue'
import SourceCategory from './components/info_modals/SourceCategory.vue'
import PrintSource from './components/info_modals/PrintSource.vue'
import ManuscriptSource from './components/info_modals/ManuscriptSource.vue'
import Archive from './components/info_modals/Archive.vue'
import Injunction from './components/info_modals/Injunction.vue'
import YearEvents from './components/info_modals/YearEvents.vue'
import Book from './components/info_modals/Book.vue'
import LoadingDots from './components/LoadingDots.vue'
import { Modal } from 'bootstrap/dist/js/bootstrap.esm'

const store = useInfoModalStore()
const {
  objectId,
  objectType,
  open,
  params,
} = storeToRefs(store)

const bootstrapModal = ref(null)
const modalElRef = ref(null)

watch(open, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (open.value) {
      bootstrapModal.value?.show()
    } else {
      bootstrapModal.value?.hide()
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
const modalHidden = () => store.reset()

onMounted(() => {
  nextTick(() => {
    modalElRef.value?.addEventListener('hidden.bs.modal', modalHidden)
    modalElRef.value?.addEventListener('shown.bs.modal', modalShown)
    bootstrapModal.value = new Modal(modalElRef.value)
    if (open.value) { bootstrapModal.value.show() }
  })
})
onUnmounted(() => {
  modalElRef.value?.removeEventListener('hidden.bs.modal', modalHidden)
  modalElRef.value?.addEventListener('shown.bs.modal', modalShown)
  bootstrapModal.value?.dispose()
  bootstrapModal.value = null
  store.reset()
})
</script>

<template>
  <div ref="modalElRef" class="modal fade" tabindex="-1">
    <div class="modal-dialog modal-fullscreen-lg-down modal-xl modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <Suspense v-if="objectType == 'monarch'">
          <Monarch :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'nation'">
          <Nation :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'province'">
          <Province :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'archdeaconry'">
          <Archdeaconry :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'town'">
          <Town :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'parish'">
          <Parish :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'transaction_action'">
          <TransactionAction :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'transaction_medium'">
          <TransactionMedium :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'book'">
          <Book :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'source_category'">
          <SourceCategory :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'print_source'">
          <PrintSource :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'manuscript_source'">
          <ManuscriptSource :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'archive'">
          <Archive :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'injunction'">
          <Injunction :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'year_events'">
          <YearEvents :objectId="objectId" :params="params" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-content {
  min-height: 150px;
}
</style>