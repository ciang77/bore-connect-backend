import { createRouter, createWebHistory } from 'vue-router'
import OverviewView from '../views/OverviewView.vue'
import SpindleView from '../views/SpindleView.vue'
import DiagnosisView from '../views/DiagnosisView.vue'
import EquipmentView from '../views/EquipmentView.vue'
import AnalysisView from '../views/AnalysisView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'overview', component: OverviewView },
    { path: '/diagnosis', name: 'diagnosis', component: DiagnosisView },
    { path: '/equipment', name: 'equipment', component: EquipmentView },
    { path: '/analysis', name: 'analysis', component: AnalysisView },
  ],
})

export default router
