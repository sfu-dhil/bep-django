

<script setup>
import { ref, watch, inject, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { Style, Text, Fill, Stroke, Circle } from "ol/style"
import FilterSingleSelect from './FilterSingleSelect.vue'
import { useGeographic } from 'ol/proj.js'
import { createEmpty, extend } from 'ol/extent.js';
import { useLocationMapStore } from '../stores/map/location.js'
import { useInfoModalStore } from '../stores/info_modals.js'
import { useParishesStore } from '../stores/data/parishes.js'

const store = useLocationMapStore()
const {
  center,
  zoom,
  rotation,
} = store
const {
  projection,
  points,
  listedNations,
  selectedNationId,
  listedProvinces,
  selectedProvinceId,
  listedDioceses,
  selectedDioceseId,
  listedArchdeaconries,
  selectedArchdeaconryId,
  listedParishes,
  listedParishesSet,
  selectedParishId,
} = storeToRefs(store)
const infoModalStore = useInfoModalStore()
const parishesStore = useParishesStore()
const {
  parishesMap,
} = storeToRefs(parishesStore)

const mapRef = ref(null)
const viewRef = ref(null)
const clusterSourceRef = ref(null)
const clickFeature = (event) => {
  if (event.selected.length == 1) {
    const features = event.selected[0].get('features')
    if (features.length > 1) {
      // zoom to fit cluster within extent
      const extent = createEmpty()
      features.forEach((feature) => extend(extent, feature.getGeometry().getExtent()))
      const paddingX = mapRef.value?.map.getSize()[0]/10
      const paddingY = mapRef.value?.map.getSize()[1]/10
      viewRef.value?.view.fit(extent, {duration: 500, nearest: true, padding: [paddingY, paddingX, paddingY, paddingX]})
    } else if (features.length == 1) {
      const parish = parishesMap.value.get(features[0].get('id'))
      if (parish) {
        infoModalStore.showModal('parish', parish.id)
      }
    }
  }
}
const isShown = (id) => selectedParishId.value ? selectedParishId.value == id : listedParishesSet.value.has(id)
const overrideGeometryFunction = (feature) => isShown(feature.get('id')) ? feature.getGeometry() : null
const overrideClusterStyle = (feature) => {
  const features = feature.get('features')
  if (features.length > 1) {
    return [
      new Style({
        image: new Circle({
          radius: 10,
          fill: new Fill({ color: '#7cb341' }),
          stroke: new Stroke({ color: 'black', width: 1 }),
        }),
        text: new Text({
          text: `${features.length}`,
          fill: new Fill({ color: '#fff' }),
        }),
      }),
    ]
  } else if (features.length == 1) {
    const parish = parishesMap.value.get(features[0].get('id'))
    return [
      new Style({
        text: new Text({
          text: '\uf041',
          scale: 1,
          textBaseline: 'bottom',
          font: 'bold 1em "Font Awesome 6 Free"',
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
  return new Style()
}
const overrideSelectedFeatureStyle = (feature) => {
  const features = feature.get('features')
  if (features.length > 1) {
    return [
      new Style({
        image: new Circle({
          radius: 10,
          fill: new Fill({ color: 'red' }),
          stroke: new Stroke({ color: 'black', width: 1 }),
        }),
        text: new Text({
            text: `${features.length}`,
            fill: new Fill({ color: '#fff' }),
        }),
        zIndex: Infinity,
      }),
    ]
  } else if (features.length == 1) {
    const parish = parishesMap.value.get(features[0].get('id'))
    return [
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
          text: `${parish.label}`,
          textBaseline: 'top',
          font: 'bold 0.6em system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
          fill: new Fill({ color: 'black' }),
          stroke: new Stroke({ color: 'white', width: 3 }),
        }),
        zIndex: Infinity,
      }),
    ]
  }
  return new Style()
}

const updateCenter = (event) => store.center = event.target.getCenter()
const updateZoom = (event) => store.zoom = event.target.getZoom()
const updateRotation = (event) => store.rotation = event.target.getRotation()
const {
  pointerMove: pointerMoveCondition,
  click: clickCondition,
} = inject("ol-selectconditions")
useGeographic()

const updateFilters = (newValue, oldValue) => {
  if (newValue !== oldValue) {
    store.updateFilters()
    nextTick(() => clusterSourceRef.value?.source.getSource().changed())
  }
}
watch(selectedNationId, updateFilters)
watch(selectedProvinceId, updateFilters)
watch(selectedDioceseId, updateFilters)
watch(selectedArchdeaconryId, updateFilters)
watch(selectedParishId, updateFilters)
</script>

<template>
  <div class="w-100 h-100 position-relative overflow-hidden">
    <ol-map
      ref="mapRef"
      class="w-100 h-100 position-absolute z-0"
      :loadTilesWhileAnimating="true"
      :loadTilesWhileInteracting="true"
      :controls="[]"
    >
      <ol-view
        ref="viewRef"
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
      <ol-vector-layer v-if="points.length > 0">
        <ol-source-cluster ref="clusterSourceRef" :distance="20" :geometryFunction="overrideGeometryFunction">
          <ol-source-vector>
            <ol-feature v-for="point in points" :key="point.id" :properties="{ 'id': point.id }">
              <ol-geom-point :coordinates="point.coordinates"></ol-geom-point>
            </ol-feature>
          </ol-source-vector>
          <ol-style :overrideStyleFunction="overrideClusterStyle"></ol-style>
        </ol-source-cluster>
      </ol-vector-layer>

      <ol-interaction-dragrotatezoom />
      <ol-zoom-control />
      <ol-rotate-control :autoHide="true" />
      <ol-fullscreen-control />
      <ol-scaleline-control />
      <ol-attribution-control :collapsible="true" :collapsed="true" />
    </ol-map>
    <FilterSingleSelect
      v-model:selected="selectedNationId"
      v-model:listed="listedNations"
      placeholder="Select a Nation"
      class="position-absolute filter select-nation"
    ></FilterSingleSelect>
    <FilterSingleSelect
      v-model:selected="selectedProvinceId"
      v-model:listed="listedProvinces"
      placeholder="Select a Province"
      class="position-absolute filter select-province"
      v-if="selectedNationId"
    ></FilterSingleSelect>
    <FilterSingleSelect
      v-model:selected="selectedDioceseId"
      v-model:listed="listedDioceses"
      placeholder="Select a Diocese"
      class="position-absolute filter select-diocese"
      v-if="selectedNationId && selectedProvinceId"
    ></FilterSingleSelect>
    <FilterSingleSelect
      v-model:selected="selectedArchdeaconryId"
      v-model:listed="listedArchdeaconries"
      placeholder="Select an Archdeaconry or Peculiar Court"
      class="position-absolute filter select-archdeaconry"
      v-if="selectedNationId && selectedProvinceId && selectedDioceseId"
    ></FilterSingleSelect>
    <FilterSingleSelect
      v-model:selected="selectedParishId"
      v-model:listed="listedParishes"
      placeholder="Select a Parish"
      class="position-absolute filter select-parish"
      v-if="selectedNationId && selectedProvinceId && selectedDioceseId && selectedArchdeaconryId"
    ></FilterSingleSelect>
  </div>
</template>

<style scoped>
.filter {
  left: .5em;
  position: absolute !important;
  width: fit-content !important;
}
.select-nation {
  top: 4.0em;
}
.select-province {
  top: 7em;
}
.select-diocese {
  top: 10em;
}
.select-archdeaconry {
  top: 13.0em;
}
.select-parish {
  top: 16.0em;
}
</style>