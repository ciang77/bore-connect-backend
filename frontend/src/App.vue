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
  { name: 'dashboard', cn: '综合总览', en: 'Dashboard', path: '/' },
  { name: 'spindle', cn: '主轴监控', en: 'Spindle', path: '/spindle' },
  { name: 'diagnosis', cn: '故障诊断', en: 'Diagnosis', path: '/diagnosis' },
  { name: 'equipment', cn: '设备管理', en: 'Equipment', path: '/equipment' },
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
              <div class="status-meta">SYSTEM STATUS</div>
              <div class="status-row">
                <span class="status-dot"></span>
                <span class="status-name">CNC CONTROL CORE</span>
              </div>
              <div class="status-subrow">
                <span class="status-online">ONLINE</span>
                <span class="status-divider"></span>
                <span class="status-desc">EDGE NODE CONNECTED</span>
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
            <div class="title-code">SYSTEM-ID: CNC-HUB-01</div>
            <h1 class="main-title">龙门镗铣床智能管理平台</h1>
            <div class="title-subline">LONGMEN BORING &amp; MILLING MACHINE INTELLIGENT CONTROL CENTER</div>
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
            <div class="datetime-label">REALTIME CLOCK</div>
            <div class="datetime-block">
              <div class="datetime-segment">
                <span class="segment-kicker">DATE</span>
                <span class="date-text">{{ formatDate(now) }}</span>
              </div>
              <span class="divider"></span>
              <div class="datetime-segment">
                <span class="segment-kicker">WEEK</span>
                <span class="weekday-text">{{ weekday(now) }}</span>
              </div>
              <span class="divider"></span>
              <div class="datetime-segment time-segment">
                <span class="segment-kicker">TIME</span>
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
      <button
        v-for="item in navItems"
        :key="item.name"
        class="nav-item"
        :class="{ active: route.name === item.name }"
        @click="router.push(item.path)"
      >
        <span class="nav-label-cn">{{ item.cn }}</span>
        <span class="nav-label-en">{{ item.en }}</span>
      </button>
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
  min-height: 100%;
}

body {
  min-height: 100vh;
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  color: #e0e6f0;
  overflow-x: hidden;
}
</style>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1040 40%, #0d1b3e 100%);
  position: relative;
  padding-bottom: 112px;
}

.bg-grid {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(100, 126, 234, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(100, 126, 234, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
}

.bg-glow {
  position: fixed;
  border-radius: 50%;
  filter: blur(100px);
  pointer-events: none;
  opacity: 0.3;
}

.bg-glow-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #667eea 0%, transparent 70%);
  top: -200px;
  right: -100px;
}

.bg-glow-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #764ba2 0%, transparent 70%);
  bottom: -200px;
  left: -100px;
}

.top-bar {
  position: sticky;
  top: 14px;
  z-index: 40;
  margin: 0 16px;
  background:
    linear-gradient(180deg, rgba(10, 14, 39, 0.96) 0%, rgba(6, 12, 34, 0.9) 100%),
    linear-gradient(90deg, rgba(0, 229, 255, 0.08), transparent 18%, rgba(102, 126, 234, 0.08) 50%, transparent 82%, rgba(0, 180, 255, 0.08));
  backdrop-filter: blur(18px);
  border: 1px solid rgba(0, 180, 255, 0.24);
  border-radius: 20px;
  padding: 14px 22px;
  box-shadow:
    inset 0 0 0 1px rgba(120, 223, 255, 0.05),
    inset 0 0 38px rgba(0, 180, 255, 0.06),
    0 14px 38px rgba(0, 0, 0, 0.34),
    0 0 36px rgba(0, 116, 255, 0.12);
  overflow: hidden;
}

.top-bar-glow {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 50% 0%, rgba(32, 196, 255, 0.16), transparent 36%),
    linear-gradient(90deg, transparent, rgba(54, 204, 255, 0.06), transparent);
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
  border-top: 2px solid rgba(0, 229, 255, 0.5);
  border-left: 2px solid rgba(0, 229, 255, 0.5);
}

.corner-tr {
  top: 10px;
  right: 10px;
  border-top: 2px solid rgba(0, 229, 255, 0.5);
  border-right: 2px solid rgba(0, 229, 255, 0.5);
}

.corner-bl {
  bottom: 10px;
  left: 10px;
  border-bottom: 2px solid rgba(102, 126, 234, 0.5);
  border-left: 2px solid rgba(102, 126, 234, 0.5);
}

.corner-br {
  bottom: 10px;
  right: 10px;
  border-bottom: 2px solid rgba(102, 126, 234, 0.5);
  border-right: 2px solid rgba(102, 126, 234, 0.5);
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
  border: 1px solid rgba(77, 204, 255, 0.22);
  border-radius: 14px;
  background:
    linear-gradient(135deg, rgba(4, 18, 47, 0.92), rgba(8, 23, 56, 0.52)),
    linear-gradient(90deg, rgba(0, 180, 255, 0.08), transparent 70%);
  box-shadow:
    inset 0 0 22px rgba(0, 180, 255, 0.08),
    inset 0 0 0 1px rgba(172, 234, 255, 0.04),
    0 0 22px rgba(0, 114, 255, 0.08);
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
  color: #87ffaf;
  text-shadow: 0 0 10px rgba(0, 230, 118, 0.3);
}

.status-divider {
  width: 24px;
  height: 1px;
  background: linear-gradient(90deg, rgba(0, 229, 255, 0.1), rgba(0, 229, 255, 0.7), rgba(0, 229, 255, 0.1));
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
  border: 1px solid rgba(58, 188, 255, 0.24);
  background:
    linear-gradient(180deg, rgba(5, 21, 52, 0.9), rgba(7, 23, 48, 0.56)),
    linear-gradient(90deg, rgba(0, 180, 255, 0.1), transparent 18%, rgba(102, 126, 234, 0.08) 50%, transparent 82%, rgba(0, 180, 255, 0.1));
  clip-path: polygon(22px 0, calc(100% - 22px) 0, 100% 50%, calc(100% - 22px) 100%, 22px 100%, 0 50%);
  box-shadow:
    inset 0 0 34px rgba(0, 136, 255, 0.1),
    inset 0 0 0 1px rgba(170, 238, 255, 0.04),
    0 0 26px rgba(0, 140, 255, 0.12);
  animation: title-float 5.5s ease-in-out infinite;
}

.title-glow {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 50% 50%, rgba(0, 229, 255, 0.12), transparent 58%),
    linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.04), transparent);
  pointer-events: none;
}

.title-core::before,
.title-core::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 70px;
  height: 2px;
  background: linear-gradient(90deg, rgba(0, 214, 255, 0), rgba(0, 214, 255, 0.9));
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
  background: linear-gradient(180deg, #ffffff 18%, #dff7ff 48%, #00b4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow:
    0 0 18px rgba(0, 180, 255, 0.16),
    0 0 32px rgba(0, 180, 255, 0.18);
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
  border-top: 1px solid rgba(70, 206, 255, 0.84);
  border-bottom: 1px solid rgba(70, 206, 255, 0.84);
  transform: translateY(-50%);
}

.title-bracket-left {
  left: 20px;
  border-left: 1px solid rgba(70, 206, 255, 0.84);
}

.title-bracket-right {
  right: 20px;
  border-right: 1px solid rgba(70, 206, 255, 0.84);
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
  background: linear-gradient(90deg, rgba(0, 180, 255, 0), rgba(0, 180, 255, 0.82));
  box-shadow: 0 0 10px rgba(0, 180, 255, 0.18);
}

.ornament-line.short {
  width: 28px;
  opacity: 0.75;
}

.ornament-diamond {
  width: 12px;
  height: 12px;
  border: 1px solid rgba(0, 229, 255, 0.82);
  transform: rotate(45deg);
  box-shadow: 0 0 12px rgba(0, 180, 255, 0.14);
  background: rgba(6, 30, 68, 0.55);
}

.title-ornament-right {
  transform: scaleX(-1);
}

.datetime-card {
  min-height: 68px;
  min-width: 360px;
  padding: 12px 16px;
  border: 1px solid rgba(54, 168, 255, 0.18);
  border-radius: 14px;
  background:
    linear-gradient(135deg, rgba(7, 18, 46, 0.72), rgba(5, 19, 42, 0.96)),
    linear-gradient(90deg, rgba(0, 180, 255, 0.06), transparent 70%);
  box-shadow:
    inset 0 0 22px rgba(0, 140, 255, 0.06),
    inset 0 0 0 1px rgba(168, 226, 255, 0.04),
    0 0 22px rgba(0, 114, 255, 0.08);
}

.datetime-label {
  font-size: 10px;
  letter-spacing: 2.6px;
  color: rgba(165, 212, 247, 0.6);
  margin-bottom: 8px;
  text-align: right;
}

.datetime-block {
  display: grid;
  grid-template-columns: 1fr auto 0.8fr auto 1fr;
  align-items: stretch;
  gap: 12px;
  white-space: nowrap;
}

.datetime-segment {
  display: flex;
  flex-direction: column;
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
  align-items: flex-end;
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
  background: linear-gradient(180deg, rgba(0, 180, 255, 0), rgba(0, 180, 255, 0.52), rgba(0, 180, 255, 0));
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
  position: relative;
  z-index: 1;
  padding-top: 22px;
}

.bottom-nav {
  position: fixed;
  left: 50%;
  bottom: 24px;
  transform: translateX(-50%);
  z-index: 50;
  display: flex;
  gap: 12px;
  padding: 8px;
  border: 1px solid rgba(0, 180, 255, 0.18);
  border-radius: 18px;
  background: rgba(7, 18, 42, 0.88);
  backdrop-filter: blur(18px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.32), 0 0 24px rgba(0, 119, 255, 0.12);
}

.nav-item {
  min-width: 148px;
  padding: 12px 18px;
  border: 1px solid transparent;
  border-radius: 14px;
  background: transparent;
  color: rgba(224, 230, 240, 0.72);
  cursor: pointer;
  transition: all 0.25s ease;
}

.nav-item:hover {
  border-color: rgba(0, 180, 255, 0.18);
  background: rgba(0, 180, 255, 0.05);
}

.nav-item.active {
  color: #fff;
  border-color: rgba(47, 203, 255, 0.42);
  background: linear-gradient(180deg, rgba(10, 99, 255, 0.18), rgba(8, 29, 77, 0.32));
  box-shadow: inset 0 0 18px rgba(0, 180, 255, 0.14), 0 0 20px rgba(0, 180, 255, 0.08);
}

.nav-label-cn,
.nav-label-en {
  display: block;
  text-align: center;
}

.nav-label-cn {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.nav-label-en {
  font-size: 11px;
  letter-spacing: 1px;
  color: rgba(224, 230, 240, 0.52);
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
    top: 12px;
    margin: 0 12px;
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
    width: calc(100% - 24px);
  }

  .nav-item {
    flex: 1;
    min-width: 0;
  }
}
</style>
