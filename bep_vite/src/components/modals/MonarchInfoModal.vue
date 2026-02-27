<script setup>
import { computed } from 'vue'
import { formattedDateRange } from '../../helpers/utils.js'
import { useMonarchsStore } from '../../stores/data.js'

const props = defineProps({
  objectId: {
    type: Number,
    required: true,
  },
})

const object = await useMonarchsStore().getById(props.objectId)
const getDate = (d) => d !== null && d != '1000-01-01' ? new Date(d) : null
const reignDateRange = computed(() => formattedDateRange([getDate(object.start_date), getDate(object.end_date)]))
</script>

<template>
  <div class="modal-header align-items-start pb-0" v-if="object">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1>{{ object.label }}</h1>
        </blockquote>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body pt-3" v-if="object">
    <div v-html="object.description"></div>

    <dl class="row" v-if="object.start_date || object.end_date">
      <dt class="col-auto">Reign:</dt>
      <dd class="col" v-if="reignDateRange">
        From {{ reignDateRange }}
      </dd>
    </dl>
  </div>
</template>

<style scoped>
</style>