<script setup>
import Sidebar from './components/Sidebar.vue'
import DashboardMap from './components/DashboardMap.vue'
import ParishModal from './components/ParishModal.vue'
</script>

<template>
  <div class="row g-0 vh-100">
    <div class="col-md-3">
      <Sidebar></Sidebar>
    </div>
    <div class="col-md-9">
      <DashboardMap></DashboardMap>
    </div>
    <ParishModal></ParishModal>
  </div>
</template>

<style scoped>
</style>
