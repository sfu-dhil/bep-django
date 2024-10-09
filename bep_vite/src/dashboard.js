

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Multiselect from 'vue-multiselect'
import OpenLayersMap from 'vue3-openlayers'
import DashboardApp from './DashboardApp.vue'

import 'vue-multiselect/dist/vue-multiselect.min.css'
import 'vue3-openlayers/styles.css'
import './assets/dashboard.css'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(DashboardApp)
app.use(pinia)
app.use(OpenLayersMap)
app.component('Multiselect', Multiselect)
app.mount('#dashboard-app')
