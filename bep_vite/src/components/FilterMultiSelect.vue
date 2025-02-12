<script setup>
const props = defineProps({
  label: {
    type: String,
    required: false,
  },
  placeholder: {
    type: String,
    required: false,
  },
})
const selected = defineModel('selected')
const listed = defineModel('listed')
// const selectAll = () => {
//   selected.value = listed.value
// }
const clear = () => {
  selected.value = []
}
</script>

<template>
  <div class="input-group">
    <div class="input-group-text" v-if="label">{{ label }}</div>
    <multiselect
        v-model="selected"
        :options="listed.map((o) => o.id)"
        :custom-label="(id) => listed.find((o) => o.id === id)?.label"
        :multiple="true"
        :close-on-select="false"
        :placeholder="placeholder"
        :limitText="(count) => `and ${count} other items`"
        :limit="5"
        :show-labels="false"
    >
      <template #clear="props">
        <i class="bi bi-x-lg fw-bold fs-6 multiselect__clear" title="Clear all" v-if="selected.length" @mousedown.prevent.stop="clear()"></i>
      </template>
    </multiselect>
    <!-- <button class="btn btn-outline-secondary" type="button" @click="selectAll">All</button> -->
  </div>
</template>

<style scoped>
</style>