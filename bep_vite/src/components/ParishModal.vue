<script setup>
import { watch, ref, onMounted, onUnmounted, nextTick, } from 'vue'
import { storeToRefs } from 'pinia'
import { useParishModalStore } from '../stores/modal.js'
import { useFilterStore } from '../stores/filter.js'
import { useData } from '../stores/data.js'
import ParishModalList from './ParishModalList.vue'

const store = useParishModalStore()
const {
  parishId,
  parish,
  open,
  transactions,
  inventories,
  holdings,
} = storeToRefs(store)
const filterStore = useFilterStore()
const {
  bookRecordToggle,
} = storeToRefs(filterStore)
const {
  bookMap,
} = useData()

const modal = ref(null)

watch(open, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (open.value) {
      modal.value?.show()
    } else {
      modal.value?.hide()
      parishId.value = null
    }
  }
})
watch(parishId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    nextTick(() => {
      modal.value?.handleUpdate()
    })
  }
})
const modalShown = () => open.value = true
const modalHidden = () => open.value = false

const clickTab = (tabValue) => {
  bookRecordToggle.value = tabValue
}

onMounted(() => {
  nextTick(() => {
    const modalEl = document.getElementById('parish-modal')
    modalEl.addEventListener('hidden.bs.modal', modalHidden)
    modalEl.addEventListener('shown.bs.modal', modalShown)

    modal.value = new bootstrap.Modal(modalEl)
    if (open.value) {
      modal.value.show()
    }
  })
})
onUnmounted(() => {
  const modalEl = document.getElementById('parish-modal')
  modalEl.removeEventListener('hidden.bs.modal', modalHidden)
  modalEl.addEventListener('shown.bs.modal', modalShown)
  modal.value.dispose()
  modal.value = null
  open.value = false
})
</script>

<template>
  <div id="parish-modal" class="modal fade" data-bs-backdrop="static" tabindex="-1">
    <div class="modal-dialog modal-fullscreen-lg-down modal-lg modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header align-items-start">
          <div class="modal-title">
            <figure>
              <blockquote class="blockquote">
                <h1>{{ parish?.label }}</h1>
              </blockquote>
              <figcaption class="blockquote-footer" v-if="parish?.address">
                {{ parish?.address }}
              </figcaption>
            </figure>
          </div>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-html="parish?.description"></div>

          <dl class="row" v-if="parish?.links">
            <dt class="col-sm-2">Links</dt>
            <dd class="col-sm-10">
              <div v-for="link in parish?.links">
                <a :href="link" target="_blank">{{ link }}</a>
              </div>
            </dd>
          </dl>

          <ul class="nav nav-pills">
            <li class="parish-tabs nav-item">
              <button class="nav-link" :class="bookRecordToggle == 'inventory' ? 'active' : ''" type="button"
                      data-bs-toggle="tab" data-bs-target="#parish-inventory-pane" @click="clickTab('inventory')">
                Inventories ({{ inventories.length }})
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="bookRecordToggle == 'transaction' ? 'active' : ''" type="button"
                      data-bs-toggle="tab" data-bs-target="#parish-transaction-pane" @click="clickTab('transaction')">
                Transactions ({{ transactions.length }})
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="bookRecordToggle == 'holding' ? 'active' : ''" type="button"
                      data-bs-toggle="tab" data-bs-target="#parish-holding-pane" @click="clickTab('holding')">
                Surviving Texts ({{ holdings.length }})
              </button>
            </li>
          </ul>
          <div class="tab-content">
            <div id="parish-inventory-pane" tabindex="0" class="tab-pane fade" :class="bookRecordToggle == 'inventory' ? 'show active' : ''">
              <ParishModalList :list="inventories" caption="List of inventory records"></ParishModalList>
            </div>
            <div id="parish-transaction-pane" tabindex="0" class="tab-pane fade" :class="bookRecordToggle == 'transaction' ? 'show active' : ''">
              <ParishModalList :list="transactions" caption="List of transaction records"></ParishModalList>
            </div>
            <div id="parish-holding-pane" tabindex="0" class="tab-pane fade" :class="bookRecordToggle == 'holding' ? 'show active' : ''">
              <ParishModalList :list="holdings" caption="List of surviving text records"></ParishModalList>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.multiselect__clear {
  cursor: pointer;
  display: inline-block;
  position: absolute;
  top: 0.5em;
  right: 2em;
}


#parish-modal .modal-title .blockquote-footer::before {
  content: none;
}
</style>