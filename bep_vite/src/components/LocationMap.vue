

<script setup>
import { ref, watch, inject, nextTick, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { Style, Text, Fill, Stroke, Circle } from "ol/style"
import { useGeographic } from 'ol/proj.js'
import { createEmpty, extend } from 'ol/extent.js';
import GeoJSON from 'ol/format/GeoJSON'
import { useLocationMapStore } from '../stores/map/location.js'
import { useInfoModalStore } from '../stores/info_modals.js'
import { useParishesStore } from '../stores/data/parishes.js'
import FilterSingleSelect from './FilterSingleSelect.vue'
// import DiocesePre1541 from '../assets/diocese_pre_1541.json?url'
import DiocesePost1541 from '../assets/diocese_post_1541.json?url'

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
  listedDiocesesSet,
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
const sourceClusterRef = ref(null)
const diocesePost1541SourceVectorRef = ref(null)
const geoJson = new GeoJSON()

const isCluster = (feature) => !!feature.get('features')
const isRegion = (feature) => !isCluster(feature)
const clickCluster = (event) => {
  if (event.selected.length == 1) {
    const feature = event.selected[0]
    const features = feature.get('features')
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
const clusterGroupingStyle = (features, active) => {
  return [
    new Style({
      image: new Circle({
        radius: 10,
        fill: new Fill({ color: active ? 'red' : '#7cb341' }),
        stroke: new Stroke({ color: 'black', width: 1 }),
      }),
      text: new Text({
        text: `${features.length}`,
        fill: new Fill({ color: '#fff' }),
      }),
      zIndex: active ? Infinity : undefined,
    }),
  ]
}
const clusterPointStyle = (feature, active) => {
  const parish = parishesMap.value.get(feature.get('id'))
  return [
    new Style({
      text: new Text({
        text: '\uf041',
        scale: 1,
        textBaseline: 'bottom',
        font: 'bold 1em "Font Awesome 6 Free"',
        fill: new Fill({ color: active ? 'red' : '#7cb341' }),
        stroke: new Stroke({ color: 'black', width: 3 }),
      }),
      zIndex: active ? Infinity : undefined,
    }),
    new Style({
      text: new Text({
        text: `${parish.label}`,
        textBaseline: 'top',
        font: 'bold 0.6em system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
        fill: new Fill({ color: 'black' }),
        stroke: new Stroke({ color: 'white', width: 3 }),
      }),
      zIndex: active ? Infinity : -1,
    }),
  ]
}
const overrideClusterStyle = (feature) => {
  const features = feature.get('features')
  if (features.length > 1) {
    return clusterGroupingStyle(features, false)
  } else if (features.length == 1) {
    return clusterPointStyle(features[0], false)
  }
  return new Style()
}
const overrideSelectedClusterStyle = (feature) => {
  const features = feature.get('features')
  if (features.length > 1) {
    return clusterGroupingStyle(features, true)
  } else if (features.length == 1) {
    return clusterPointStyle(features[0], true)
  }
  return new Style()
}
const dioceseRegionStyle = (feature, active) => {
  active = active || (selectedDioceseId.value && selectedDioceseId.value == feature.get('pk'))
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
    text: new Text({
      text: `${feature.get('name')}`,
      font: 'bold 0.5em system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
      fill: new Fill({ color: 'black' }),
      stroke: new Stroke({ color: 'white', width: 3 }),
    }),
    zIndex: active ? Infinity : undefined,
  })
}
const overrideRegionsFunction = (feature) => {
  if (['diocese_post_1541', 'diocese_pre_1541'].includes(feature.get('type'))) {
    return dioceseRegionStyle(feature, false)
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
    nextTick(() => {
      sourceClusterRef.value?.source.getSource().changed()
      diocesePost1541SourceVectorRef.value?.source.changed()
    })
  }
}
watch(selectedNationId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedProvinceId.value = null
    selectedDioceseId.value = null
    selectedArchdeaconryId.value = null
    selectedParishId.value = null
  }
  updateFilters(newValue, oldValue)
})
watch(selectedProvinceId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedDioceseId.value = null
    selectedArchdeaconryId.value = null
    selectedParishId.value = null
  }
  updateFilters(newValue, oldValue)
})
watch(listedDiocesesSet, updateFilters)
watch(selectedDioceseId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedArchdeaconryId.value = null
    selectedParishId.value = null
  }
  updateFilters(newValue, oldValue)
})
watch(selectedArchdeaconryId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedParishId.value = null
  }
  updateFilters(newValue, oldValue)
})
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
        :filter="isCluster"
      >
        <ol-style :overrideStyleFunction="overrideSelectedClusterStyle"></ol-style>
      </ol-interaction-select>
      <ol-interaction-select
        @select="clickCluster"
        :condition="clickCondition"
        :filter="isCluster"
      >
        <ol-style :overrideStyleFunction="overrideSelectedClusterStyle"></ol-style>
      </ol-interaction-select>

      <ol-vector-layer>
        <ol-source-vector ref="diocesePost1541SourceVectorRef" :url="DiocesePost1541" :format="geoJson">
          <ol-style :overrideStyleFunction="overrideRegionsFunction"></ol-style>
        </ol-source-vector>
      </ol-vector-layer>
      <ol-vector-layer v-if="points.length > 0">
        <ol-source-cluster ref="sourceClusterRef" :distance="20" :geometryFunction="overrideGeometryFunction">
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