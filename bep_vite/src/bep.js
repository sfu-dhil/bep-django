// vuejs
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Multiselect from 'vue-multiselect'
import OpenLayersMap from 'vue3-openlayers'
import LocationMapApp from './LocationMapApp.vue'
import InfoModalApp from './InfoModalApp.vue'
import InfoModalToggleApp from './InfoModalToggleApp.vue'
import ParishMapApp from './ParishMapApp.vue'
import DioceseMapApp from './DioceseMapApp.vue'

// other
import { Popover } from 'bootstrap/dist/js/bootstrap.esm'
import './fixes/jquery_load_fix.js'
import select2 from 'select2'
select2()

import './assets/bep.css'

const ready = (fn) => document.readyState !== 'loading' ? fn() : document.addEventListener('DOMContentLoaded', fn)
ready(() => {
  // setup popovers
  document.querySelectorAll('[data-bs-toggle="popover"]').forEach((popoverTriggerEl) => {
    new Popover(popoverTriggerEl, { html: true, trigger: 'focus' })
  })
  // setup select2
  document.querySelectorAll('.django-select2').forEach((djangoSelect2El) => {
    $(djangoSelect2El).select2({
      width: '100%',
    })
  })
  // remember detail open state for specific details (requires detail to have an id)
  document.querySelectorAll('details').forEach((detailEl) => {
    if (detailEl.getAttribute('id')) {
      const openStateKey = `details-${detailEl.getAttribute('id')}`
      detailEl.addEventListener('toggle', () => localStorage.setItem(openStateKey, detailEl.open ? 'open' : 'closed'))
      if (localStorage.getItem(openStateKey) == 'open') {
        detailEl.setAttribute('open', '')
      } else if (localStorage.getItem(openStateKey) == 'closed') {
        detailEl.removeAttribute('open')
      }
      // else use whatever default open state in on the element
    }
  });

  const pinia = createPinia()
  pinia.use(piniaPluginPersistedstate)

  document.querySelectorAll('#location-map-app').forEach((mountEl) => {
    const app = createApp(LocationMapApp)
    app.use(pinia)
    app.use(OpenLayersMap)
    app.component('Multiselect', Multiselect)
    app.mount(mountEl)
  })

  document.querySelectorAll('#info-modal-app').forEach((mountEl) => {
    const app = createApp(InfoModalApp)
    app.use(pinia)
    app.mount(mountEl)
  })

  document.querySelectorAll('.info-modal-toggle-app').forEach((mountEl) => {
    const app = createApp(InfoModalToggleApp, { ...mountEl.dataset })
    app.use(pinia)
    app.use(OpenLayersMap)
    app.mount(mountEl)
  })

  document.querySelectorAll('.parish-map-app').forEach((mountEl) => {
    const app = createApp(ParishMapApp, { ...mountEl.dataset })
    app.use(pinia)
    app.use(OpenLayersMap)
    app.mount(mountEl)
  })

  document.querySelectorAll('.diocese-map-app').forEach((mountEl) => {
    const app = createApp(DioceseMapApp, { ...mountEl.dataset })
    app.use(pinia)
    app.use(OpenLayersMap)
    app.mount(mountEl)
  })
})