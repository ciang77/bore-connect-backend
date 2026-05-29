import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import SmartAnalysisView from '../views/SmartAnalysisView.vue'
import SystemStatusView from '../views/SystemStatusView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: DashboardView },
    { path: '/smart-analysis', name: 'smart-analysis', component: SmartAnalysisView },
    { path: '/system-status', name: 'system-status', component: SystemStatusView },
  ],
})

export default router
