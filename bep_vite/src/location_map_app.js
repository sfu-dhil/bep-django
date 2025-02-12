import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Multiselect from 'vue-multiselect'
import OpenLayersMap from 'vue3-openlayers'
import LocationMapApp from './LocationMapApp.vue'

import 'vue-multiselect/dist/vue-multiselect.min.css'
import 'vue3-openlayers/styles.css'
import './assets/base.css'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(LocationMapApp)
app.use(pinia)
app.use(OpenLayersMap)
app.component('Multiselect', Multiselect)
app.mount('#location-map-app')
