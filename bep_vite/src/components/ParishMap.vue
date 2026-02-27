<script setup>
import { ref } from 'vue'
import { Style, Text, Fill, Stroke } from "ol/style"
import { useGeographic } from 'ol/proj.js'
import { useParishesStore } from '../stores/data.js'

const props = defineProps({
  parishId: {
    type: Number,
    required: true,
  },
})
const parish = await useParishesStore().getById(props.parishId)
const center = ref(parish.coordinates || [-2, 53])
const zoom = ref(7.5)
const projection = ref('EPSG:3857')
const rotation = ref(0)

const overrideFeatureStyle = (feature) => {
  return [
    new Style({
      text: new Text({
          text: '\uf041',
          scale: 1,
          textBaseline: 'bottom',
          font: 'bold 1em "Font Awesome 7 Free"',
          fill: new Fill({ color: '#7cb341' }),
          stroke: new Stroke({ color: 'black', width: 3 }),
      }),
    }),
    new Style({
      text: new Text({
          text: `${parish.label}`,
          textBaseline: 'top',
          font: 'bold 0.6em system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
          fill: new Fill({ color: 'black' }),
          stroke: new Stroke({ color: 'white', width: 3 }),
      }),
      zIndex: -1,
    }),
  ]
}
useGeographic()
</script>

<template>
  <div class="w-100 h-100 position-relative overflow-hidden">
    <ol-map
      class="w-100 h-100 position-absolute z-0"
      :loadTilesWhileAnimating="true"
      :loadTilesWhileInteracting="true"
      :controls="[]"
    >
      <ol-view
        :center="center"
        :rotation="rotation"
        :zoom="zoom"
        :projection="projection"
      />

      <ol-tile-layer>
        <ol-source-osm />
      </ol-tile-layer>

      <ol-vector-layer>
        <ol-source-vector>
          <ol-feature v-if="parish && parish.id" :key="parish.id">
            <ol-geom-point :coordinates="parish.coordinates"></ol-geom-point>
            <ol-style :overrideStyleFunction="overrideFeatureStyle"></ol-style>
          </ol-feature>
        </ol-source-vector>
      </ol-vector-layer>

      <ol-interaction-drag-rotate-and-zoom  />
      <ol-zoom-control />
      <ol-rotate-control :autoHide="true" />
      <ol-full-screen-control />
      <ol-scale-line-control />
      <ol-attribution-control :collapsible="true" :collapsed="true" />
    </ol-map>
  </div>
</template>

<style scoped>
</style>