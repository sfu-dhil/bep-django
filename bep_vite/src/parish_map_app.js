import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import OpenLayersMap from 'vue3-openlayers'
import ParishMapApp from './ParishMapApp.vue'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const mountElList = document.querySelectorAll('.parish-map-app')
mountElList.forEach((mountEl) => {
  const app = createApp(ParishMapApp, { ...mountEl.dataset })
  app.use(pinia)
  app.use(OpenLayersMap)
  app.mount(mountEl)
})