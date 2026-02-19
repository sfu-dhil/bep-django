import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { Popover } from 'bootstrap/dist/js/bootstrap.esm'

import './assets/bep.css'

const ready = (fn) => document.readyState !== 'loading' ? fn() : document.addEventListener('DOMContentLoaded', fn)
ready(() => {
  const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
  const popoverList = [...popoverTriggerList].map((popoverTriggerEl) => new Popover(popoverTriggerEl, { html: true, trigger: 'focus' }))
})