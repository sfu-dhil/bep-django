<script setup>
import { ref, watch, inject, nextTick, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { Style, Text, Fill, Stroke, Circle } from "ol/style"
import { useGeographic } from 'ol/proj.js'
import { createEmpty, extend } from 'ol/extent.js'
import { MVT, GeoJSON } from 'ol/format.js'
import { useLocationMapStore } from '../stores/location.js'
import { useInfoModalStore } from '../stores/info_modal.js'
import FilterSingleSelect from './FilterSingleSelect.vue'
import {
  // useNationsStore,
  // useProvincesStore,
  // useDiocesesStore,
  // useArchdeaconriesStore,
  useCountiesStore,
  // useTownsStore,
  useParishesStore,
} from '../stores/data.js'
import {
    // filterByNationId,
    // filterByProvinceId,
    // filterByDioceseId,
    // filterByArchdeaconryId,
    filterByCountyId,
    // filterByTownId,
} from '../helpers/utils.js'

const mvt = new MVT()
const geoJson = new GeoJSON()

const locationStore = useLocationMapStore()
const {
  center,
  zoom,
  rotation,
  diocesePre1541Visible,
  diocesePost1541Visible,
} = locationStore
const {
  projection,
  // selectedNationId,
  // selectedProvinceId,
  // selectedDioceseId,
  // selectedArchdeaconryId,
  selectedCountyId,
  // selectedTownId,
  selectedParishId,
} = storeToRefs(locationStore)

const mapRef = ref(null)
const viewRef = ref(null)
const parishSourceClusterRef = ref(null)
const parishSourceVectorRef = ref(null)
const diocesePre1541TileLayerRef = ref(null)
const diocesePost1541TileLayerRef = ref(null)
const websiteOrigin = window.location.origin

// const nations = await useNationsStore().getAll()
// const listedNations = computed(() => nations)
// const provinces = await useProvincesStore().getAll()
// const listedProvinces = computed(() => provinces.filter(filterByNationId(selectedNationId.value)))
// const dioceses = await useDiocesesStore().getAll()
// const listedDioceses = computed(() => dioceses.filter((o) => filterByNationId(selectedNationId.value)(o) && filterByProvinceId(selectedProvinceId.value)(o)))
// const archdeaconries = await useArchdeaconriesStore().getAll()
// const listedArchdeaconries = computed(() => archdeaconries.filter((o) => filterByNationId(selectedNationId.value)(o) && filterByProvinceId(selectedProvinceId.value)(o) && filterByDioceseId(selectedDioceseId.value)(o)))
const counties = await useCountiesStore().getAll()
// const listedCounties = computed(() => counties.filter(filterByNationId(selectedNationId.value)))
const listedCounties = computed(() => counties)
// const towns = await useTownsStore().getAll()
// const listedTowns = computed(() => towns.filter((o) => filterByNationId(selectedNationId.value)(o) && filterByCountyId(selectedCountyId.value)(o)))
const parishes = await useParishesStore().getAll()
const listedParishes = computed(() => parishes.filter(filterByCountyId(selectedCountyId.value)))

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
      useInfoModalStore().showModal('parish', features[0].getId())
    }
  }
}
const overrideGeometryFunction = (feature) => {
  if (selectedParishId.value && selectedParishId.value != feature.getId()) { return null }
  if (selectedCountyId.value && selectedCountyId.value != feature.get('county_id')) { return null }
  // if (selectedTownId.value && selectedTownId.value != feature.get('town_id')) { return null }
  // if (selectedArchdeaconryId.value && selectedArchdeaconryId.value != feature.get('archdeaconry_id')) { return null }
  // if (selectedDioceseId.value && selectedDioceseId.value != feature.get('diocese_id')) { return null }
  // if (selectedProvinceId.value && selectedProvinceId.value != feature.get('province_id')) { return null }
  // if (selectedNationId.value && selectedNationId.value != feature.get('nation_id')) { return null }
  return feature.getGeometry()
}
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
  return [
    new Style({
      text: new Text({
        text: '\uf041',
        scale: 1,
        textBaseline: 'bottom',
        font: 'bold 1em "Font Awesome 7 Free"',
        fill: new Fill({ color: active ? 'red' : '#7cb341' }),
        stroke: new Stroke({ color: 'black', width: 3 }),
      }),
      zIndex: active ? Infinity : undefined,
    }),
    new Style({
      text: new Text({
        text: `${feature.get('label') ?? ''}`,
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
const dioceseRegionStyle = (feature) => {
  // const active = selectedDioceseId.value && selectedDioceseId.value == feature.get('id')
  // const active = selectedParishId.value && useParishesStore().parishesMap.get(selectedParishId.value).diocese_id == feature.get('id')
  const active = false
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
      text: `${feature.get('label') ?? ''}`,
      font: 'bold 0.5em system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
      fill: new Fill({ color: 'black' }),
      stroke: new Stroke({ color: 'white', width: 3 }),
    }),
    zIndex: active ? Infinity : undefined,
  })
}

const layerSwitcherChange = (layer) => {
  if (diocesePre1541TileLayerRef.value?.vectorTileLayer === layer) {
    locationStore.diocesePre1541Visible = layer.getVisible()
  } else if (diocesePost1541TileLayerRef.value?.vectorTileLayer === layer) {
    locationStore.diocesePost1541Visible = layer.getVisible()
  }
}
const layerSwitcherDisplayLayer = (layer) => {
  return diocesePre1541TileLayerRef.value?.vectorTileLayer === layer || diocesePost1541TileLayerRef.value?.vectorTileLayer === layer
}

const updateCenter = (event) => locationStore.center = event.target.getCenter()
const updateZoom = (event) => locationStore.zoom = event.target.getZoom()
const updateRotation = (event) => locationStore.rotation = event.target.getRotation()
const {
  pointerMove: pointerMoveCondition,
  click: clickCondition,
} = inject("ol-selectconditions")
useGeographic()

const updateFilters = async () => {
  nextTick(() => parishSourceVectorRef.value?.source.changed())
}
/*
watch(selectedNationId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedProvinceId.value = null
    selectedDioceseId.value = null
    selectedArchdeaconryId.value = null
    selectedParishId.value = null
    updateFilters()
  }
})
watch(selectedProvinceId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedDioceseId.value = null
    selectedArchdeaconryId.value = null
    selectedParishId.value = null
    updateFilters()
  }
})
watch(selectedDioceseId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedArchdeaconryId.value = null
    selectedParishId.value = null

    nextTick(() => {
      // hack to reset styles (using vectorTileLayer.getSource().changed() causes blinking)
      const resetStyle = (layer) => {
        const currentStyle = layer.getStyle()
        layer.setStyle(new Style())
        layer.setStyle(currentStyle)
      }
      resetStyle(diocesePre1541TileLayerRef.value?.vectorTileLayer)
      resetStyle(diocesePost1541TileLayerRef.value?.vectorTileLayer)
    })
    updateFilters()
  }
})
watch(selectedArchdeaconryId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedParishId.value = null
    updateFilters()
  }
})
*/
watch(selectedCountyId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedParishId.value = null
    updateFilters()
  }
})
watch(selectedParishId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    // nextTick(() => {
    //   // hack to reset styles (using vectorTileLayer.getSource().changed() causes blinking)
    //   const resetStyle = (layer) => {
    //     const currentStyle = layer.getStyle()
    //     layer.setStyle(new Style())
    //     layer.setStyle(currentStyle)
    //   }
    //   resetStyle(diocesePre1541TileLayerRef.value?.vectorTileLayer)
    //   resetStyle(diocesePost1541TileLayerRef.value?.vectorTileLayer)
    // })
    updateFilters()
  }
})
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
        <ol-source-osm url="https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png" />
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

      <ol-vector-tile-layer ref="diocesePre1541TileLayerRef"
          :renderMode="'vector'" :updateWhileAnimating="true" :updateWhileInteracting="true" :visible="diocesePre1541Visible"
          :properties="{ 'name': 'Dioceses before 1541' }">
        <ol-source-vector-tile :url="websiteOrigin+'/api/geo/dioceses/pre1541/tiles/{z}/{x}/{y}'" :format="mvt">
          <ol-style :overrideStyleFunction="dioceseRegionStyle"></ol-style>
        </ol-source-vector-tile>
      </ol-vector-tile-layer>
      <ol-vector-tile-layer ref="diocesePost1541TileLayerRef"
          :renderMode="'vector'" :updateWhileAnimating="true" :updateWhileInteracting="true" :visible="diocesePost1541Visible"
          :properties="{ 'name': 'Dioceses 1541 and after' }">
        <ol-source-vector-tile :url="websiteOrigin+'/api/geo/dioceses/post1541/tiles/{z}/{x}/{y}'" :format="mvt">
          <ol-style :overrideStyleFunction="dioceseRegionStyle"></ol-style>
        </ol-source-vector-tile>
      </ol-vector-tile-layer>

      <ol-vector-layer>
        <ol-source-cluster ref="parishSourceClusterRef" :distance="20" :geometryFunction="overrideGeometryFunction">
          <ol-source-vector ref="parishSourceVectorRef"
            :url="'api/geo/parishes'" :format="geoJson"
          ></ol-source-vector>
          <ol-style :overrideStyleFunction="overrideClusterStyle"></ol-style>
        </ol-source-cluster>
      </ol-vector-layer>

      <ol-interaction-drag-rotate-and-zoom  />
      <ol-zoom-control />
      <ol-rotate-control :autoHide="true" />
      <ol-full-screen-control />
      <ol-scale-line-control />
      <ol-layerswitcher-control
        :collapsed="false" :reordering="false" :trash="false" :noScroll="true"
        :displayInLayerSwitcher="layerSwitcherDisplayLayer" :onchangeCheck="layerSwitcherChange"
      />
      <ol-attribution-control :collapsible="true" :collapsed="true" />
    </ol-map>
    <!-- <FilterSingleSelect
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
    ></FilterSingleSelect> -->
    <FilterSingleSelect
      v-model:selected="selectedCountyId"
      v-model:listed="listedCounties"
      placeholder="Select a County"
      class="position-absolute filter select-county"
    ></FilterSingleSelect>
    <FilterSingleSelect
      v-model:selected="selectedParishId"
      v-model:listed="listedParishes"
      placeholder="Select a Parish"
      class="position-absolute filter select-parish"
      v-if="selectedCountyId"
    ></FilterSingleSelect>
  </div>
</template>

<style scoped>
.filter {
  left: .5em;
  position: absolute !important;
  width: fit-content !important;
}
/* .select-nation {
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
} */
.select-county {
  top: 4.0em;
}
.select-parish {
  top: 7em;
}
</style>