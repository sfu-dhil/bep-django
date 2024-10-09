

<script setup>
import { ref, inject, onMounted, nextTick, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Style, Text, Fill, Stroke } from "ol/style"
import { useGeographic } from 'ol/proj.js'
import Timeline from 'ol-ext/control/Timeline'
import { useFilterStore } from '../stores/filter.js'
import { useMapStore } from '../stores/map.js'
import { useParishModalStore } from '../stores/modal.js'
import { isSameObjectArrayById } from '../helpers/utils'

const store = useMapStore()
const {
  center,
  zoom,
  rotation,
} = store
const {
  projection,
  parishes,
  timelineFeatures,
  timelinePlaybackStartDate,
  timelinePlaybackEndDate,
} = storeToRefs(store)
const filterStore = useFilterStore()
const {
  selectedMonarchs,
} = storeToRefs(filterStore)
const parishModalStore = useParishModalStore()
const {
  parishId: modalParishId,
  open: modalOpen,
} = storeToRefs(parishModalStore)

const mapRef = ref(null)
const timelineDate = ref(timelinePlaybackStartDate.value)
const tooltips = ref([])
const clickFeature = (event) => {
  if (event.selected.length > 0) {
    modalParishId.value = event.selected[0].get('parish').id
    modalOpen.value = true
  }
}
const overrideSelectedFeatureStyle = (feature) => [
  new Style({
      text: new Text({
          text: '\uf041',
          scale: 1,
          textBaseline: 'bottom',
          font: 'bold 1em "Font Awesome 6 Free"',
          fill: new Fill({ color: 'red' }),
          stroke: new Stroke({ color: 'black', width: 3 }),
      }),
      zIndex: Infinity,
  }),
  new Style({
      text: new Text({
          text: feature.get('parish').label,
          scale: 0.8,
          textBaseline: 'top',
          font: 'bold 1em system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
          fill: new Fill({ color: 'black' }),
          stroke: new Stroke({ color: 'white', width: 3 }),
      }),
      zIndex: Infinity,
  }),
]

const updateCenter = (event) => store.center = event.target.getCenter()
const updateZoom = (event) => store.zoom = event.target.getZoom()
const updateRotation = (event) => store.rotation = event.target.getRotation()
const getTimelineFeatureHTML = (feature) => `
  <div class="w-100 badge ${filterStore.isSelectedMonarch(feature) ? 'text-bg-primary' : 'text-bg-secondary'}"
      data-bs-title="${feature.label}"
      data-bs-toggle="tooltip"
      data-bs-placement="top"
      data-bs-custom-class="timeline-tooltip">
    ${feature.label.replace(/\s*\(.*?\)\s*/g, '')}
  </div>
`
const getTimelineFeatureStartDate = (feature) => new Date(feature.start_date)
const getTimelineFeatureEndDate = (feature) => new Date(feature.end_date)
const timelineControl = new Timeline({
  className: 'ol-pointer',
  features: timelineFeatures.value,
  graduation: 'day',
  maxWidth: 3000,
  minDate: new Date('1506-01-01'),
  maxDate: new Date('1686-12-31'),
  getHTML: getTimelineFeatureHTML,
  getFeatureDate: getTimelineFeatureStartDate,
  endFeatureDate: getTimelineFeatureEndDate,
})
timelineControl.on('select', (event) => {
  filterStore.toggleSelectedMonarch(event.feature)
})
const refreshTimeline = () => {
  for (const tooltip of tooltips.value) {
    tooltip.dispose()
  }
  timelineControl.refresh()
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  tooltips.value = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
}
watch(selectedMonarchs, (newValue, oldValue) => {
  if (!isSameObjectArrayById(newValue, oldValue)) {
    refreshTimeline()
  }
})
watch(timelineFeatures, (newValue, oldValue) => {
  if (!isSameObjectArrayById(newValue, oldValue)) {
    timelineControl.setFeatures(timelineFeatures.value, 1.0)
    refreshTimeline()
  }
})
watch(timelineDate, (newValue, oldValue) => {
  if (newValue != oldValue) {
    timelineControl.setDate(newValue, { anim: false, position: 'center' })
  }
})

const {
  pointerMove: pointerMoveCondition,
  click: clickCondition,
} = inject("ol-selectconditions")
useGeographic()

onMounted(() => {
  nextTick(() => {
    mapRef.value?.map.addControl(timelineControl)
    timelineControl.setDate(timelineDate.value, { anim: false, position: 'center' })
    refreshTimeline()
  })
})
</script>

<template>
  <div class="w-100 h-100 position-relative overflow-hidden">
    <ol-map
      ref="mapRef"
      id="dashboard-map"
      class="w-100 h-100 position-absolute"
      :loadTilesWhileAnimating="true"
      :loadTilesWhileInteracting="true"
      :controls="[]"
    >
      <ol-view
        ref="view"
        :center="center"
        :rotation="rotation"
        :zoom="zoom"
        :projection="projection"
        @change:center="updateCenter"
        @change:resolution="updateZoom"
        @change:rotation="updateRotation"
      />

      <ol-tile-layer>
        <ol-source-osm />
      </ol-tile-layer>

      <ol-interaction-select
        :condition="pointerMoveCondition"
      >
        <ol-style :overrideStyleFunction="overrideSelectedFeatureStyle"></ol-style>
      </ol-interaction-select>

      <ol-interaction-select
        @select="clickFeature"
        :condition="clickCondition"
      >
        <ol-style :overrideStyleFunction="overrideSelectedFeatureStyle"></ol-style>
      </ol-interaction-select>

      <ol-vector-layer>
        <ol-source-vector>
          <ol-feature v-for="parish in parishes" :properties="{ 'parish': parish }">
            <ol-geom-point :coordinates="[parish.longitude, parish.latitude]"></ol-geom-point>
            <ol-style>
              <ol-style-text
                text="&#xf041"
                scale="1"
                textBaseline="bottom"
                font="bold 1em 'Font Awesome 6 Free'"
                fill="#7cb341"
                :stroke="{ color: 'black', width: 3 }"
              ></ol-style-text>
            </ol-style>
          </ol-feature>
        </ol-source-vector>
      </ol-vector-layer>

      <ol-interaction-dragrotatezoom />
      <ol-zoom-control />
      <ol-rotate-control :autoHide="true" />
      <ol-attribution-control :collapsible="true" :collapsed="true" />
    </ol-map>
  </div>
</template>

<style scoped>
.options {
  min-width: 18em;
}
</style>