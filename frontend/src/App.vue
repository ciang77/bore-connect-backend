<script setup lang="ts">
import ChatBot from './components/ChatBot.vue'
import FaultPie from './components/FaultPie.vue'
import { ref, onMounted, onUnmounted } from 'vue'

const now = ref(new Date())
let timer: ReturnType<typeof setInterval> | undefined

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

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
onUnmounted(() => { clearInterval(timer) })
</script>

<template>
  <div class="page">
    <!-- 背景装饰 -->
    <div class="bg-grid"></div>
    <div class="bg-glow bg-glow-1"></div>
    <div class="bg-glow bg-glow-2"></div>

    <!-- 顶部标题栏 -->
    <header class="top-bar">
      <!-- 左右装饰角 -->
      <div class="corner corner-tl"></div>
      <div class="corner corner-tr"></div>
      <div class="top-bar-inner">
        <!-- 左侧：Logo + 状态 -->
        <div class="top-bar-left">
          <div class="logo">
            <svg viewBox="0 0 32 32" fill="none" class="logo-icon">
              <rect x="2" y="8" width="28" height="16" rx="4" stroke="currentColor" stroke-width="2"/>
              <circle cx="10" cy="16" r="3" fill="currentColor" opacity="0.6"/>
              <circle cx="22" cy="16" r="3" fill="currentColor" opacity="0.6"/>
              <line x1="16" y1="4" x2="16" y2="8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <circle cx="16" cy="3" r="2" fill="currentColor"/>
            </svg>
            <span class="status-dot"></span>
            <span class="status-text">系统运行中</span>
          </div>
        </div>

        <!-- 中间：标题 -->
        <div class="top-bar-center">
          <div class="title-deco title-deco-left"></div>
          <h1 class="main-title">龙门镗铣床智能管理平台</h1>
          <div class="title-deco title-deco-right"></div>
        </div>

        <!-- 右侧：日期时间 -->
        <div class="top-bar-right">
          <div class="datetime-block">
            <span class="date-text">{{ formatDate(now) }}</span>
            <span class="divider">|</span>
            <span class="weekday-text">{{ weekday(now) }}</span>
            <span class="divider">|</span>
            <span class="time-text">{{ formatTime(now) }}</span>
          </div>
        </div>
      </div>
      <!-- 底部扫描线 -->
      <div class="scan-line"></div>
    </header>

    <!-- 图表区域 -->
    <section class="charts-section">
      <FaultPie />
    </section>

    <!-- 智能助手浮窗 -->
    <ChatBot />
  </div>
</template>

<style>
/* ── 全局重置 ── */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  min-height: 100vh;
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  color: #e0e6f0;
  overflow-x: hidden;
}
</style>

<style scoped>
/* ── 页面背景 ── */
.page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1040 40%, #0d1b3e 100%);
  position: relative;
}

/* 网格背景 */
.bg-grid {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(100, 126, 234, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(100, 126, 234, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
}

/* 光晕装饰 */
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

/* ── 顶部标题栏 ── */
.top-bar {
  position: sticky;
  top: 28px;
  z-index: 100;
  background: linear-gradient(180deg, rgba(10, 14, 39, 0.95) 0%, rgba(10, 14, 39, 0.85) 100%);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(0, 180, 255, 0.15);
  padding: 20px 24px 10px;
}

/* 装饰角 */
.corner {
  position: absolute;
  width: 16px;
  height: 16px;
  pointer-events: none;
}
.corner-tl {
  top: 8px; left: 8px;
  border-top: 2px solid rgba(0, 180, 255, 0.4);
  border-left: 2px solid rgba(0, 180, 255, 0.4);
}
.corner-tr {
  top: 8px; right: 8px;
  border-top: 2px solid rgba(0, 180, 255, 0.4);
  border-right: 2px solid rgba(0, 180, 255, 0.4);
}

.top-bar-inner {
  max-width: 1400px;
  margin: 0 auto;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

/* 左侧 */
.top-bar-left {
  flex: 1;
  display: flex;
  align-items: center;
}
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.logo-icon {
  width: 32px;
  height: 32px;
  color: #00b4ff;
  filter: drop-shadow(0 0 6px rgba(0, 180, 255, 0.5));
}
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #00e676;
  box-shadow: 0 0 8px rgba(0, 230, 118, 0.6);
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.status-text {
  font-size: 20px;
  color: rgba(0, 180, 255, 0.7);
  letter-spacing: 1px;
}

/* 中间标题 */
.top-bar-center {
  flex: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}
.main-title {
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 8px;
  color: #fff;
  text-shadow:
    0 0 20px rgba(0, 180, 255, 0.5),
    0 0 40px rgba(0, 180, 255, 0.2);
  white-space: nowrap;
  background: linear-gradient(180deg, #ffffff 30%, #00b4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}
.title-deco {
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(0, 180, 255, 0.6), transparent);
  position: relative;
  flex-shrink: 0;
}
.title-deco::before {
  content: '';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  background: #00b4ff;
  box-shadow: 0 0 8px rgba(0, 180, 255, 0.8);
}
.title-deco-left::before { right: 0; }
.title-deco-right::before { left: 0; }

/* 右侧时间 */
.top-bar-right {
  flex: 1.2;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.datetime-block {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  white-space: nowrap;
  flex-shrink: 0;
}
.date-text {
  font-size: 20px;
  color: rgba(200, 215, 240, 0.6);
  letter-spacing: 1px;
}
.divider {
  color: rgba(0, 180, 255, 0.25);
  font-size: 12px;
}
.weekday-text {
  font-size: 20px;
  color: rgba(0, 180, 255, 0.6);
}
.time-text {
  font-size: 20px;
  font-weight: 700;
  color: #00e5ff;
  letter-spacing: 2px;
  font-family: "Courier New", "Microsoft YaHei", monospace;
  text-shadow: 0 0 10px rgba(0, 229, 255, 0.35);
}

/* 底部扫描线 */
.scan-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(0, 180, 255, 0.1) 20%,
    rgba(0, 180, 255, 0.5) 50%,
    rgba(0, 180, 255, 0.1) 80%,
    transparent 100%
  );
  animation: scan-sweep 4s ease-in-out infinite;
}
@keyframes scan-sweep {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* ── 图表区域 ── */
.charts-section {
  max-width: 600px;
  margin: 36px 16px 0 auto;
  padding: 0 24px;
}


</style>
