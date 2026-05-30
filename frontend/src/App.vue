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
  { name: 'dashboard', cn: '总览', path: '/', icon: '◈' },
  { name: 'smart-analysis', cn: '智能分析', path: '/smart-analysis', icon: '◆' },
  { name: 'system-status', cn: '系统状态', path: '/system-status', icon: '◉' },
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
              <div class="status-meta">系统状态</div>
              <div class="status-row">
                <span class="status-dot"></span>
                <span class="status-name">数控系统核心</span>
              </div>
              <div class="status-subrow">
                <span class="status-online">运行中</span>
                <span class="status-divider"></span>
                <span class="status-desc">边缘节点已连接</span>
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
      <div class="nav-corner nav-corner-tl"></div>
      <div class="nav-corner nav-corner-tr"></div>
      <div class="nav-corner nav-corner-bl"></div>
      <div class="nav-corner nav-corner-br"></div>
      <div class="nav-glow"></div>
      <div class="nav-noise"></div>
      <div class="nav-inner">
        <button
          v-for="item in navItems"
          :key="item.name"
          class="nav-item"
          :class="{ active: route.name === item.name }"
          @click="router.push(item.path)"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label-cn">{{ item.cn }}</span>
        </button>
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
  min-height: 100%;
}

body {
  height: 100vh;
  overflow: hidden;
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  color: #e0e6f0;
}
</style>

<style scoped>
.page {
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1040 40%, #0d1b3e 100%);
  position: relative;
  display: flex;
  flex-direction: column;
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
  position: relative;
  z-index: 40;
  margin: 10px 16px 0;
  flex-shrink: 0;
  background:
    linear-gradient(180deg, rgba(10, 14, 39, 0.96) 0%, rgba(6, 12, 34, 0.9) 100%),
    linear-gradient(90deg, rgba(0, 229, 255, 0.08), transparent 18%, rgba(102, 126, 234, 0.08) 50%, transparent 82%, rgba(0, 180, 255, 0.08));
  backdrop-filter: blur(18px);
  border: 1px solid rgba(0, 180, 255, 0.24);
  border-radius: 16px;
  padding: 10px 16px;
  box-shadow:
    inset 0 0 0 1px rgba(120, 223, 255, 0.05),
    inset 0 0 28px rgba(0, 180, 255, 0.06),
    0 10px 28px rgba(0, 0, 0, 0.34),
    0 0 28px rgba(0, 116, 255, 0.12);
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
  width: 18px;
  height: 18px;
  pointer-events: none;
  opacity: 0.9;
}

.corner-tl {
  top: 7px;
  left: 7px;
  border-top: 1.5px solid rgba(0, 229, 255, 0.5);
  border-left: 1.5px solid rgba(0, 229, 255, 0.5);
}

.corner-tr {
  top: 7px;
  right: 7px;
  border-top: 1.5px solid rgba(0, 229, 255, 0.5);
  border-right: 1.5px solid rgba(0, 229, 255, 0.5);
}

.corner-bl {
  bottom: 7px;
  left: 7px;
  border-bottom: 1.5px solid rgba(102, 126, 234, 0.5);
  border-left: 1.5px solid rgba(102, 126, 234, 0.5);
}

.corner-br {
  bottom: 7px;
  right: 7px;
  border-bottom: 1.5px solid rgba(102, 126, 234, 0.5);
  border-right: 1.5px solid rgba(102, 126, 234, 0.5);
}

.top-bar-inner {
  max-width: 1600px;
  margin: 0 auto;
  min-height: 56px;
  display: grid;
  grid-template-columns: minmax(200px, 1fr) minmax(420px, 1.6fr) minmax(260px, 1fr);
  align-items: center;
  position: relative;
  gap: 14px;
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
  min-height: 50px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  padding: 8px 12px;
  border: 1px solid rgba(77, 204, 255, 0.22);
  border-radius: 10px;
  background:
    linear-gradient(135deg, rgba(4, 18, 47, 0.92), rgba(8, 23, 56, 0.52)),
    linear-gradient(90deg, rgba(0, 180, 255, 0.08), transparent 70%);
  box-shadow:
    inset 0 0 16px rgba(0, 180, 255, 0.08),
    inset 0 0 0 1px rgba(172, 234, 255, 0.04),
    0 0 16px rgba(0, 114, 255, 0.08);
}

.status-meta {
  font-size: 9px;
  letter-spacing: 2.2px;
  color: rgba(170, 223, 255, 0.54);
  text-transform: uppercase;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: radial-gradient(circle, #75ff9b 0%, #00e676 65%, #00b85b 100%);
  box-shadow:
    0 0 0 3px rgba(0, 230, 118, 0.12),
    0 0 10px rgba(0, 230, 118, 0.7);
  animation: pulse-dot 2.2s ease-in-out infinite;
}

.status-name {
  font-size: 15px;
  color: rgba(225, 246, 255, 0.96);
  letter-spacing: 1.4px;
  font-weight: 600;
}

.status-subrow {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(181, 223, 246, 0.6);
  font-size: 10px;
  letter-spacing: 1.2px;
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
  gap: 12px;
}

.title-core {
  min-width: 480px;
  padding: 8px 40px 10px;
  position: relative;
  text-align: center;
  border: 1px solid rgba(58, 188, 255, 0.24);
  background:
    linear-gradient(180deg, rgba(5, 21, 52, 0.9), rgba(7, 23, 48, 0.56)),
    linear-gradient(90deg, rgba(0, 180, 255, 0.1), transparent 18%, rgba(102, 126, 234, 0.08) 50%, transparent 82%, rgba(0, 180, 255, 0.1));
  clip-path: polygon(16px 0, calc(100% - 16px) 0, 100% 50%, calc(100% - 16px) 100%, 16px 100%, 0 50%);
  box-shadow:
    inset 0 0 26px rgba(0, 136, 255, 0.1),
    inset 0 0 0 1px rgba(170, 238, 255, 0.04),
    0 0 20px rgba(0, 140, 255, 0.12);
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
  width: 50px;
  height: 1.5px;
  background: linear-gradient(90deg, rgba(0, 214, 255, 0), rgba(0, 214, 255, 0.9));
}

.title-core::before {
  left: -36px;
}

.title-core::after {
  right: -36px;
  transform: scaleX(-1);
}

.title-code {
  font-size: 9px;
  letter-spacing: 2.4px;
  color: rgba(159, 220, 255, 0.66);
  margin-bottom: 3px;
}

.main-title {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 4px;
  white-space: nowrap;
  background: linear-gradient(180deg, #ffffff 18%, #dff7ff 48%, #00b4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow:
    0 0 14px rgba(0, 180, 255, 0.16),
    0 0 24px rgba(0, 180, 255, 0.18);
}

.title-subline {
  margin-top: 4px;
  font-size: 10px;
  letter-spacing: 2px;
  color: rgba(186, 221, 245, 0.58);
}

.title-bracket {
  position: absolute;
  top: 50%;
  width: 14px;
  height: 32px;
  border-top: 1px solid rgba(70, 206, 255, 0.84);
  border-bottom: 1px solid rgba(70, 206, 255, 0.84);
  transform: translateY(-50%);
}

.title-bracket-left {
  left: 14px;
  border-left: 1px solid rgba(70, 206, 255, 0.84);
}

.title-bracket-right {
  right: 14px;
  border-right: 1px solid rgba(70, 206, 255, 0.84);
}

.title-ornament {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 86px;
}

.ornament-line {
  display: block;
  width: 42px;
  height: 1.5px;
  background: linear-gradient(90deg, rgba(0, 180, 255, 0), rgba(0, 180, 255, 0.82));
  box-shadow: 0 0 8px rgba(0, 180, 255, 0.18);
}

.ornament-line.short {
  width: 20px;
  opacity: 0.75;
}

.ornament-diamond {
  width: 10px;
  height: 10px;
  border: 1px solid rgba(0, 229, 255, 0.82);
  transform: rotate(45deg);
  box-shadow: 0 0 10px rgba(0, 180, 255, 0.14);
  background: rgba(6, 30, 68, 0.55);
}

.title-ornament-right {
  transform: scaleX(-1);
}

.datetime-card {
  min-height: 50px;
  min-width: 280px;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  border: 1px solid rgba(54, 168, 255, 0.18);
  border-radius: 10px;
  background:
    linear-gradient(135deg, rgba(7, 18, 46, 0.72), rgba(5, 19, 42, 0.96)),
    linear-gradient(90deg, rgba(0, 180, 255, 0.06), transparent 70%);
  box-shadow:
    inset 0 0 16px rgba(0, 140, 255, 0.06),
    inset 0 0 0 1px rgba(168, 226, 255, 0.04),
    0 0 16px rgba(0, 114, 255, 0.08);
}

.datetime-label {
  font-size: 9px;
  letter-spacing: 2px;
  color: rgba(165, 212, 247, 0.6);
  margin-bottom: 5px;
  text-align: right;
}

.datetime-block {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: stretch;
  gap: 10px;
  white-space: nowrap;
}

.datetime-segment {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.segment-kicker {
  font-size: 8px;
  letter-spacing: 1.6px;
  color: rgba(155, 205, 236, 0.45);
}

.date-text,
.weekday-text,
.time-text {
  font-size: 15px;
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
  flex: 1;
  overflow: hidden;
  padding: 10px 0;
}

.bottom-nav {
  position: relative;
  align-self: center;
  z-index: 50;
  flex-shrink: 0;
  margin-bottom: 10px;
  background:
    linear-gradient(180deg, rgba(6, 12, 34, 0.9) 0%, rgba(10, 14, 39, 0.96) 100%),
    linear-gradient(90deg, rgba(0, 229, 255, 0.08), transparent 18%, rgba(102, 126, 234, 0.08) 50%, transparent 82%, rgba(0, 180, 255, 0.08));
  backdrop-filter: blur(18px);
  border: 1px solid rgba(0, 180, 255, 0.24);
  border-radius: 16px;
  padding: 10px 20px;
  box-shadow:
    inset 0 0 0 1px rgba(120, 223, 255, 0.05),
    inset 0 0 28px rgba(0, 180, 255, 0.06),
    0 10px 28px rgba(0, 0, 0, 0.34),
    0 0 28px rgba(0, 116, 255, 0.12);
  overflow: hidden;
}

.nav-inner {
  display: flex;
  align-items: center;
  gap: 32px;
  position: relative;
  z-index: 1;
}

.nav-glow {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 50% 100%, rgba(32, 196, 255, 0.16), transparent 36%),
    linear-gradient(90deg, transparent, rgba(54, 204, 255, 0.06), transparent);
  pointer-events: none;
}

.nav-noise {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.035) 0, rgba(255, 255, 255, 0.035) 1px, transparent 1px, transparent 4px);
  opacity: 0.18;
  pointer-events: none;
}

.nav-corner {
  position: absolute;
  width: 14px;
  height: 14px;
  pointer-events: none;
  opacity: 0.9;
}

.nav-corner-tl {
  top: 4px;
  left: 4px;
  border-top: 1.5px solid rgba(0, 229, 255, 0.5);
  border-left: 1.5px solid rgba(0, 229, 255, 0.5);
}

.nav-corner-tr {
  top: 4px;
  right: 4px;
  border-top: 1.5px solid rgba(0, 229, 255, 0.5);
  border-right: 1.5px solid rgba(0, 229, 255, 0.5);
}

.nav-corner-bl {
  bottom: 4px;
  left: 4px;
  border-bottom: 1.5px solid rgba(102, 126, 234, 0.5);
  border-left: 1.5px solid rgba(102, 126, 234, 0.5);
}

.nav-corner-br {
  bottom: 4px;
  right: 4px;
  border-bottom: 1.5px solid rgba(102, 126, 234, 0.5);
  border-right: 1.5px solid rgba(102, 126, 234, 0.5);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 4px;
  border: none;
  border-radius: 0;
  background: transparent;
  color: rgba(224, 230, 240, 0.45);
  cursor: pointer;
  transition: color 0.25s ease;
}

.nav-item:hover {
  color: rgba(224, 230, 240, 0.75);
}

.nav-item.active {
  color: #00e5ff;
  text-shadow: 0 0 12px rgba(0, 229, 255, 0.3);
}

.nav-icon {
  font-size: 18px;
  line-height: 1;
  transition: inherit;
  opacity: 0.7;
}

.nav-item.active .nav-icon {
  opacity: 1;
  text-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
}

.nav-label-cn {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.2;
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

</style>
