import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import SpindleView from '../views/SpindleView.vue'
import DiagnosisView from '../views/DiagnosisView.vue'
import EquipmentView from '../views/EquipmentView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: DashboardView },
    { path: '/spindle', name: 'spindle', component: SpindleView },
    { path: '/diagnosis', name: 'diagnosis', component: DiagnosisView },
    { path: '/equipment', name: 'equipment', component: EquipmentView },
  ],
})

export default router
