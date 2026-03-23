<script setup>
import { ref, computed, provide } from 'vue'
import {
  useParishesStore,
  useParishTransactionsStore,
  useParishInventoriesStore,
  useMonarchsStore,
  useInjunctionStore
} from '../stores/data.js'
import { useInfoModalStore } from '../stores/info_modal.js'
import { getLsdString, getColorPalletByIndex } from '../helpers/utils.js'
import 'echarts'
import VChart, { THEME_KEY } from 'vue-echarts'
provide(THEME_KEY, 'dark')

const props = defineProps({
  parishIds: {
    type: Array,
    required: true,
  },
})


// setup onload data
const monarchs = await useMonarchsStore().getAll()
const injunctionsByYearMap = [...await useInjunctionStore().getAll()].reduce((result, injunction) => {
  const axis = !injunction.date || isNaN(parseInt(injunction.date)) ? null : parseInt(injunction.date)
  if (!result.has(axis)) { result.set(axis, []) }
  result.get(axis).push(injunction)
  return result
}, new Map())
const parishMap = new Map()
const inventoriesByYearMap = new Map()
const transactionsByYearMap = new Map()
const transactionCategoriesMap = new Map()
for (let index = 0; index < props.parishIds.length; ++index) {
  // load parish
  parishMap.set(props.parishIds[index], await useParishesStore().getById(props.parishIds[index]))
  // load parish transactions
  const transactions = await useParishTransactionsStore().getByParishId(props.parishIds[index])
  transactions.forEach((transaction) => {
    if (!transactionsByYearMap.has(transaction.start_year)) { transactionsByYearMap.set(transaction.start_year, []) }
    transactionsByYearMap.get(transaction.start_year).push(transaction)
    transaction.transaction_categories.forEach(({id, label}) => {
      if (!transactionCategoriesMap.has(id)) { transactionCategoriesMap.set(id, {label, count: 0}) }
      ++transactionCategoriesMap.get(id).count
    })
  })
  const inventories = await useParishInventoriesStore().getByParishId(props.parishIds[index])
  inventories.forEach((inventory) => {
    if (!inventoriesByYearMap.has(inventory.start_year)) { inventoriesByYearMap.set(inventory.start_year, []) }
    inventoriesByYearMap.get(inventory.start_year).push(inventory)
  })
}

// gets all unique years from both sets
const yearKeys = [...new Set([...transactionsByYearMap.keys(), ...injunctionsByYearMap.keys()])].filter((year) => year !== null).map((year) => parseInt(year))
const yearMin = Math.min(...yearKeys)
const yearMax = Math.max(...yearKeys)
const zoomStart = transactionsByYearMap.get(null) ? 'Unknown' : Math.min(...transactionsByYearMap.keys()) || yearMin
const zoomEnd = Math.max(...transactionsByYearMap.keys()) || yearMax

const GRID_LIST = []
let gridListIndexSetter = 0
const TOP_CHART_GRID_INDEX = gridListIndexSetter++
GRID_LIST[TOP_CHART_GRID_INDEX] = { top: '15%', height: '35%', left: '10%', width: '65%', }
const BOTTOM_CHART_GRID_INDEX = gridListIndexSetter++
GRID_LIST[BOTTOM_CHART_GRID_INDEX] = { bottom: '10%', height: '35%', left: '10%', width: '65%', }

const DATA_ALL_YEARS = Array.from({ length: yearMax - yearMin + 1 }, (_, i) => `${yearMin + i}`)
if (transactionsByYearMap.get(null) || injunctionsByYearMap.get(null)) {
  DATA_ALL_YEARS.unshift('Unknown')
}

const DATASET_LIST = []
let datasetListIndexSetter = 0
const DATASET_ALL_YEARS_INDEX = datasetListIndexSetter++
DATASET_LIST[DATASET_ALL_YEARS_INDEX] = {
  dimensions: ['year'],
  source: DATA_ALL_YEARS.map((year) => ({year}))
}
const DATASET_TRANSACTION_TOTALS_INDEX = datasetListIndexSetter++
DATASET_LIST[DATASET_TRANSACTION_TOTALS_INDEX] = {
  dimensions: ['year', 'total'],
  source: [...transactionsByYearMap]
    .sort(([yearA, _A], [yearB, _B]) => yearA - yearB)
    .map(([year, objects]) => ({year: year ? `${year}` : 'Unknown', total: objects.length}))
}
const DATASET_INVENTORIES_TOTALS_INDEX = datasetListIndexSetter++
DATASET_LIST[DATASET_INVENTORIES_TOTALS_INDEX] = {
  dimensions: ['year', 'total'],
  source: [...inventoriesByYearMap]
    .sort(([yearA, _A], [yearB, _B]) => yearA - yearB)
    .map(([year, objects]) => ({year: year ? `${year}` : 'Unknown', total: objects.length}))
}
const DATASET_INJUNCTION_TOTALS_INDEX = datasetListIndexSetter++
DATASET_LIST[DATASET_INJUNCTION_TOTALS_INDEX] = {
  dimensions: ['year', 'total'],
  source: [...injunctionsByYearMap]
    .sort(([yearA, _A], [yearB, _B]) => yearA - yearB)
    .map(([year, objects]) => ({year: year ? `${year}` : 'Unknown', total: objects.length}))
}
const DATASET_TRANSACTION_VALUES_TOTALS_INDEX = datasetListIndexSetter++
DATASET_LIST[DATASET_TRANSACTION_VALUES_TOTALS_INDEX] = {
  dimensions: ['year', 'total'],
  source: [...transactionsByYearMap]
    .sort(([yearA, _A], [yearB, _B]) => yearA - yearB)
    .map(([year, objects]) => ({year: year ? `${year}` : 'Unknown', total: objects.reduce((sum, transaction) => sum + transaction.value, 0)}))
    .filter(({year, total}) => total > 0)
}
const DATASET_TRANSACTION_SHIPPING_TOTALS_INDEX = datasetListIndexSetter++
DATASET_LIST[DATASET_TRANSACTION_SHIPPING_TOTALS_INDEX] = {
  dimensions: ['year', 'total'],
  source: [...transactionsByYearMap]
    .sort(([yearA, _A], [yearB, _B]) => yearA - yearB)
    .map(([year, objects]) => ({year: `${year}`, total: objects.reduce((sum, transaction) => sum + transaction.shipping, 0)}))
    .filter(({year, total}) => total > 0)
}
const DATASET_TRANSACTION_CATEGORIES_INDEX = datasetListIndexSetter++
DATASET_LIST[DATASET_TRANSACTION_CATEGORIES_INDEX] = {
  dimensions: ['label', 'count'],
  source: [...transactionCategoriesMap.values()],
}

const X_AXIS_LIST = []
let xAxisListIndexSetter = 0
const TOP_CHART_X_AXIS_INDEX = xAxisListIndexSetter++
X_AXIS_LIST[TOP_CHART_X_AXIS_INDEX] = {
  gridIndex: TOP_CHART_GRID_INDEX,
  // name: 'Year',
  type: 'category',
  data: DATA_ALL_YEARS,
  axisPointer: { label: { formatter: (params) => params.value === 'Unknown' ? 'Unknown Year' : `Year ${params.value}` } },
  triggerEvent: true,
}
const BOTTOM_CHART_X_AXIS_INDEX = xAxisListIndexSetter++
X_AXIS_LIST[BOTTOM_CHART_X_AXIS_INDEX] = {
  gridIndex: BOTTOM_CHART_GRID_INDEX,
  type: 'category',
  data: DATA_ALL_YEARS,
  position: 'top',
  axisPointer: { label: { formatter: (params) => params.value === 'Unknown' ? 'Unknown Year' : `Year ${params.value}` } },
  axisLabel: { show: false },
  axisLine: { show: false },
  axisTick: { show: false },
  triggerEvent: true,
}

const Y_AXIS_LIST = []
let yAxisListIndexSetter = 0
const TOP_CHART_Y_AXIS_INDEX = yAxisListIndexSetter++
Y_AXIS_LIST[TOP_CHART_Y_AXIS_INDEX] = {
  gridIndex: TOP_CHART_GRID_INDEX,
  type: 'value',
  minInterval: 1,
}
const BOTTOM_CHART_Y_AXIS_INDEX = yAxisListIndexSetter++
Y_AXIS_LIST[BOTTOM_CHART_Y_AXIS_INDEX] = {
  gridIndex: BOTTOM_CHART_GRID_INDEX,
  type: 'value',
  minInterval: 1,
  axisLabel: { formatter: getLsdString },
}

const showYearEventsModal = (year) => {
  useInfoModalStore().showModal('year_events', year, {
    transactions: transactionsByYearMap.get(year) || [],
    inventories: inventoriesByYearMap.get(year) || [],
    injunctions: injunctionsByYearMap.get(year) || [],
  })
}

const handleChartClick = (params) => {
  if (params.componentType === 'xAxis') {
    const year = params.value === 'Unknown' ? null : parseInt(params.value)
    showYearEventsModal(year)
  } else if (params.componentType === 'series' && params.value?.year) {
    const year = params.value.year === 'Unknown' ? null : parseInt(params.value.year)
    showYearEventsModal(year)
  }
}
const markAreaDataMonarchs = monarchs
  .filter((monarch) => monarch.start_year && monarch.start_year <= yearMax && monarch.end_year && monarch.end_year >= yearMin)
  .sort((a, b) => a.start_year - b.start_year)
  .map((monarch, index) => {
    const startYear = monarch.start_year < yearMin ? yearMin : monarch.start_year
    const endYear = monarch.end_year > yearMax ? yearMax : monarch.end_year
    return [
      {
        name: monarch.label.split('(')[0].trim(),
        xAxis: `${startYear}`,
        itemStyle: { color: getColorPalletByIndex(index), borderColor: getColorPalletByIndex(index) },
      },
      { xAxis: `${endYear}`, }
    ]
  })
const markAreaDataMonarchsWithoutLabels = markAreaDataMonarchs.map((markAreaValue) => {
  const { name: _, ...data0 } = markAreaValue[0]
  const {...data1} = markAreaValue[1]
  return [data0, data1]
})

const chartOptions = computed(() => ({
  title: [
    { text: 'Events by Year', left: 'center' },
    { text: 'Transaction Categories', top: '10%', left: '87.5%', textAlign: 'center' },
  ],
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow', snap: true },
  },
  // TODO: FIX the tooltip formatting (year only once, order from top to bottom)
  axisPointer: { link: [{ xAxisIndex: [TOP_CHART_X_AXIS_INDEX, BOTTOM_CHART_X_AXIS_INDEX] }] },
  toolbox: {
    feature: {
      dataZoom: { yAxisIndex: 'none' },
      dataView: { readOnly: false },
      restore: {},
      saveAsImage: {},
    }
  },
  grid: GRID_LIST,
  xAxis: X_AXIS_LIST,
  yAxis: Y_AXIS_LIST,
  dataZoom: [
    { type: 'slider', startValue: zoomStart, endValue: zoomEnd, xAxisIndex: [TOP_CHART_X_AXIS_INDEX, BOTTOM_CHART_X_AXIS_INDEX] },
    { type: 'inside', startValue: zoomStart, endValue: zoomEnd, xAxisIndex: [TOP_CHART_X_AXIS_INDEX, BOTTOM_CHART_X_AXIS_INDEX] },
  ],
  dataset: DATASET_LIST,
  legend: {
    orient: 'horizontal',
    top: 45,
    data: ['Transactions', 'Injunctions', 'Inventories', 'Total Transaction Value', 'Total Transaction Shipping' ],
  },
  series: [
    {
      name: 'Top Chart Monarch Mark Areas',
      xAxisIndex: TOP_CHART_X_AXIS_INDEX,
      yAxisIndex: TOP_CHART_Y_AXIS_INDEX,
      datasetIndex: DATASET_ALL_YEARS_INDEX,
      type: 'custom',
      renderItem: () => {},
      tooltip: { show: false },
      markArea: {
        silent: true,
        itemStyle: { opacity: 0.2 },
        data: markAreaDataMonarchs
      },
    },
    {
      name: 'Transactions',
      xAxisIndex: TOP_CHART_X_AXIS_INDEX,
      yAxisIndex: TOP_CHART_Y_AXIS_INDEX,
      datasetIndex: DATASET_TRANSACTION_TOTALS_INDEX,
      type: 'bar',
      stack: 'events_total',
      encode: { x: 'year', y: 'total'},
    },
    {
      name: 'Injunctions',
      xAxisIndex: TOP_CHART_X_AXIS_INDEX,
      yAxisIndex: TOP_CHART_Y_AXIS_INDEX,
      datasetIndex: DATASET_INJUNCTION_TOTALS_INDEX,
      type: 'bar',
      stack: 'events_total',
      encode: { x: 'year', y: 'total'},
    },
    {
      name: 'Inventories',
      xAxisIndex: TOP_CHART_X_AXIS_INDEX,
      yAxisIndex: TOP_CHART_Y_AXIS_INDEX,
      datasetIndex: DATASET_INVENTORIES_TOTALS_INDEX,
      type: 'bar',
      stack: 'events_total',
      encode: { x: 'year', y: 'total'},
    },
    {
      name: 'Bottom Chart Monarch Mark Areas',
      xAxisIndex: BOTTOM_CHART_X_AXIS_INDEX,
      yAxisIndex: BOTTOM_CHART_Y_AXIS_INDEX,
      type: 'custom',
      renderItem: () => {},
      tooltip: { show: false },
      markArea: {
        silent: true,
        itemStyle: { opacity: 0.2 },
        data: markAreaDataMonarchsWithoutLabels
      },
    },
    {
      name: 'Total Transaction Value',
      xAxisIndex: BOTTOM_CHART_X_AXIS_INDEX,
      yAxisIndex: BOTTOM_CHART_Y_AXIS_INDEX,
      datasetIndex: DATASET_TRANSACTION_VALUES_TOTALS_INDEX,
      type: 'bar',
      stack: 'lsd_total',
      encode: { x: 'year', y: 'total'},
      tooltip: { valueFormatter: getLsdString },
      connectNulls: true,
    },
    // {
    //   name: 'Average Value',
    //   xAxisIndex: 1,
    //   yAxisIndex: 1,
    //   type: 'line',
    //   encode: { x: 'year', y: 'valueAverage'},
    //   tooltip: { valueFormatter: getLsdString },
    //   connectNulls: true,
    // },
    {
      name: 'Total Transaction Shipping',
      xAxisIndex: BOTTOM_CHART_X_AXIS_INDEX,
      yAxisIndex: BOTTOM_CHART_Y_AXIS_INDEX,
      datasetIndex: DATASET_TRANSACTION_SHIPPING_TOTALS_INDEX,
      type: 'bar',
      stack: 'lsd_total',
      encode: { x: 'year', y: 'shippingTotal'},
      tooltip: { valueFormatter: getLsdString },
      connectNulls: true,
    },
    // {
    //   name: 'Average Shipping',
    //   xAxisIndex: 1,
    //   yAxisIndex: 1,
    //   type: 'line',
    //   encode: { x: 'year', y: 'shippingAverage'},
    //   tooltip: { valueFormatter: getLsdString },
    //   connectNulls: true,
    // },
    {
      name: 'Transaction Categories',
      datasetIndex: DATASET_TRANSACTION_CATEGORIES_INDEX,
      type: 'pie',
      radius: '100%',
      center: ['50%', '50%'],
      top: '15%',
      height: '35%',
      left: '80%',
      right: '5%',
      encode: { itemName: 'label', value: 'count' },
      avoidLabelOverlap: false,
      label: { show: false, position: 'center' },
      labelLine: { show: false },
      emphasis: { show: false },
      tooltip: { trigger: 'item' },
    },
  ],
}))
</script>

<template>
  <VChart class="chart" :option="chartOptions" autoresize @click="handleChartClick" />
</template>

<style scoped>
.chart {
  min-height: 40em;
  height: 100%;
}
</style>
