<script setup>
import { watch } from 'vue'
import { useFilterStore } from '../stores/filter.js'
import { isSameObjectArrayById } from '../helpers/utils'

const store = useFilterStore()

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  objectId: {
    type: String,
    default: 'id',
  },
  objectLabel: {
    type: String,
    default: 'label',
  },
})
const selected = defineModel('selected')
const listed = defineModel('listed')
const selectAll = () => {
  selected.value = listed.value
}
const clearAll = () => {
  selected.value = []
}

watch(selected, (newValue, oldValue) => {
  if (!isSameObjectArrayById(newValue, oldValue)) {
    store.updateFilters()
  }
})
</script>

<template>
  <div class="input-group mb-3">
    <div class="input-group-text">
      {{ label }}
    </div>
    <multiselect
        v-model="selected"
        :options="listed"
        :multiple="true"
        :close-on-select="false"
        :placeholder="`Select a ${label}`"
        :limitText="(count) => `and ${count} other items`"
        :limit="5"
        :label="objectLabel"
        :track-by="objectId"
        :show-labels="false"
    >
      <template #clear="props">
        <i class="bi bi-x-lg fw-bold fs-6 multiselect__clear" title="Clear all" v-if="selected.length" @mousedown.prevent.stop="clearAll()"></i>
      </template>
    </multiselect>
    <!-- <button class="btn btn-outline-secondary" type="button" @click="selectAll">All</button> -->
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
</style>