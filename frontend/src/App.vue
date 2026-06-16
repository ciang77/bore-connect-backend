<script setup lang="ts">
import ChatBot from './components/ChatBot.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const now = ref(new Date())
let timer: ReturnType<typeof setInterval> | undefined

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

const navItems = [
  { name: 'overview', cn: '总览', en: 'Overview', path: '/' },
  { name: 'analysis', cn: '智能分析', en: 'Analysis', path: '/analysis' },
  { name: 'diagnosis', cn: '状态检测', en: 'Diagnosis', path: '/diagnosis' },
  { name: 'test', cn: '测试', en: 'Test', path: '/test' },
]

function pad(n: number): string {
  return n < 10 ? '0' + n : '' + n
}

function formatDate(d: Date): string {
  return `${d.getFullYear()}年${pad(d.getMonth() + 1)}月${pad(d.getDate())}日`
}

function formatTime(d: Date): string {
  return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

function weekday(d: Date): string {
  return '星期' + weekdays[d.getDay()]
}

onMounted(() => {
  timer = setInterval(() => { now.value = new Date() }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="page">
    <div class="bg-grid"></div>
    <div class="bg-glow bg-glow-1"></div>
    <div class="bg-glow bg-glow-2"></div>
    <div class="bg-glow bg-glow-3"></div>
    <div class="bg-gradient-subtle"></div>

    <header class="top-bar">
      <div class="corner corner-tl"></div>
      <div class="corner corner-tr"></div>
      <div class="corner corner-bl"></div>
      <div class="corner corner-br"></div>
      <div class="top-bar-glow"></div>
      <div class="top-bar-noise"></div>
      <div class="top-bar-inner">
        <div class="top-bar-left">
          <div class="status-panel">
            <div class="status-frame">
              <div class="status-row">
                <span class="status-dot"></span>
                <span class="status-name">CNC CONTROL CORE</span>
              </div>
            </div>
          </div>
        </div>

        <div class="top-bar-center">
          <div class="title-ornament title-ornament-left" aria-hidden="true">
            <span class="ornament-line"></span>
            <span class="ornament-diamond"></span>
            <span class="ornament-line short"></span>
          </div>
          <div class="title-core">
            <div class="title-glow"></div>
            <h1 class="main-title">龙门镗铣床智能管理平台</h1>
            <div class="title-bracket title-bracket-left"></div>
            <div class="title-bracket title-bracket-right"></div>
          </div>
          <div class="title-ornament title-ornament-right" aria-hidden="true">
            <span class="ornament-line"></span>
            <span class="ornament-diamond"></span>
            <span class="ornament-line short"></span>
          </div>
        </div>

        <div class="top-bar-right">
          <div class="datetime-card">
            <div class="datetime-block">
              <div class="datetime-segment">
                <span class="date-text">{{ formatDate(now) }}</span>
              </div>
              <span class="divider"></span>
              <div class="datetime-segment">
                <span class="weekday-text">{{ weekday(now) }}</span>
              </div>
              <span class="divider"></span>
              <div class="datetime-segment time-segment">
                <span class="time-text">{{ formatTime(now) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="scan-line"></div>
    </header>

    <main class="content">
      <router-view />
    </main>

    <nav class="bottom-nav">
      <div class="corner corner-bl"></div>
      <div class="corner corner-br"></div>
      <div class="bottom-nav-glow"></div>
      <div class="bottom-nav-noise"></div>
      <div class="scan-line"></div>
      <div class="nav-ornament nav-ornament-left">
        <svg viewBox="0 0 400 44" preserveAspectRatio="none" class="ornament-svg">
          <defs>
            <linearGradient id="flowGradL1" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="transparent"/>
              <stop offset="100%" stop-color="#667eea"/>
            </linearGradient>
            <linearGradient id="flowGradL2" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="transparent"/>
              <stop offset="100%" stop-color="#a855f7"/>
            </linearGradient>
            <linearGradient id="fadeGradL" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="rgba(20,26,48,0.95)"/>
              <stop offset="100%" stop-color="transparent"/>
            </linearGradient>
          </defs>
          <rect x="0" y="0" width="400" height="44" fill="url(#fadeGradL)"/>
          <path d="M0 22 Q100 4 200 22 T380 22" stroke="url(#flowGradL1)" stroke-width="1.5" fill="none" opacity="0.8">
            <animate attributeName="d" dur="3s" repeatCount="indefinite" values="M0 22 Q100 4 200 22 T380 22;M0 22 Q100 40 200 22 T380 22;M0 22 Q100 4 200 22 T380 22"/>
          </path>
          <path d="M0 32 Q120 14 220 32 T400 32" stroke="url(#flowGradL2)" stroke-width="1" fill="none" opacity="0.6">
            <animate attributeName="d" dur="4s" repeatCount="indefinite" values="M0 32 Q120 14 220 32 T400 32;M0 32 Q120 50 220 32 T400 32;M0 32 Q120 14 220 32 T400 32"/>
          </path>
          <path d="M0 12 Q80 30 180 12 T360 12" stroke="url(#flowGradL1)" stroke-width="1" fill="none" opacity="0.5">
            <animate attributeName="d" dur="3.5s" repeatCount="indefinite" values="M0 12 Q80 30 180 12 T360 12;M0 12 Q80 6 180 12 T360 12;M0 12 Q80 30 180 12 T360 12"/>
          </path>
          <circle cx="60" cy="22" r="2.5" fill="#667eea" opacity="0.6">
            <animate attributeName="cy" dur="2s" repeatCount="indefinite" values="22;18;22"/>
          </circle>
          <circle cx="160" cy="22" r="2" fill="#a855f7" opacity="0.7">
            <animate attributeName="cy" dur="2.5s" repeatCount="indefinite" values="22;26;22"/>
          </circle>
          <circle cx="260" cy="22" r="3" fill="#667eea" opacity="0.5">
            <animate attributeName="cy" dur="3s" repeatCount="indefinite" values="22;19;22"/>
          </circle>
          <circle cx="350" cy="22" r="2" fill="#a855f7" opacity="0.6">
            <animate attributeName="cy" dur="2.2s" repeatCount="indefinite" values="22;25;22"/>
          </circle>
          <polygon points="120,22 125,17 130,22 125,27" fill="#667eea" opacity="0.5">
            <animateTransform attributeName="transform" type="rotate" dur="4s" repeatCount="indefinite" from="45 125 22" to="405 125 22"/>
          </polygon>
          <polygon points="220,22 225,17 230,22 225,27" fill="#a855f7" opacity="0.6">
            <animateTransform attributeName="transform" type="rotate" dur="5s" repeatCount="indefinite" from="45 225 22" to="405 225 22"/>
          </polygon>
          <polygon points="320,22 325,17 330,22 325,27" fill="#667eea" opacity="0.45">
            <animateTransform attributeName="transform" type="rotate" dur="3.5s" repeatCount="indefinite" from="45 325 22" to="405 325 22"/>
          </polygon>
        </svg>
      </div>
      <div class="nav-items-wrapper">
        <button
          v-for="item in navItems"
          :key="item.name"
          class="nav-item"
          :class="{ active: route.name === item.name }"
          @click="router.push(item.path)"
        >
          <span class="nav-icon">
            <svg v-if="item.name === 'overview'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
            </svg>
            <svg v-else-if="item.name === 'analysis'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"/>
            </svg>
            <svg v-else-if="item.name === 'diagnosis'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14l-5-5 1.41-1.41L12 14.17l4.59-4.58L18 11l-6 6z"/>
            </svg>
            <svg v-else-if="item.name === 'test'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
            </svg>
          </span>
          <span class="nav-label-cn">{{ item.cn }}</span>
        </button>
      </div>
      <div class="nav-ornament nav-ornament-right">
        <svg viewBox="0 0 400 44" preserveAspectRatio="none" class="ornament-svg">
          <defs>
            <linearGradient id="flowGradR1" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#667eea"/>
              <stop offset="100%" stop-color="transparent"/>
            </linearGradient>
            <linearGradient id="flowGradR2" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#a855f7"/>
              <stop offset="100%" stop-color="transparent"/>
            </linearGradient>
            <linearGradient id="fadeGradR" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="transparent"/>
              <stop offset="100%" stop-color="rgba(20,26,48,0.95)"/>
            </linearGradient>
          </defs>
          <rect x="0" y="0" width="400" height="44" fill="url(#fadeGradR)"/>
          <path d="M400 22 Q300 4 200 22 T20 22" stroke="url(#flowGradR1)" stroke-width="1.5" fill="none" opacity="0.8">
            <animate attributeName="d" dur="3s" repeatCount="indefinite" values="M400 22 Q300 4 200 22 T20 22;M400 22 Q300 40 200 22 T20 22;M400 22 Q300 4 200 22 T20 22"/>
          </path>
          <path d="M400 32 Q280 14 180 32 T0 32" stroke="url(#flowGradR2)" stroke-width="1" fill="none" opacity="0.6">
            <animate attributeName="d" dur="4s" repeatCount="indefinite" values="M400 32 Q280 14 180 32 T0 32;M400 32 Q280 50 180 32 T0 32;M400 32 Q280 14 180 32 T0 32"/>
          </path>
          <path d="M400 12 Q320 30 220 12 T40 12" stroke="url(#flowGradR1)" stroke-width="1" fill="none" opacity="0.5">
            <animate attributeName="d" dur="3.5s" repeatCount="indefinite" values="M400 12 Q320 30 220 12 T40 12;M400 12 Q320 6 220 12 T40 12;M400 12 Q320 30 220 12 T40 12"/>
          </path>
          <circle cx="340" cy="22" r="2.5" fill="#667eea" opacity="0.6">
            <animate attributeName="cy" dur="2s" repeatCount="indefinite" values="22;18;22"/>
          </circle>
          <circle cx="240" cy="22" r="2" fill="#a855f7" opacity="0.7">
            <animate attributeName="cy" dur="2.5s" repeatCount="indefinite" values="22;26;22"/>
          </circle>
          <circle cx="140" cy="22" r="3" fill="#667eea" opacity="0.5">
            <animate attributeName="cy" dur="3s" repeatCount="indefinite" values="22;19;22"/>
          </circle>
          <circle cx="50" cy="22" r="2" fill="#a855f7" opacity="0.6">
            <animate attributeName="cy" dur="2.2s" repeatCount="indefinite" values="22;25;22"/>
          </circle>
          <polygon points="280,22 285,17 290,22 285,27" fill="#667eea" opacity="0.5">
            <animateTransform attributeName="transform" type="rotate" dur="4s" repeatCount="indefinite" from="45 285 22" to="405 285 22"/>
          </polygon>
          <polygon points="180,22 185,17 190,22 185,27" fill="#a855f7" opacity="0.6">
            <animateTransform attributeName="transform" type="rotate" dur="5s" repeatCount="indefinite" from="45 185 22" to="405 185 22"/>
          </polygon>
          <polygon points="80,22 85,17 90,22 85,27" fill="#667eea" opacity="0.45">
            <animateTransform attributeName="transform" type="rotate" dur="3.5s" repeatCount="indefinite" from="45 85 22" to="405 85 22"/>
          </polygon>
        </svg>
      </div>
    </nav>

    <ChatBot />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  height: 100%;
  overflow: hidden;
}

body {
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  color: #e0e6f0;
}
</style>

<style scoped>
.page {
  height: 100vh;
  background: linear-gradient(160deg, #0f1629 0%, #1a1f3a 40%, #12182b 70%, #0d1220 100%);
  position: relative;
  display: flex;
  flex-direction: column;
}

.bg-gradient-subtle {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 20%, rgba(99, 126, 234, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(168, 85, 247, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse 50% 30% at 50% 50%, rgba(0, 180, 216, 0.04) 0%, transparent 60%);
  pointer-events: none;
}

.bg-glow {
  position: fixed;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
}

.bg-glow-1 {
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(99, 126, 234, 0.15) 0%, transparent 70%);
  top: -250px;
  right: -150px;
}

.bg-glow-2 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.12) 0%, transparent 70%);
  bottom: -200px;
  left: -100px;
}

.bg-glow-3 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(0, 229, 255, 0.08) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.top-bar {
  margin: 16px 16px 0;
  background:
    linear-gradient(180deg, rgba(20, 26, 48, 0.95) 0%, rgba(15, 20, 40, 0.92) 100%),
    linear-gradient(90deg, rgba(99, 126, 234, 0.06), transparent 20%, rgba(168, 85, 247, 0.04) 50%, transparent 80%, rgba(0, 229, 255, 0.06));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(99, 126, 234, 0.2);
  border-radius: 20px;
  padding: 14px 22px;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.03),
    inset 0 0 40px rgba(99, 126, 234, 0.05),
    0 16px 40px rgba(0, 0, 0, 0.35),
    0 0 40px rgba(99, 126, 234, 0.08);
  overflow: hidden;
  flex-shrink: 0;
}

.top-bar-glow {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 100% 80% at 50% 0%, rgba(99, 126, 234, 0.12) 0%, transparent 50%),
    linear-gradient(90deg, transparent, rgba(99, 126, 234, 0.03), transparent);
  pointer-events: none;
}

.top-bar-noise {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.035) 0, rgba(255, 255, 255, 0.035) 1px, transparent 1px, transparent 4px);
  opacity: 0.18;
  pointer-events: none;
}

.corner {
  position: absolute;
  width: 22px;
  height: 22px;
  pointer-events: none;
  opacity: 0.9;
}

.corner-tl {
  top: 10px;
  left: 10px;
  border-top: 2px solid rgba(99, 126, 234, 0.6);
  border-left: 2px solid rgba(99, 126, 234, 0.6);
}

.corner-tr {
  top: 10px;
  right: 10px;
  border-top: 2px solid rgba(99, 126, 234, 0.6);
  border-right: 2px solid rgba(99, 126, 234, 0.6);
}

.corner-bl {
  bottom: 10px;
  left: 10px;
  border-bottom: 2px solid rgba(168, 85, 247, 0.5);
  border-left: 2px solid rgba(168, 85, 247, 0.5);
}

.corner-br {
  bottom: 10px;
  right: 10px;
  border-bottom: 2px solid rgba(168, 85, 247, 0.5);
  border-right: 2px solid rgba(168, 85, 247, 0.5);
}

.top-bar-inner {
  max-width: 1600px;
  margin: 0 auto;
  min-height: 76px;
  display: grid;
  grid-template-columns: minmax(240px, 1fr) minmax(520px, 1.6fr) minmax(320px, 1fr);
  align-items: center;
  position: relative;
  gap: 18px;
}

.top-bar-left,
.top-bar-right {
  display: flex;
  align-items: center;
}

.top-bar-right {
  justify-content: flex-end;
}

.status-panel {
  width: 100%;
}

.status-frame {
  min-height: 68px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  padding: 12px 16px;
  border: 1px solid rgba(99, 126, 234, 0.2);
  border-radius: 14px;
  background:
    linear-gradient(135deg, rgba(20, 26, 48, 0.9), rgba(15, 22, 45, 0.6)),
    linear-gradient(90deg, rgba(99, 126, 234, 0.06), transparent 70%);
  box-shadow:
    inset 0 0 24px rgba(99, 126, 234, 0.06),
    inset 0 0 0 1px rgba(255, 255, 255, 0.02),
    0 0 24px rgba(99, 126, 234, 0.06);
}

.status-meta {
  font-size: 10px;
  letter-spacing: 2.6px;
  color: rgba(170, 223, 255, 0.54);
  text-transform: uppercase;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: radial-gradient(circle, #75ff9b 0%, #00e676 65%, #00b85b 100%);
  box-shadow:
    0 0 0 4px rgba(0, 230, 118, 0.12),
    0 0 14px rgba(0, 230, 118, 0.7);
  animation: pulse-dot 2.2s ease-in-out infinite;
}

.status-name {
  font-size: 18px;
  color: rgba(225, 246, 255, 0.96);
  letter-spacing: 1.8px;
  font-weight: 600;
}

.status-subrow {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(181, 223, 246, 0.6);
  font-size: 11px;
  letter-spacing: 1.5px;
}

.status-online {
  color: #a5b4fc;
  text-shadow: 0 0 10px rgba(99, 126, 234, 0.3);
}

.status-divider {
  width: 24px;
  height: 1px;
  background: linear-gradient(90deg, rgba(99, 126, 234, 0.1), rgba(99, 126, 234, 0.6), rgba(99, 126, 234, 0.1));
}

.status-desc {
  color: rgba(170, 213, 240, 0.56);
}

.top-bar-center {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
}

.title-core {
  min-width: 620px;
  padding: 12px 56px 14px;
  position: relative;
  text-align: center;
  border: 1px solid rgba(99, 126, 234, 0.25);
  background:
    linear-gradient(180deg, rgba(20, 26, 48, 0.88), rgba(15, 22, 45, 0.6)),
    linear-gradient(90deg, rgba(99, 126, 234, 0.08), transparent 18%, rgba(168, 85, 247, 0.05) 50%, transparent 82%, rgba(99, 126, 234, 0.08));
  clip-path: polygon(22px 0, calc(100% - 22px) 0, 100% 50%, calc(100% - 22px) 100%, 22px 100%, 0 50%);
  box-shadow:
    inset 0 0 36px rgba(99, 126, 234, 0.08),
    inset 0 0 0 1px rgba(255, 255, 255, 0.03),
    0 0 28px rgba(99, 126, 234, 0.1);
}

.title-glow {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 50% 50%, rgba(99, 126, 234, 0.1) 0%, transparent 60%),
    linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.03), transparent);
  pointer-events: none;
}

.title-core::before,
.title-core::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 70px;
  height: 2px;
  background: linear-gradient(90deg, rgba(99, 126, 234, 0), rgba(99, 126, 234, 0.8));
}

.title-core::before {
  left: -48px;
}

.title-core::after {
  right: -48px;
  transform: scaleX(-1);
}

.title-code {
  font-size: 10px;
  letter-spacing: 3px;
  color: rgba(159, 220, 255, 0.66);
  margin-bottom: 5px;
}

.main-title {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: 5px;
  white-space: nowrap;
  background: linear-gradient(180deg, #ffffff 18%, #e8f0ff 48%, #99b4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-subline {
  margin-top: 6px;
  font-size: 11px;
  letter-spacing: 2.6px;
  color: rgba(186, 221, 245, 0.58);
}

.title-bracket {
  position: absolute;
  top: 50%;
  width: 18px;
  height: 42px;
  border-top: 1px solid rgba(99, 126, 234, 0.7);
  border-bottom: 1px solid rgba(99, 126, 234, 0.7);
  transform: translateY(-50%);
}

.title-bracket-left {
  left: 20px;
  border-left: 1px solid rgba(99, 126, 234, 0.7);
}

.title-bracket-right {
  right: 20px;
  border-right: 1px solid rgba(99, 126, 234, 0.7);
}

.title-ornament {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 114px;
}

.ornament-line {
  display: block;
  width: 56px;
  height: 2px;
  background: linear-gradient(90deg, rgba(99, 126, 234, 0), rgba(99, 126, 234, 0.75));
}

.ornament-line.short {
  width: 28px;
  opacity: 0.7;
}

.ornament-diamond {
  width: 12px;
  height: 12px;
  border: 1px solid rgba(99, 126, 234, 0.75);
  transform: rotate(45deg);
  background: rgba(20, 26, 48, 0.6);
}

.title-ornament-right {
  transform: scaleX(-1);
}

.datetime-card {
  min-height: 68px;
  min-width: 360px;
  padding: 12px 40px;
  border: 1px solid rgba(99, 126, 234, 0.18);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    linear-gradient(135deg, rgba(20, 26, 48, 0.85), rgba(15, 22, 45, 0.7)),
    linear-gradient(90deg, rgba(99, 126, 234, 0.05), transparent 70%);
  box-shadow:
    inset 0 0 24px rgba(99, 126, 234, 0.05),
    inset 0 0 0 1px rgba(255, 255, 255, 0.02),
    0 0 24px rgba(99, 126, 234, 0.06);
}

.datetime-block {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: center;
  justify-items: center;
  gap: 16px;
  white-space: nowrap;
}

.datetime-segment {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.segment-kicker {
  font-size: 9px;
  letter-spacing: 2px;
  color: rgba(155, 205, 236, 0.45);
}

.date-text,
.weekday-text,
.time-text {
  font-size: 18px;
}

.date-text {
  color: rgba(214, 230, 248, 0.78);
}

.weekday-text {
  color: rgba(0, 229, 255, 0.78);
}

.time-segment {
  align-items: center;
}

.time-text {
  font-weight: 700;
  color: #00e5ff;
  letter-spacing: 2.4px;
  font-family: "Courier New", "Microsoft YaHei", monospace;
  text-shadow:
    0 0 10px rgba(0, 229, 255, 0.35),
    0 0 18px rgba(0, 229, 255, 0.18);
}

.divider {
  width: 1px;
  align-self: stretch;
  background: linear-gradient(180deg, rgba(99, 126, 234, 0), rgba(99, 126, 234, 0.4), rgba(99, 126, 234, 0));
}

.scan-line {
  position: absolute;
  top: 0;
  left: -20%;
  width: 40%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(120, 240, 255, 0.12), rgba(120, 240, 255, 0.02), transparent);
  transform: skewX(-24deg);
  animation: scan-sweep 6s linear infinite;
  pointer-events: none;
}

.content {
  flex: 1;
  overflow: hidden;
  position: relative;
  z-index: 1;
  margin: 0 16px;
}

.bottom-nav {
  position: relative;
  z-index: 50;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  margin: 0 16px 16px;
  background:
    linear-gradient(180deg, rgba(20, 26, 48, 0.95) 0%, rgba(15, 20, 40, 0.92) 100%),
    linear-gradient(90deg, rgba(99, 126, 234, 0.06), transparent 20%, rgba(168, 85, 247, 0.04) 50%, transparent 80%, rgba(99, 126, 234, 0.06));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(99, 126, 234, 0.2);
  border-radius: 20px;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.03),
    inset 0 0 40px rgba(99, 126, 234, 0.05),
    0 16px 40px rgba(0, 0, 0, 0.35),
    0 0 40px rgba(99, 126, 234, 0.08);
  overflow: hidden;
}

.bottom-nav-glow {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 100% 80% at 50% 100%, rgba(168, 85, 247, 0.1) 0%, transparent 50%),
    linear-gradient(90deg, transparent, rgba(99, 126, 234, 0.03), transparent);
  pointer-events: none;
}

.bottom-nav-noise {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.035) 0, rgba(255, 255, 255, 0.035) 1px, transparent 1px, transparent 4px);
  opacity: 0.18;
  pointer-events: none;
}

.bottom-nav .scan-line {
  position: absolute;
  bottom: 0;
  left: -20%;
  width: 40%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(120, 240, 255, 0.1), rgba(120, 240, 255, 0.02), transparent);
  transform: skewX(24deg);
  animation: scan-sweep 6s linear infinite;
  pointer-events: none;
}

.nav-items-wrapper {
  display: flex;
  gap: 8px;
  padding: 10px 16px;
  position: relative;
  z-index: 2;
}

.nav-ornament {
  display: flex;
  align-items: center;
  overflow: hidden;
  height: 44px;
  position: relative;
  z-index: 1;
}

.nav-ornament-left {
  justify-content: flex-end;
}

.nav-ornament-right {
  justify-content: flex-start;
}

.ornament-svg {
  width: 100%;
  height: 44px;
}

.nav-item {
  min-width: 100px;
  padding: 10px 16px;
  border: none;
  border-radius: 14px;
  background: transparent;
  color: rgba(224, 230, 240, 0.72);
  cursor: pointer;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.nav-item:hover {
  background: rgba(99, 126, 234, 0.1);
  color: rgba(224, 230, 240, 0.92);
}

.nav-item.active {
  color: #fff;
  background: linear-gradient(180deg, rgba(99, 126, 234, 0.25), rgba(60, 80, 150, 0.35));
  box-shadow: inset 0 0 20px rgba(99, 126, 234, 0.2), 0 0 20px rgba(99, 126, 234, 0.12);
}

.nav-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon svg {
  width: 100%;
  height: 100%;
}

.nav-label-cn,
.nav-label-en {
  display: block;
  text-align: center;
}

.nav-label-cn {
  font-size: 14px;
  font-weight: 600;
}

.nav-label-en {
  font-size: 10px;
  letter-spacing: 0.5px;
  color: rgba(224, 230, 240, 0.45);
}

.nav-item.active .nav-label-en {
  color: rgba(168, 85, 247, 0.8);
}

@keyframes pulse-dot {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow:
      0 0 0 4px rgba(0, 230, 118, 0.12),
      0 0 14px rgba(0, 230, 118, 0.7);
  }
  50% {
    opacity: 0.82;
    transform: scale(1.15);
    box-shadow:
      0 0 0 8px rgba(0, 230, 118, 0.06),
      0 0 20px rgba(0, 230, 118, 0.92);
  }
}

@keyframes scan-sweep {
  0% { transform: translateX(-160%) skewX(-24deg); }
  100% { transform: translateX(420%) skewX(-24deg); }
}

@keyframes title-float {
  0%, 100% {
    transform: translateY(0);
    box-shadow:
      inset 0 0 34px rgba(0, 136, 255, 0.1),
      inset 0 0 0 1px rgba(170, 238, 255, 0.04),
      0 0 26px rgba(0, 140, 255, 0.12);
  }
  50% {
    transform: translateY(-1px);
    box-shadow:
      inset 0 0 38px rgba(0, 136, 255, 0.12),
      inset 0 0 0 1px rgba(170, 238, 255, 0.05),
      0 0 34px rgba(0, 140, 255, 0.18);
  }
}

@media (max-width: 1100px) {
  .top-bar {
    margin: 12px 12px 0;
    padding: 14px 16px;
  }

  .top-bar-inner {
    grid-template-columns: 1fr;
    align-items: stretch;
  }

  .top-bar-left,
  .top-bar-right,
  .top-bar-center {
    justify-content: center;
  }

  .status-frame,
  .datetime-card {
    width: 100%;
  }

  .title-core {
    min-width: 0;
    width: 100%;
    padding: 12px 28px 14px;
  }

  .main-title {
    font-size: 24px;
    letter-spacing: 3px;
    white-space: normal;
  }

  .title-ornament {
    display: none;
  }

  .datetime-block {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .divider {
    display: none;
  }

  .time-segment {
    align-items: flex-start;
  }

  .bottom-nav {
    margin: 0 12px 12px;
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .nav-ornament {
    display: none;
  }

  .nav-items-wrapper {
    width: 100%;
    justify-content: center;
  }

  .nav-item {
    flex: 1;
    min-width: 0;
  }
}
</style>
