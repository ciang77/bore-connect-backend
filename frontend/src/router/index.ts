import { createRouter, createWebHistory } from 'vue-router'
import OverviewView from '../views/OverviewView.vue'
import SpindleView from '../views/SpindleView.vue'
import DiagnosisView from '../views/DiagnosisView.vue'
import AnalysisView from '../views/AnalysisView.vue'
import TestView from '../views/TestView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'overview', component: OverviewView },
    { path: '/diagnosis', name: 'diagnosis', component: DiagnosisView },
    { path: '/analysis', name: 'analysis', component: AnalysisView },
    { path: '/test', name: 'test', component: TestView },
  ],
})

export default router
