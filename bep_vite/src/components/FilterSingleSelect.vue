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
const clear = () => {
  selected.value = null
}
</script>

<template>
  <div class="input-group">
    <div class="input-group-text" v-if="label">{{ label }}</div>
    <!-- https://github.com/shentao/vue-multiselect/issues/1464#issuecomment-1814672480 -->
    <multiselect
        v-model="selected"
        :options="listed.map((o) => o.id)"
        :custom-label="(id) => listed.find((o) => o.id === id)?.label"
        :placeholder="placeholder"
        :show-labels="false"
    >
      <template #clear="props">
        <i class="bi bi-x-lg fw-bold fs-6 multiselect__clear" title="Clear all" v-if="selected" @mousedown.prevent.stop="clear()"></i>
      </template>
    </multiselect>
  </div>
</template>

<style scoped>
</style>