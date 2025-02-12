

<script setup>
import { ref, inject, onMounted, nextTick, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Style, Text, Fill, Stroke } from "ol/style"
import { useGeographic } from 'ol/proj.js'
import { useFilterStore } from '../stores/filter.js'
import { useMapStore } from '../stores/map.js'
import { useParishModalStore } from '../stores/modal.js'

const store = useMapStore()
const {
  center,
  zoom,
  rotation,
} = store
const {
  projection,
  parishes,
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
const {
  pointerMove: pointerMoveCondition,
  click: clickCondition,
} = inject("ol-selectconditions")
useGeographic()
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