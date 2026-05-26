<script setup>
import { ref, computed } from 'vue'
import { Style, Fill, Stroke } from "ol/style"
import { MVT } from 'ol/format.js'
import { useGeographic } from 'ol/proj.js'

const mvt = new MVT()

const props = defineProps({
  countyId: {
    type: String,
    required: true,
  },
})
const center = ref([-2, 53])
const zoom = ref(5.5)
const projection = ref('EPSG:3857')
const rotation = ref(0)

const websiteOrigin = window.location.origin

const countyRegionStyle = (feature) => {
  if (feature.get('id') != parseInt(props.countyId)) {
    return new Style({})
  }
  const active = true
  const activeFill = new Fill({
    color: 'rgba(0, 0, 255, 0.1)',
  })
  return new Style({
    stroke: new Stroke({
      color: 'blue',
      lineDash:[4],
      width: active ? 2 : 1,
    }),
    fill: active ? activeFill : null,
    zIndex: active ? Infinity : undefined,
  })
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

      <ol-vector-tile-layer ref="countyTileLayerRef"
          :renderMode="'vector'" :updateWhileAnimating="true" :updateWhileInteracting="true" :visible="true"
          :properties="{ 'name': 'Counties' }">
        <ol-source-vector-tile :url="websiteOrigin+'/api/geo/counties/tiles/{z}/{x}/{y}'" :format="mvt">
          <ol-style :overrideStyleFunction="countyRegionStyle"></ol-style>
        </ol-source-vector-tile>
      </ol-vector-tile-layer>

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