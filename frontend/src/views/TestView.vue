<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
} from 'echarts/components'
import { fetchRealtimeData } from '../api/test'
import { useEventSource } from '../composables/useEventSource'

use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
])

const ACT_COLOR = '#448aff'
const SET_COLOR = '#ffab40'
const SPEED_COLOR = '#69f0ae'

const timeRange = ref<'24h' | '7d'>('24h')
const actPosition = ref<number[]>([])
const setPosition = ref<number[]>([])
const speedData = ref<number[]>([])
const timeLabels = ref<string[]>([])

const showAct = ref(true)
const showSet = ref(true)
const showSpeed = ref(true)

// 延迟计算（毫秒）
const latencyMs = ref<number | null>(null)
function updateLatency(latestTime: string | null) {
  if (latestTime) {
    latencyMs.value = Date.now() - new Date(latestTime).getTime()
  }
}

// 最新实时值（来自 realtime_data 覆盖表）
const latestValues = ref<Record<string, { value: number; time: string }>>({})
function updateLatestValues(vals: Record<string, { value: number; time: string }> | undefined) {
  if (vals) latestValues.value = vals
}

const chartRef = ref<HTMLDivElement>()
let chartInst: echarts.ECharts | null = null
let resizeHandler: (() => void) | undefined

const streamUrl = computed(() => `/api/test/realtime-data/stream?range=${timeRange.value}`)

function buildOption(labels: string[], act: number[], set_: number[], spd: number[]) {
  return {
    backgroundColor: 'transparent',
    grid: { left: 55, right: 70, top: 40, bottom: 32 },
    xAxis: {
      type: 'category',
      data: labels,
      boundaryGap: false,
      axisLine: { lineStyle: { color: 'rgba(0, 191, 255, 0.25)', width: 1 } },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(148, 163, 184, 0.8)',
        fontSize: 10,
        interval: Math.max(1, Math.floor(labels.length / 8)),
      },
    },
    yAxis: [
      {
        type: 'value',
        name: '位置 (mm)',
        nameTextStyle: { color: ACT_COLOR, fontSize: 11, fontWeight: 500 },
        axisLabel: { color: 'rgba(148, 163, 184, 0.75)', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(0, 191, 255, 0.08)', type: 'dashed', width: 1 } },
        show: true,
      },
      {
        type: 'value',
        name: '速度 (mm/s)',
        nameTextStyle: { color: SPEED_COLOR, fontSize: 11, fontWeight: 500 },
        axisLabel: { color: 'rgba(148, 163, 184, 0.75)', fontSize: 10 },
        splitLine: { show: false },
        show: true,
      },
    ],
    series: [
      {
        name: '实际位置',
        type: 'line',
        yAxisIndex: 0,
        data: showAct.value ? act : [],
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: ACT_COLOR, width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(68, 138, 255, 0.2)' },
            { offset: 1, color: 'rgba(68, 138, 255, 0.02)' },
          ]),
        },
      },
      {
        name: '设定位置',
        type: 'line',
        yAxisIndex: 0,
        data: showSet.value ? set_ : [],
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: SET_COLOR, width: 2, type: 'dashed' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 171, 64, 0.15)' },
            { offset: 1, color: 'rgba(255, 171, 64, 0.02)' },
          ]),
        },
      },
      {
        name: '速度',
        type: 'line',
        yAxisIndex: 1,
        data: showSpeed.value ? spd : [],
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: SPEED_COLOR, width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(105, 240, 174, 0.15)' },
            { offset: 1, color: 'rgba(105, 240, 174, 0.02)' },
          ]),
        },
      },
    ],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(10, 20, 40, 0.95)',
      borderColor: 'rgba(0, 191, 255, 0.3)',
      borderWidth: 1,
      textStyle: { color: '#e2e8f0', fontSize: 12 },
      formatter: (params: any) => {
        let html = `<b style="color:#00d4ff">${params[0].axisValue}</b><br/>`
        params.forEach((p: any) => {
          const unit = p.seriesName === '速度' ? 'mm/s' : 'mm'
          html += `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p.color};margin-right:6px;"></span>${p.seriesName}: <b>${p.value}</b> ${unit}<br/>`
        })
        return html
      },
    },
    legend: {
      show: true,
      bottom: 0,
      textStyle: { color: 'rgba(148, 163, 184, 0.8)', fontSize: 11 },
      data: ['实际位置', '设定位置', '速度'],
    },
  }
}

async function loadData(range: '24h' | '7d') {
  try {
    const res = await fetchRealtimeData(range)
    if (res.code === 0 && res.data) {
      timeLabels.value = res.data.labels
      actPosition.value = res.data.actPosition
      setPosition.value = res.data.setPosition
      speedData.value = res.data.speed
      updateLatency(res.data.latestTime)
      updateLatestValues(res.data.latestValues)
      updateChart()
    }
  } catch {
    // keep last data
  }
}

function updateChart() {
  if (chartInst && !chartInst.isDisposed()) {
    chartInst.setOption(
      buildOption(timeLabels.value, actPosition.value, setPosition.value, speedData.value),
      true
    )
  }
}

function toggleParam(param: 'act' | 'set' | 'speed') {
  if (param === 'act') showAct.value = !showAct.value
  if (param === 'set') showSet.value = !showSet.value
  if (param === 'speed') showSpeed.value = !showSpeed.value
  updateChart()
}

function switchRange(range: '24h' | '7d') {
  timeRange.value = range
  loadData(range)
}

// SSE — 必须在 setup 同步阶段注册
useEventSource(streamUrl, (data: { labels: string[]; actPosition: number[]; setPosition: number[]; speed: number[]; latestTime: string | null; latestValues?: Record<string, { value: number; time: string }> }) => {
  timeLabels.value = data.labels
  actPosition.value = data.actPosition
  setPosition.value = data.setPosition
  speedData.value = data.speed
  updateLatency(data.latestTime)
  updateLatestValues(data.latestValues)
  updateChart()
})

onMounted(async () => {
  await loadData('24h')
  await nextTick()
  if (chartRef.value) {
    chartInst = echarts.init(chartRef.value)
    chartInst.setOption(
      buildOption(timeLabels.value, actPosition.value, setPosition.value, speedData.value)
    )
  }
  resizeHandler = () => chartInst?.resize()
  window.addEventListener('resize', resizeHandler)
})

onUnmounted(() => {
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  chartInst?.dispose()
})
</script>

<template>
  <div class="view">
    <div class="content-wrapper">
      <div class="border-box">
        <div class="border-top">
          <div class="corner top-left"></div>
          <div class="title-bar">
            <div class="title-decoration left">
              <div class="deco-wave"></div>
              <div class="deco-dot"></div>
              <div class="deco-line"></div>
            </div>
            <h2 class="title-text">X轴 实时数据监控</h2>
            <div class="title-decoration right">
              <div class="deco-line"></div>
              <div class="deco-dot"></div>
              <div class="deco-wave"></div>
            </div>
          </div>
          <div class="corner top-right"></div>
        </div>
        <div class="border-body">
          <div class="side-line left"></div>
          <div class="content-area">
            <div class="chart-ref" ref="chartRef"></div>
            <!-- 实时值小窗 -->
            <div class="realtime-panel" v-if="latestValues['axis_x_actPosition']">
              <div class="realtime-panel-title">实时数值</div>
              <div class="realtime-row">
                <span class="realtime-dot act"></span>
                <span class="realtime-label">实际位置</span>
                <span class="realtime-value act-val">{{ latestValues['axis_x_actPosition']?.value?.toFixed(3) ?? '-' }}</span>
                <span class="realtime-unit">mm</span>
              </div>
              <div class="realtime-row">
                <span class="realtime-dot set"></span>
                <span class="realtime-label">设定位置</span>
                <span class="realtime-value set-val">{{ latestValues['axis_x_setPosition']?.value?.toFixed(3) ?? '-' }}</span>
                <span class="realtime-unit">mm</span>
              </div>
              <div class="realtime-row">
                <span class="realtime-dot speed"></span>
                <span class="realtime-label">速度</span>
                <span class="realtime-value speed-val">{{ latestValues['axis_x_speed']?.value?.toFixed(3) ?? '-' }}</span>
                <span class="realtime-unit">mm/s</span>
              </div>
            </div>
          </div>
          <div class="side-line right"></div>
        </div>
        <div class="trend-control-bar">
          <div class="param-group">
            <div class="param-item" :class="{ active: showAct }" @click="toggleParam('act')">
              <span class="param-dot act"></span>
              <span class="param-label">实际位置</span>
            </div>
            <div class="param-item" :class="{ active: showSet }" @click="toggleParam('set')">
              <span class="param-dot set"></span>
              <span class="param-label">设定位置</span>
            </div>
            <div class="param-item" :class="{ active: showSpeed }" @click="toggleParam('speed')">
              <span class="param-dot speed"></span>
              <span class="param-label">速度</span>
            </div>
          </div>
          <div class="latency-display" v-if="latencyMs !== null">
            <span class="latency-label">延迟</span>
            <span class="latency-value" :class="latencyMs < 500 ? 'latency-good' : latencyMs < 2000 ? 'latency-warn' : 'latency-bad'">
              {{ latencyMs }} ms
            </span>
          </div>
          <div class="time-toggle">
            <button class="time-btn" :class="{ active: timeRange === '24h' }" @click="switchRange('24h')">
              <span class="btn-indicator"></span>
              <span class="btn-text">日</span>
            </button>
            <button class="time-btn" :class="{ active: timeRange === '7d' }" @click="switchRange('7d')">
              <span class="btn-indicator"></span>
              <span class="btn-text">周</span>
            </button>
          </div>
        </div>
        <div class="border-bottom">
          <div class="corner bottom-left"></div>
          <div class="bottom-center"></div>
          <div class="corner bottom-right"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 10px;
  color: #e2e8f0;
  box-sizing: border-box;
}

.content-wrapper {
  flex: 1;
  min-height: 0;
}

.border-box {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, rgba(10, 20, 40, 0.95), rgba(15, 25, 50, 0.9));
  border-radius: 4px;
  position: relative;
  border: 1px solid rgba(0, 191, 255, 0.15);
}

.border-top {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 42px;
  background: linear-gradient(180deg, rgba(20, 35, 65, 0.98), rgba(15, 28, 55, 0.95));
  border-bottom: 1px solid rgba(0, 191, 255, 0.1);
}

.border-bottom {
  display: flex;
  align-items: center;
  height: 20px;
  background: linear-gradient(180deg, rgba(15, 28, 55, 0.95), rgba(10, 20, 40, 0.98));
  border-top: 1px solid rgba(0, 191, 255, 0.1);
  position: relative;
}

.border-body {
  flex: 1;
  display: flex;
  min-height: 0;
}

.title-bar {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  height: 100%;
}

.title-decoration {
  display: flex;
  align-items: center;
  gap: 4px;
}

.deco-wave {
  width: 8px;
  height: 4px;
  background: rgba(0, 191, 255, 0.4);
  border-radius: 2px;
}

.deco-dot {
  width: 6px;
  height: 6px;
  background: rgba(102, 126, 234, 0.6);
  border-radius: 50%;
}

.deco-line {
  width: 12px;
  height: 2px;
  background: linear-gradient(90deg, rgba(0, 191, 255, 0.5), rgba(102, 126, 234, 0.5));
}

.title-text {
  font-size: 14px;
  font-weight: 600;
  color: #00d4ff;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
  margin: 0;
  white-space: nowrap;
}

.corner {
  width: 16px;
  height: 16px;
  position: absolute;
  z-index: 10;
}

.corner::before,
.corner::after {
  content: '';
  position: absolute;
  background: rgba(0, 191, 255, 0.6);
}

.corner.top-left {
  top: -1px;
  left: -1px;
}

.corner.top-left::before {
  top: 0;
  left: 0;
  width: 16px;
  height: 3px;
  border-radius: 0 0 2px 0;
}

.corner.top-left::after {
  top: 0;
  left: 0;
  width: 3px;
  height: 16px;
  border-radius: 0 0 2px 0;
}

.corner.top-right {
  top: -1px;
  right: -1px;
}

.corner.top-right::before {
  top: 0;
  right: 0;
  width: 16px;
  height: 3px;
  border-radius: 0 0 0 2px;
}

.corner.top-right::after {
  top: 0;
  right: 0;
  width: 3px;
  height: 16px;
  border-radius: 0 0 0 2px;
}

.corner.bottom-left {
  bottom: -1px;
  left: -1px;
}

.corner.bottom-left::before {
  bottom: 0;
  left: 0;
  width: 16px;
  height: 3px;
  border-radius: 0 2px 0 0;
}

.corner.bottom-left::after {
  bottom: 0;
  left: 0;
  width: 3px;
  height: 16px;
  border-radius: 0 2px 0 0;
}

.corner.bottom-right {
  bottom: -1px;
  right: -1px;
}

.corner.bottom-right::before {
  bottom: 0;
  right: 0;
  width: 16px;
  height: 3px;
  border-radius: 2px 0 0 0;
}

.corner.bottom-right::after {
  bottom: 0;
  right: 0;
  width: 3px;
  height: 16px;
  border-radius: 2px 0 0 0;
}

.bottom-center {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 191, 255, 0.3), transparent);
}

.side-line {
  width: 1px;
  background: linear-gradient(180deg, transparent, rgba(0, 191, 255, 0.3) 20%, rgba(0, 191, 255, 0.3) 80%, transparent);
}

.content-area {
  flex: 1;
  overflow: hidden;
  padding: 8px;
  box-sizing: border-box;
  display: flex;
  position: relative;
}

.chart-ref {
  flex: 1;
  min-height: 0;
  width: 100%;
}

/* ══════ 实时值面板 ══════ */
.realtime-panel {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
  min-width: 180px;
  padding: 12px 16px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(10, 20, 40, 0.94), rgba(15, 25, 50, 0.9));
  border: 1px solid rgba(0, 191, 255, 0.2);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 191, 255, 0.06);
  backdrop-filter: blur(8px);
}

.realtime-panel-title {
  font-size: 11px;
  font-weight: 600;
  color: rgba(0, 212, 255, 0.7);
  text-align: center;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0, 191, 255, 0.1);
  letter-spacing: 2px;
}

.realtime-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
}

.realtime-row + .realtime-row {
  border-top: 1px solid rgba(255, 255, 255, 0.03);
}

.realtime-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.realtime-dot.act { background: #448aff; box-shadow: 0 0 5px rgba(68, 138, 255, 0.6); }
.realtime-dot.set { background: #ffab40; box-shadow: 0 0 5px rgba(255, 171, 64, 0.6); }
.realtime-dot.speed { background: #69f0ae; box-shadow: 0 0 5px rgba(105, 240, 174, 0.6); }

.realtime-label {
  flex: 1;
  font-size: 11px;
  color: rgba(148, 163, 184, 0.7);
  white-space: nowrap;
}

.realtime-value {
  font-size: 14px;
  font-weight: 700;
  font-family: 'Courier New', monospace;
  min-width: 60px;
  text-align: right;
}

.realtime-value.act-val { color: #448aff; text-shadow: 0 0 6px rgba(68, 138, 255, 0.3); }
.realtime-value.set-val { color: #ffab40; text-shadow: 0 0 6px rgba(255, 171, 64, 0.3); }
.realtime-value.speed-val { color: #69f0ae; text-shadow: 0 0 6px rgba(105, 240, 174, 0.3); }

.realtime-unit {
  font-size: 10px;
  color: rgba(148, 163, 184, 0.4);
  width: 30px;
  text-align: left;
}

.trend-control-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  background: linear-gradient(180deg, rgba(15, 25, 50, 0.95), rgba(10, 20, 40, 0.98));
  border-top: 1px solid rgba(0, 191, 255, 0.15);
}

.param-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.param-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0.6;
}

.param-item:hover {
  opacity: 0.85;
  background: rgba(255, 255, 255, 0.05);
}

.param-item.active {
  opacity: 1;
  background: rgba(255, 255, 255, 0.08);
}

.param-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.param-dot.act {
  background: rgba(68, 138, 255, 0.4);
}

.param-item.active .param-dot.act {
  background: #448aff;
  box-shadow: 0 0 6px rgba(68, 138, 255, 0.6);
}

.param-dot.set {
  background: rgba(255, 171, 64, 0.4);
}

.param-item.active .param-dot.set {
  background: #ffab40;
  box-shadow: 0 0 6px rgba(255, 171, 64, 0.6);
}

.param-dot.speed {
  background: rgba(105, 240, 174, 0.4);
}

.param-item.active .param-dot.speed {
  background: #69f0ae;
  box-shadow: 0 0 6px rgba(105, 240, 174, 0.6);
}

.param-label {
  font-size: 11px;
  color: rgba(148, 163, 184, 0.7);
  font-weight: 500;
  transition: color 0.2s ease;
}

.param-item.active .param-label {
  color: rgba(210, 230, 248, 0.95);
}

.latency-display {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 4px;
  background: rgba(0, 191, 255, 0.05);
  border: 1px solid rgba(0, 191, 255, 0.1);
}

.latency-label {
  font-size: 10px;
  color: rgba(148, 163, 184, 0.6);
  text-transform: uppercase;
}

.latency-value {
  font-size: 13px;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

.latency-good {
  color: #69f0ae;
  text-shadow: 0 0 6px rgba(105, 240, 174, 0.3);
}

.latency-warn {
  color: #ffab40;
  text-shadow: 0 0 6px rgba(255, 171, 64, 0.3);
}

.latency-bad {
  color: #ff5252;
  text-shadow: 0 0 6px rgba(255, 82, 82, 0.4);
}

.time-toggle {
  display: flex;
  gap: 4px;
}

.time-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 6px;
  background: transparent;
  color: rgba(148, 163, 184, 0.7);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.time-btn:hover {
  border-color: rgba(0, 191, 255, 0.35);
  color: rgba(210, 230, 248, 0.9);
  background: rgba(0, 191, 255, 0.05);
}

.time-btn.active {
  border-color: rgba(0, 212, 255, 0.5);
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.12), rgba(0, 140, 200, 0.08));
  color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.15);
}

.btn-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(148, 163, 184, 0.4);
  transition: all 0.25s ease;
}

.time-btn.active .btn-indicator {
  background: #00d4ff;
  box-shadow: 0 0 6px rgba(0, 212, 255, 0.6);
}

.btn-text {
  font-weight: 500;
  letter-spacing: 1px;
}
</style>
