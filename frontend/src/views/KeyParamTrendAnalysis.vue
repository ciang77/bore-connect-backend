<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'

const CYAN = '#00d4ff'
const BLUE = '#448aff'
const GREEN = '#69f0ae'
const ORANGE = '#ffab40'

const trendTimeRange = ref<'24h' | '7d'>('24h')
const servoCurrentTrend = ref<number[]>([])
const vibrationTrend = ref<number[]>([])
const temperatureTrend = ref<number[]>([])
const trendTimeLabels = ref<string[]>([])

const showServoCurrent = ref(true)
const showTemperature = ref(true)
const showVibration = ref(true)

function toggleParameter(param: 'servo' | 'temp' | 'vibration') {
  if (param === 'servo') showServoCurrent.value = !showServoCurrent.value
  if (param === 'temp') showTemperature.value = !showTemperature.value
  if (param === 'vibration') showVibration.value = !showVibration.value
  healthTrendChartInst?.setOption(
    buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value), true
  )
}

const trendChartRef = ref<HTMLDivElement>()
let healthTrendChartInst: echarts.ECharts | null = null
let updateTimer: ReturnType<typeof setInterval> | undefined
let resizeHandler: (() => void) | undefined

function generateTrendData(points: number, hoursBack: number) {
  const now = new Date()
  const labels: string[] = []
  const currentData: number[] = []
  const vibrationData: number[] = []
  const tempData: number[] = []
  let currentVal = 12.3
  let vibrationVal = 3.2
  let tempVal = 52.8
  for (let i = points - 1; i >= 0; i--) {
    const t = new Date(now.getTime() - (i * hoursBack * 3600000) / points)
    if (hoursBack <= 24) {
      labels.push(`${t.getHours().toString().padStart(2, '0')}:${t.getMinutes().toString().padStart(2, '0')}`)
    } else {
      labels.push(`${(t.getMonth() + 1).toString().padStart(2, '0')}/${t.getDate().toString().padStart(2, '0')}`)
    }
    currentVal += (Math.random() - 0.48) * 0.6
    currentVal = Math.max(8, Math.min(18, currentVal))
    if (Math.random() < 0.03) currentVal += 2 + Math.random() * 3
    currentData.push(+currentVal.toFixed(2))

    vibrationVal += (Math.random() - 0.48) * 0.3
    vibrationVal = Math.max(1, Math.min(5.5, vibrationVal))
    if (Math.random() < 0.03) vibrationVal += 0.8 + Math.random() * 1.5
    vibrationData.push(+vibrationVal.toFixed(2))

    tempVal += (Math.random() - 0.48) * 1.2
    tempVal = Math.max(42, Math.min(65, tempVal))
    if (Math.random() < 0.03) tempVal += 3 + Math.random() * 5
    tempData.push(+tempVal.toFixed(2))
  }
  return { labels, currentData, vibrationData, tempData }
}

function switchTimeRange(range: '24h' | '7d') {
  trendTimeRange.value = range
  const points = range === '24h' ? 288 : 168
  const hours = range === '24h' ? 24 : 168
  const result = generateTrendData(points, hours)
  trendTimeLabels.value = result.labels
  servoCurrentTrend.value = result.currentData
  vibrationTrend.value = result.vibrationData
  temperatureTrend.value = result.tempData
  healthTrendChartInst?.setOption(
    buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value), true
  )
}

function buildTrendOption(labels: string[], currentData: number[], vibrationData: number[], tempData: number[]) {
  return {
    backgroundColor: 'transparent',
    grid: { left: 50, right: 16, top: 36, bottom: 28 },
    xAxis: {
      type: 'category',
      data: labels,
      boundaryGap: false,
      axisLine: { lineStyle: { color: 'rgba(0, 191, 255, 0.25)', width: 1 } },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(148, 163, 184, 0.8)',
        fontSize: 10,
        interval: Math.floor(labels.length / 6),
      },
    },
    yAxis: [
      {
        type: 'value',
        name: '伺服电流 (A)',
        nameTextStyle: { color: BLUE, fontSize: 11, fontWeight: 500 },
        axisLabel: { color: 'rgba(148, 163, 184, 0.75)', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(0, 191, 255, 0.08)', type: 'dashed', width: 1 } },
        min: 6,
        max: 20,
        show: showServoCurrent.value,
      },
      {
        type: 'value',
        name: '温度 (°C)',
        nameTextStyle: { color: ORANGE, fontSize: 11, fontWeight: 500 },
        axisLabel: { color: 'rgba(148, 163, 184, 0.75)', fontSize: 10 },
        splitLine: { show: false },
        min: 35,
        max: 70,
        show: showTemperature.value,
      },
      {
        type: 'value',
        name: '振动 (mm/s)',
        offset: 60,
        nameTextStyle: { color: GREEN, fontSize: 11, fontWeight: 500 },
        axisLabel: { color: 'rgba(148, 163, 184, 0.75)', fontSize: 10 },
        splitLine: { show: false },
        min: 0,
        max: 7,
        show: showVibration.value,
      },
    ],
    series: [
      {
        name: '伺服电流',
        type: 'line',
        yAxisIndex: 0,
        data: currentData,
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: BLUE, width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(68, 138, 255, 0.25)' },
            { offset: 1, color: 'rgba(68, 138, 255, 0.02)' },
          ]),
        },
        show: showServoCurrent.value,
      },
      {
        name: '温度',
        type: 'line',
        yAxisIndex: 1,
        data: tempData,
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: ORANGE, width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 171, 64, 0.2)' },
            { offset: 1, color: 'rgba(255, 171, 64, 0.02)' },
          ]),
        },
        show: showTemperature.value,
      },
      {
        name: '振动信号',
        type: 'line',
        yAxisIndex: 2,
        data: vibrationData,
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: GREEN, width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(105, 240, 174, 0.2)' },
            { offset: 1, color: 'rgba(105, 240, 174, 0.02)' },
          ]),
        },
        show: showVibration.value,
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
          const unit = p.seriesName === '温度' ? '°C' : p.seriesName === '伺服电流' ? 'A' : 'mm/s'
          html += `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p.color};margin-right:6px;"></span>${p.seriesName}: <b>${p.value}</b>${unit}<br/>`
        })
        return html
      },
    },
    legend: {
      show: false,
    },
  }
}

function initChart() {
  if (trendChartRef.value) {
    healthTrendChartInst = echarts.init(trendChartRef.value)
    healthTrendChartInst.setOption(
      buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value)
    )
  }
}

function updateData() {
  const now = new Date()
  const timeStr = trendTimeRange.value === '24h'
    ? `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
    : `${(now.getMonth() + 1).toString().padStart(2, '0')}/${now.getDate().toString().padStart(2, '0')}`
  trendTimeLabels.value = [...trendTimeLabels.value.slice(1), timeStr]

  const newCurrent = +(12.3 + (Math.random() - 0.5) * 1.2).toFixed(2)
  const newVibration = +(3.2 + (Math.random() - 0.5) * 0.6).toFixed(2)
  const newTemp = +(52.8 + (Math.random() - 0.5) * 2.4).toFixed(2)
  servoCurrentTrend.value = [...servoCurrentTrend.value.slice(1), newCurrent]
  vibrationTrend.value = [...vibrationTrend.value.slice(1), newVibration]
  temperatureTrend.value = [...temperatureTrend.value.slice(1), newTemp]

  healthTrendChartInst?.setOption(
    buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value)
  )
}

onMounted(async () => {
  const trendResult = generateTrendData(288, 24)
  trendTimeLabels.value = trendResult.labels
  servoCurrentTrend.value = trendResult.currentData
  vibrationTrend.value = trendResult.vibrationData
  temperatureTrend.value = trendResult.tempData

  await nextTick()
  initChart()

  updateTimer = setInterval(updateData, 3000)
  resizeHandler = () => healthTrendChartInst?.resize()
  window.addEventListener('resize', resizeHandler)
})

onUnmounted(() => {
  if (updateTimer) clearInterval(updateTimer)
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  healthTrendChartInst?.dispose()
})
</script>

<template>
  <div class="border-box trend-box">
    <div class="border-top">
      <div class="corner top-left"></div>
      <div class="decoration left">
        <div class="d-block" v-for="i in 3" :key="i"></div>
      </div>
      <div class="title-bar">
        <div class="title-decoration left">
          <div class="deco-wave"></div>
          <div class="deco-dot"></div>
          <div class="deco-line"></div>
          <div class="deco-diamond"></div>
          <div class="deco-line"></div>
          <div class="deco-dot"></div>
          <div class="deco-wave"></div>
        </div>
        <h2 class="title-text">运行趋势</h2>
        <div class="title-decoration right">
          <div class="deco-wave"></div>
          <div class="deco-dot"></div>
          <div class="deco-line"></div>
          <div class="deco-diamond"></div>
          <div class="deco-line"></div>
          <div class="deco-dot"></div>
          <div class="deco-wave"></div>
        </div>
      </div>
      <div class="decoration right">
        <div class="d-block" v-for="i in 3" :key="i"></div>
      </div>
      <div class="corner top-right"></div>
    </div>
    <div class="border-body">
      <div class="side-line left"></div>
      <div class="content-area trend-content-wrapper">
        <div class="trend-chart-ref" ref="trendChartRef"></div>
        <div class="control-bar">
          <div class="param-group">
            <div class="param-item" :class="{ active: showServoCurrent }" @click="toggleParameter('servo')">
              <span class="param-dot servo"></span>
              <span class="param-label">伺服电流</span>
            </div>
            <div class="param-item" :class="{ active: showTemperature }" @click="toggleParameter('temp')">
              <span class="param-dot temp"></span>
              <span class="param-label">温度</span>
            </div>
            <div class="param-item" :class="{ active: showVibration }" @click="toggleParameter('vibration')">
              <span class="param-dot vibration"></span>
              <span class="param-label">振动</span>
            </div>
          </div>
          <div class="time-toggle">
            <button
              class="time-btn"
              :class="{ active: trendTimeRange === '24h' }"
              @click="switchTimeRange('24h')"
            >
              <span class="btn-indicator"></span>
              <span class="btn-text">日</span>
            </button>
            <button
              class="time-btn"
              :class="{ active: trendTimeRange === '7d' }"
              @click="switchTimeRange('7d')"
            >
              <span class="btn-indicator"></span>
              <span class="btn-text">周</span>
            </button>
          </div>
        </div>
      </div>
      <div class="side-line right"></div>
    </div>
    <div class="border-bottom">
      <div class="corner bottom-left"></div>
      <div class="bottom-center"></div>
      <div class="corner bottom-right"></div>
    </div>
  </div>
</template>

<style scoped>
.trend-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.trend-content-wrapper {
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100%;
}

.trend-chart-ref {
  flex: 1;
  min-height: 0;
  width: 100%;
}

.param-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 3px 8px;
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

.param-dot.servo {
  background: rgba(68, 138, 255, 0.4);
}

.param-item.active .param-dot.servo {
  background: #448aff;
  box-shadow: 0 0 6px rgba(68, 138, 255, 0.6);
}

.param-dot.temp {
  background: rgba(255, 171, 64, 0.4);
}

.param-item.active .param-dot.temp {
  background: #ffab40;
  box-shadow: 0 0 6px rgba(255, 171, 64, 0.6);
}

.param-dot.vibration {
  background: rgba(105, 240, 174, 0.4);
}

.param-item.active .param-dot.vibration {
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

.control-bar {
  position: absolute;
  top: 8px;
  left: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(0, 0, 0, 0.3);
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid rgba(0, 191, 255, 0.15);
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

.param-dot.servo {
  background: rgba(68, 138, 255, 0.4);
}

.param-item.active .param-dot.servo {
  background: #448aff;
  box-shadow: 0 0 6px rgba(68, 138, 255, 0.6);
}

.param-dot.temp {
  background: rgba(255, 171, 64, 0.4);
}

.param-item.active .param-dot.temp {
  background: #ffab40;
  box-shadow: 0 0 6px rgba(255, 171, 64, 0.6);
}

.param-dot.vibration {
  background: rgba(105, 240, 174, 0.4);
}

.param-item.active .param-dot.vibration {
  background: #69f0ae;
  box-shadow: 0 0 6px rgba(105, 240, 174, 0.6);
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

.border-box {
  background: linear-gradient(135deg, rgba(6, 16, 40, 0.94), rgba(8, 20, 48, 0.78));
  border-radius: 12px;
  border: 1px solid rgba(0, 180, 255, 0.18);
  overflow: hidden;
  box-shadow:
    inset 0 0 0 1px rgba(120, 223, 255, 0.04),
    inset 0 0 28px rgba(0, 120, 255, 0.04),
    0 4px 16px rgba(0, 0, 0, 0.24);
}

.border-top {
  display: flex;
  align-items: center;
  height: 42px;
  padding: 0 8px;
  background: linear-gradient(180deg, rgba(0, 140, 255, 0.06), transparent);
  border-bottom: 1px solid rgba(0, 160, 255, 0.1);
  position: relative;
}

.corner {
  width: 14px;
  height: 14px;
  position: absolute;
}

.corner.top-left {
  top: 4px;
  left: 4px;
  border-top: 1.5px solid rgba(0, 210, 255, 0.5);
  border-left: 1.5px solid rgba(0, 210, 255, 0.5);
}

.corner.top-right {
  top: 4px;
  right: 4px;
  border-top: 1.5px solid rgba(0, 210, 255, 0.5);
  border-right: 1.5px solid rgba(0, 210, 255, 0.5);
}

.corner.bottom-left {
  bottom: 4px;
  left: 4px;
  border-bottom: 1.5px solid rgba(102, 126, 234, 0.5);
  border-left: 1.5px solid rgba(102, 126, 234, 0.5);
}

.corner.bottom-right {
  bottom: 4px;
  right: 4px;
  border-bottom: 1.5px solid rgba(102, 126, 234, 0.5);
  border-right: 1.5px solid rgba(102, 126, 234, 0.5);
}

.decoration {
  display: flex;
  align-items: center;
  gap: 3px;
}

.decoration.left {
  margin-right: 8px;
}

.decoration.right {
  margin-left: 8px;
}

.d-block {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: rgba(0, 191, 255, 0.4);
}

.title-bar {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.title-decoration {
  display: flex;
  align-items: center;
  gap: 4px;
}

.deco-wave {
  width: 20px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(0, 191, 255, 0.4), transparent);
}

.deco-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(0, 191, 255, 0.6);
}

.deco-line {
  width: 16px;
  height: 1px;
  background: rgba(0, 191, 255, 0.3);
}

.deco-diamond {
  width: 6px;
  height: 6px;
  background: rgba(0, 191, 255, 0.5);
  transform: rotate(45deg);
}

.title-text {
  font-size: 14px;
  font-weight: 600;
  color: rgba(225, 240, 255, 0.92);
  letter-spacing: 2px;
  margin: 0;
  white-space: nowrap;
}

.border-body {
  flex: 1;
  display: flex;
  min-height: 0;
  position: relative;
}

.side-line {
  width: 1px;
  position: absolute;
  top: 0;
  bottom: 0;
}

.side-line.left {
  left: 0;
  background: linear-gradient(180deg, transparent, rgba(0, 191, 255, 0.2) 20%, rgba(0, 191, 255, 0.2) 80%, transparent);
}

.side-line.right {
  right: 0;
  background: linear-gradient(180deg, transparent, rgba(102, 126, 234, 0.2) 20%, rgba(102, 126, 234, 0.2) 80%, transparent);
}

.content-area {
  flex: 1;
  padding: 8px 12px;
  margin: 0 8px;
}

.border-bottom {
  height: 20px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bottom-center {
  width: 60%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 191, 255, 0.2), rgba(102, 126, 234, 0.2), transparent);
}
</style>