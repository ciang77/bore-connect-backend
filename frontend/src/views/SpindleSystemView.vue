<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'

function generateTrendData(baseMin: number, baseMax: number, points: number, spikeProbability = 0.03, spikeMultiplier = 1.8) {
  const data: number[] = []
  for (let i = 0; i < points; i++) {
    let val = baseMin + Math.random() * (baseMax - baseMin)
    if (Math.random() < spikeProbability) val *= spikeMultiplier
    data.push(+val.toFixed(2))
  }
  return data
}

function generateTimeLabels(points: number, hoursBack = 24) {
  const now = new Date()
  const labels: string[] = []
  for (let i = points - 1; i >= 0; i--) {
    const t = new Date(now.getTime() - (i * hoursBack * 3600000) / points)
    labels.push(
      `${t.getHours().toString().padStart(2, '0')}:${t.getMinutes().toString().padStart(2, '0')}`,
    )
  }
  return labels
}

const DATA_POINTS = 288
const WAVEFORM_POINTS = 120

const timeLabels = ref(generateTimeLabels(DATA_POINTS))

const currentVibration = ref(3.2)
const currentTemperature = ref(52.8)
const currentCurrent = ref(45.6)
const currentSpeed = ref(3200)

const vibStatus = ref<'normal' | 'warning' | 'danger'>('normal')
const tempStatus = ref<'normal' | 'warning' | 'danger'>('normal')

const vibrationTrend = ref(generateTrendData(2, 6, DATA_POINTS, 0.04, 2.2))
const temperatureTrend = ref(generateTrendData(42, 68, DATA_POINTS, 0.02, 1.3))
const currentTrend = ref(generateTrendData(22, 72, DATA_POINTS, 0.03, 1.5))
const speedTrend = ref(generateTrendData(1500, 4800, DATA_POINTS, 0.02, 1.4))
const waveformData = ref(generateTrendData(3100, 3300, WAVEFORM_POINTS, 0.1, 1.08))
const waveformTimeLabels = ref(generateTimeLabels(WAVEFORM_POINTS, 2 / 60))

const vibGaugeRef = ref<HTMLDivElement>()
const vibTrendRef = ref<HTMLDivElement>()
const tempGaugeRef = ref<HTMLDivElement>()
const tempTrendRef = ref<HTMLDivElement>()
const currentGaugeRef = ref<HTMLDivElement>()
const currentTrendRef = ref<HTMLDivElement>()
const speedGaugeRef = ref<HTMLDivElement>()
const speedWaveRef = ref<HTMLDivElement>()

let vibGaugeInst: echarts.ECharts | null = null
let vibTrendInst: echarts.ECharts | null = null
let tempGaugeInst: echarts.ECharts | null = null
let tempTrendInst: echarts.ECharts | null = null
let currentGaugeInst: echarts.ECharts | null = null
let currentTrendInst: echarts.ECharts | null = null
let speedGaugeInst: echarts.ECharts | null = null
let speedWaveInst: echarts.ECharts | null = null

let updateTimer: ReturnType<typeof setInterval> | undefined
let resizeHandler: (() => void) | undefined
let allCharts: echarts.ECharts[] = []

const CYAN = '#00e5ff'
const BLUE = '#448aff'
const PURPLE = '#7c4dff'
const GREEN = '#69f0ae'
const ORANGE = '#ffab40'
const RED = '#ff5252'

// Unified trend chart font sizes
const GAUGE_LABEL = 13

function buildVibGaugeOption(val: number, status: string) {
  const statusColor = status === 'danger' ? RED : status === 'warning' ? ORANGE : CYAN
  return {
    series: [{
      type: 'gauge', startAngle: 210, endAngle: -30, center: ['50%', '56%'], radius: '88%',
      min: 0, max: 20, splitNumber: 10,
      axisLine: { show: true, lineStyle: { width: 22, color: [[0.355, GREEN], [0.55, ORANGE], [1, RED]] } },
      pointer: { icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z', length: '68%', width: 10, offsetCenter: [0, '-12%'], itemStyle: { color: statusColor, shadowBlur: 16, shadowColor: statusColor } },
      axisTick: { distance: -22, length: 8, lineStyle: { width: 1.5, color: 'rgba(180,215,240,0.6)' } },
      splitLine: { distance: -26, length: 18, lineStyle: { width: 3, color: 'rgba(180,215,240,0.7)' } },
      axisLabel: { distance: 34, color: 'rgba(200,230,250,0.8)', fontSize: GAUGE_LABEL },
      anchor: { show: true, size: 16, itemStyle: { borderWidth: 2, borderColor: statusColor } },
      title: { offsetCenter: [0, '78%'], color: 'rgba(200,230,250,0.75)', fontSize: 13 },
      detail: { valueAnimation: true, fontSize: 46, fontWeight: 'bold', offsetCenter: [0, '46%'], formatter: '{value}', color: '#fff', textShadowColor: statusColor, textShadowBlur: 14 },
      data: [{ value: val, name: 'mm/s' }],
    }],
  }
}

function buildVibTrendOption(labels: string[], data: number[]) {
  const anomalies: any[] = []
  data.forEach((v, i) => {
    if (v > 10) anomalies.push({ coord: [i, v], value: v.toFixed(1), symbol: 'pin', symbolSize: 36, itemStyle: { color: RED } })
  })
  return {
    grid: { left: 50, right: 20, top: 44, bottom: 30 },
    xAxis: {
      type: 'category', data: labels, boundaryGap: false,
      axisLine: { lineStyle: { color: 'rgba(100,160,230,0.45)', width: 1 } },
      axisTick: { show: false },
      axisLabel: { color: 'rgba(210,230,248,0.72)', fontSize: 14, fontWeight: 500, interval: 23 },
    },
    yAxis: {
      type: 'value', name: 'mm/s', nameLocation: 'middle', nameGap: 42,
      min: 0, max: 20,
      splitLine: { lineStyle: { color: 'rgba(80,140,210,0.18)', type: 'dashed', width: 1 } },
      axisLabel: { color: 'rgba(210,230,248,0.75)', fontSize: 14, fontWeight: 500 },
      nameTextStyle: { color: 'rgba(210,235,250,0.85)', fontSize: 15, fontWeight: 600 },
    },
    series: [{
      type: 'line', data, smooth: true, symbol: 'none',
      lineStyle: { color: CYAN, width: 2, shadowBlur: 10, shadowColor: CYAN },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(0,229,255,0.2)' }, { offset: 1, color: 'rgba(0,229,255,0.02)' },
      ]) },
      markLine: {
        silent: true, symbol: 'none',
        lineStyle: { type: 'dashed', width: 1.5 },
        label: { color: 'rgba(230,240,250,0.7)', fontSize: 14, fontWeight: 500 },
        data: [
          { yAxis: 7.1, lineStyle: { color: ORANGE }, label: { formatter: '预警 7.1 mm/s' } },
          { yAxis: 11, lineStyle: { color: RED }, label: { formatter: '报警 11 mm/s' } },
        ],
      },
      markPoint: { data: anomalies, animation: true },
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(6,14,38,0.94)', borderColor: 'rgba(0,200,255,0.4)',
      textStyle: { color: '#f0f4fa', fontSize: 15 },
      formatter: (params: any) => `<b>${params[0].axisValue}</b><br/>振动: <b style="color:#00e5ff;font-size:16px">${params[0].value} mm/s</b>`,
    },
  }
}

function buildTempGaugeOption(val: number) {
  const color = val > 75 ? RED : val > 65 ? ORANGE : CYAN
  return {
    series: [{
      type: 'gauge', startAngle: 200, endAngle: -20, center: ['50%', '58%'], radius: '90%',
      min: 30, max: 90, splitNumber: 6,
      axisLine: { show: true, lineStyle: { width: 16, color: [[(65 - 30) / 60, CYAN], [(75 - 30) / 60, ORANGE], [1, RED]] } },
      pointer: { length: '62%', width: 8, itemStyle: { color, shadowBlur: 12, shadowColor: color } },
      axisTick: { distance: -16, length: 6, lineStyle: { width: 1, color: 'rgba(180,215,240,0.5)' } },
      splitLine: { distance: -20, length: 14, lineStyle: { width: 2.5, color: 'rgba(180,215,240,0.65)' } },
      axisLabel: { distance: 28, color: 'rgba(200,230,250,0.8)', fontSize: GAUGE_LABEL, formatter: '{value}°C' },
      anchor: { show: true, size: 12, itemStyle: { borderWidth: 2, borderColor: color } },
      title: { offsetCenter: [0, '82%'], color: 'rgba(200,230,250,0.75)', fontSize: 13 },
      detail: { valueAnimation: true, fontSize: 40, fontWeight: 'bold', offsetCenter: [0, '48%'], formatter: '{value}°C', color: '#fff', textShadowColor: color, textShadowBlur: 12 },
      data: [{ value: val, name: '温度' }],
    }],
  }
}

function buildTempTrendOption(labels: string[], data: number[]) {
  return {
    grid: { left: 50, right: 20, top: 44, bottom: 30 },
    xAxis: {
      type: 'category', data: labels, boundaryGap: false,
      axisLine: { lineStyle: { color: 'rgba(100,160,230,0.45)', width: 1 } },
      axisTick: { show: false },
      axisLabel: { color: 'rgba(210,230,248,0.72)', fontSize: 14, fontWeight: 500, interval: 23 },
    },
    yAxis: {
      type: 'value', name: '°C', nameLocation: 'middle', nameGap: 42,
      min: 30, max: 90,
      splitLine: { lineStyle: { color: 'rgba(80,140,210,0.18)', type: 'dashed', width: 1 } },
      axisLabel: { color: 'rgba(210,230,248,0.75)', fontSize: 14, fontWeight: 500 },
      nameTextStyle: { color: 'rgba(210,235,250,0.85)', fontSize: 15, fontWeight: 600 },
    },
    series: [{
      type: 'line', data, smooth: true, symbol: 'none',
      lineStyle: { color: ORANGE, width: 2, shadowBlur: 10, shadowColor: ORANGE },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(255,171,64,0.18)' }, { offset: 1, color: 'rgba(255,171,64,0.02)' },
      ]) },
      markLine: {
        silent: true, symbol: 'none',
        lineStyle: { type: 'dashed', width: 1.5 },
        label: { color: 'rgba(230,240,250,0.7)', fontSize: 14, fontWeight: 500 },
        data: [
          { yAxis: 65, lineStyle: { color: ORANGE }, label: { formatter: '预警 65°C' } },
          { yAxis: 75, lineStyle: { color: RED }, label: { formatter: '报警 75°C' } },
        ],
      },
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(6,14,38,0.94)', borderColor: 'rgba(255,171,64,0.4)',
      textStyle: { color: '#f0f4fa', fontSize: 15 },
      formatter: (params: any) => `<b>${params[0].axisValue}</b><br/>温度: <b style="color:#ffab40;font-size:16px">${params[0].value}°C</b>`,
    },
  }
}

function buildCurrentGaugeOption(val: number) {
  const color = val > 85 ? RED : val > 70 ? ORANGE : CYAN
  return {
    series: [{
      type: 'gauge', startAngle: 180, endAngle: 0, center: ['50%', '72%'], radius: '92%',
      min: 0, max: 100, splitNumber: 10,
      axisLine: { show: true, lineStyle: { width: 20, color: [[0.7, CYAN], [0.85, ORANGE], [1, RED]] } },
      pointer: { length: '64%', width: 8, itemStyle: { color, shadowBlur: 12, shadowColor: color } },
      axisTick: { distance: -20, length: 6, lineStyle: { width: 1.5, color: 'rgba(180,215,240,0.5)' } },
      splitLine: { distance: -24, length: 14, lineStyle: { width: 3, color: 'rgba(180,215,240,0.6)' } },
      axisLabel: { distance: 24, color: 'rgba(200,230,250,0.8)', fontSize: GAUGE_LABEL, formatter: '{value}' },
      anchor: { show: true, size: 14, itemStyle: { borderWidth: 2, borderColor: color } },
      title: { offsetCenter: [0, '30%'], color: 'rgba(200,230,250,0.75)', fontSize: 13 },
      detail: { valueAnimation: true, fontSize: 40, fontWeight: 'bold', offsetCenter: [0, '48%'], formatter: '{value}A', color: '#fff', textShadowColor: color, textShadowBlur: 12 },
      data: [{ value: val, name: '电流' }],
    }],
  }
}

function buildCurrentTrendOption(labels: string[], data: number[]) {
  return {
    grid: { left: 50, right: 20, top: 44, bottom: 30 },
    xAxis: {
      type: 'category', data: labels, boundaryGap: false,
      axisLine: { lineStyle: { color: 'rgba(100,160,230,0.45)', width: 1 } },
      axisTick: { show: false },
      axisLabel: { color: 'rgba(210,230,248,0.72)', fontSize: 14, fontWeight: 500, interval: 23 },
    },
    yAxis: {
      type: 'value', name: 'A', nameLocation: 'middle', nameGap: 42,
      min: 0, max: 100,
      splitLine: { lineStyle: { color: 'rgba(80,140,210,0.18)', type: 'dashed', width: 1 } },
      axisLabel: { color: 'rgba(210,230,248,0.75)', fontSize: 14, fontWeight: 500 },
      nameTextStyle: { color: 'rgba(210,235,250,0.85)', fontSize: 15, fontWeight: 600 },
    },
    series: [{
      type: 'line', data, smooth: true, symbol: 'none',
      lineStyle: { color: PURPLE, width: 2, shadowBlur: 10, shadowColor: PURPLE },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(124,77,255,0.22)' }, { offset: 1, color: 'rgba(124,77,255,0.02)' },
      ]) },
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(6,14,38,0.94)', borderColor: 'rgba(124,77,255,0.4)',
      textStyle: { color: '#f0f4fa', fontSize: 15 },
      formatter: (params: any) => `<b>${params[0].axisValue}</b><br/>电流: <b style="color:#7c4dff;font-size:16px">${params[0].value} A</b>`,
    },
  }
}

function buildSpeedGaugeOption(val: number) {
  const color = val > 5000 ? RED : val > 4200 ? ORANGE : CYAN
  return {
    series: [{
      type: 'gauge', startAngle: 220, endAngle: -40, center: ['50%', '56%'], radius: '86%',
      min: 0, max: 6000, splitNumber: 12,
      axisLine: { show: true, lineStyle: { width: 20, color: [[0.5, CYAN], [0.7, BLUE], [0.85, ORANGE], [1, RED]] } },
      pointer: { length: '64%', width: 8, itemStyle: { color, shadowBlur: 14, shadowColor: color } },
      axisTick: { distance: -20, length: 6, lineStyle: { width: 1.5, color: 'rgba(180,215,240,0.5)' } },
      splitLine: { distance: -24, length: 16, lineStyle: { width: 3, color: 'rgba(180,215,240,0.6)' } },
      axisLabel: { distance: 30, color: 'rgba(200,230,250,0.8)', fontSize: GAUGE_LABEL, formatter: '{value}' },
      anchor: { show: true, size: 14, itemStyle: { borderWidth: 2, borderColor: color } },
      title: { offsetCenter: [0, '76%'], color: 'rgba(200,230,250,0.75)', fontSize: 13 },
      detail: { valueAnimation: true, fontSize: 44, fontWeight: 'bold', offsetCenter: [0, '46%'], formatter: '{value}', color: '#fff', textShadowColor: color, textShadowBlur: 14 },
      data: [{ value: val, name: 'RPM' }],
    }],
  }
}

function buildSpeedWaveOption(labels: string[], data: number[]) {
  return {
    grid: { left: 50, right: 20, top: 44, bottom: 30 },
    xAxis: {
      type: 'category', data: labels, boundaryGap: false,
      axisLine: { lineStyle: { color: 'rgba(100,160,230,0.45)', width: 1 } },
      axisTick: { show: false },
      axisLabel: { color: 'rgba(210,230,248,0.72)', fontSize: 14, fontWeight: 500, interval: 19 },
    },
    yAxis: {
      type: 'value', name: 'RPM', nameLocation: 'middle', nameGap: 46,
      min: 2900, max: 3500,
      splitLine: { lineStyle: { color: 'rgba(80,140,210,0.18)', type: 'dashed', width: 1 } },
      axisLabel: { color: 'rgba(210,230,248,0.75)', fontSize: 14, fontWeight: 500 },
      nameTextStyle: { color: 'rgba(210,235,250,0.85)', fontSize: 15, fontWeight: 600 },
    },
    series: [{
      type: 'line', data, smooth: true, symbol: 'none',
      lineStyle: { color: CYAN, width: 1.8, shadowBlur: 10, shadowColor: CYAN },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(0,229,255,0.22)' }, { offset: 1, color: 'rgba(0,229,255,0.02)' },
      ]) },
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(6,14,38,0.94)', borderColor: 'rgba(0,200,255,0.4)',
      textStyle: { color: '#f0f4fa', fontSize: 15 },
      formatter: (params: any) => `<b>${params[0].axisValue}</b><br/>转速: <b style="color:#00e5ff;font-size:16px">${params[0].value} RPM</b>`,
    },
  }
}

function initCharts() {
  const set = (ref: HTMLDivElement | undefined, opt: any) => {
    if (!ref) return null
    const inst = echarts.init(ref)
    inst.setOption(opt)
    return inst
  }

  vibGaugeInst = set(vibGaugeRef.value, buildVibGaugeOption(currentVibration.value, vibStatus.value))
  vibTrendInst = set(vibTrendRef.value, buildVibTrendOption(timeLabels.value, vibrationTrend.value))
  tempGaugeInst = set(tempGaugeRef.value, buildTempGaugeOption(currentTemperature.value))
  tempTrendInst = set(tempTrendRef.value, buildTempTrendOption(timeLabels.value, temperatureTrend.value))
  currentGaugeInst = set(currentGaugeRef.value, buildCurrentGaugeOption(currentCurrent.value))
  currentTrendInst = set(currentTrendRef.value, buildCurrentTrendOption(timeLabels.value, currentTrend.value))
  speedGaugeInst = set(speedGaugeRef.value, buildSpeedGaugeOption(currentSpeed.value))
  speedWaveInst = set(speedWaveRef.value, buildSpeedWaveOption(waveformTimeLabels.value, waveformData.value))

  allCharts = [vibGaugeInst, vibTrendInst, tempGaugeInst, tempTrendInst, currentGaugeInst, currentTrendInst, speedGaugeInst, speedWaveInst].filter(Boolean) as echarts.ECharts[]
}

function updateData() {
  const vibChange = (Math.random() - 0.5) * 1.2
  currentVibration.value = +Math.max(0.5, Math.min(18, currentVibration.value + vibChange)).toFixed(2)
  if (currentVibration.value > 11) vibStatus.value = 'danger'
  else if (currentVibration.value > 7.1) vibStatus.value = 'warning'
  else vibStatus.value = 'normal'

  const tempChange = (Math.random() - 0.5) * 1.5
  currentTemperature.value = +Math.max(32, Math.min(88, currentTemperature.value + tempChange)).toFixed(1)
  if (currentTemperature.value > 75) tempStatus.value = 'danger'
  else if (currentTemperature.value > 65) tempStatus.value = 'warning'
  else tempStatus.value = 'normal'

  currentCurrent.value = +Math.max(5, Math.min(98, currentCurrent.value + (Math.random() - 0.5) * 4)).toFixed(1)
  currentSpeed.value = +Math.max(200, Math.min(5900, currentSpeed.value + (Math.random() - 0.5) * 120)).toFixed(0)

  vibrationTrend.value = [...vibrationTrend.value.slice(1), currentVibration.value]
  temperatureTrend.value = [...temperatureTrend.value.slice(1), currentTemperature.value]
  currentTrend.value = [...currentTrend.value.slice(1), currentCurrent.value]
  speedTrend.value = [...speedTrend.value.slice(1), currentSpeed.value]
  waveformData.value = [...waveformData.value.slice(1), currentSpeed.value + (Math.random() - 0.5) * 60]
  const now = new Date()
  waveformTimeLabels.value = [...waveformTimeLabels.value.slice(1), `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`]
  timeLabels.value = [...timeLabels.value.slice(1), new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })]

  vibGaugeInst?.setOption(buildVibGaugeOption(currentVibration.value, vibStatus.value))
  vibTrendInst?.setOption(buildVibTrendOption(timeLabels.value, vibrationTrend.value))
  tempGaugeInst?.setOption(buildTempGaugeOption(currentTemperature.value))
  tempTrendInst?.setOption(buildTempTrendOption(timeLabels.value, temperatureTrend.value))
  currentGaugeInst?.setOption(buildCurrentGaugeOption(currentCurrent.value))
  currentTrendInst?.setOption(buildCurrentTrendOption(timeLabels.value, currentTrend.value))
  speedGaugeInst?.setOption(buildSpeedGaugeOption(currentSpeed.value))
  speedWaveInst?.setOption(buildSpeedWaveOption(waveformTimeLabels.value, waveformData.value))
}

onMounted(async () => {
  await nextTick()
  initCharts()
  updateTimer = setInterval(updateData, 2500)
  resizeHandler = () => allCharts.forEach(c => c.resize())
  window.addEventListener('resize', resizeHandler)
})

onUnmounted(() => {
  if (updateTimer) clearInterval(updateTimer)
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  allCharts.forEach(c => c.dispose())
})
</script>

<template>
  <div class="spindle-view">
    <div class="monitoring-grid">
      <!-- LEFT PANEL -->
      <div class="left-panel">
        <div class="card vib-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-icon vib-icon"></span>
              <span class="header-title">振动监测</span>
              <span class="header-badge" :class="'badge-' + vibStatus">
                {{ vibStatus === 'danger' ? '危险' : vibStatus === 'warning' ? '预警' : '正常' }}
              </span>
            </div>
            <div class="header-right">
              <span class="header-unit">VIBRATION</span>
            </div>
          </div>
          <div class="card-corners">
            <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
          </div>
          <div class="card-body">
            <div class="gauge-wrap" ref="vibGaugeRef"></div>
            <div class="trend-wrap" ref="vibTrendRef"></div>
          </div>
          <div class="card-scan-line"></div>
        </div>

        <div class="card temp-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-icon temp-icon"></span>
              <span class="header-title">温度监测</span>
              <span class="header-badge" :class="'badge-' + tempStatus">
                {{ tempStatus === 'danger' ? '报警' : tempStatus === 'warning' ? '预警' : '正常' }}
              </span>
            </div>
            <div class="header-right">
              <span class="header-unit">TEMPERATURE</span>
            </div>
          </div>
          <div class="card-corners">
            <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
          </div>
          <div class="card-body">
            <div class="gauge-wrap" ref="tempGaugeRef"></div>
            <div class="trend-wrap" ref="tempTrendRef"></div>
          </div>
          <div class="card-scan-line"></div>
        </div>
      </div>

      <!-- CENTER: Spindle Model -->
      <div class="center-panel">
        <div class="card spindle-model-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-icon spindle-icon"></span>
              <span class="header-title">主轴模型</span>
            </div>
            <div class="header-right">
              <span class="header-unit">SPINDLE MODEL</span>
            </div>
          </div>
          <div class="card-corners">
            <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
          </div>
          <div class="spindle-visual">
            <div class="spindle-outer">
              <div class="spindle-housing">
                <div class="spindle-rotor" :style="{ animationDuration: (6000 - currentSpeed) / 30 + 's' }">
                  <div class="rotor-core"></div>
                  <div class="rotor-ring r1"></div>
                  <div class="rotor-ring r2"></div>
                  <div class="rotor-ring r3"></div>
                </div>
                <div class="bearing b-left"><div class="bearing-dot"></div></div>
                <div class="bearing b-right"><div class="bearing-dot"></div></div>
              </div>
              <div class="particle-stream ps-left"></div>
              <div class="particle-stream ps-right"></div>
            </div>
            <div class="spindle-overlay">
              <div class="so-item">
                <span class="so-label">实时转速</span>
                <span class="so-value">{{ currentSpeed }} <small>RPM</small></span>
              </div>
              <div class="so-item">
                <span class="so-label">运行状态</span>
                <span class="so-value so-status" :class="vibStatus === 'danger' ? 'text-danger' : vibStatus === 'warning' ? 'text-warning' : 'text-normal'">
                  {{ vibStatus === 'danger' ? '异常' : vibStatus === 'warning' ? '注意' : '正常' }}
                </span>
              </div>
            </div>
          </div>
          <div class="card-scan-line"></div>
        </div>
      </div>

      <!-- RIGHT PANEL -->
      <div class="right-panel">
        <div class="card current-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-icon current-icon"></span>
              <span class="header-title">电流监测</span>
            </div>
            <div class="header-right">
              <span class="header-unit">CURRENT</span>
            </div>
          </div>
          <div class="card-corners">
            <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
          </div>
          <div class="card-body">
            <div class="gauge-wrap" ref="currentGaugeRef"></div>
            <div class="trend-wrap" ref="currentTrendRef"></div>
          </div>
          <div class="card-scan-line"></div>
        </div>

        <div class="card speed-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-icon speed-icon"></span>
              <span class="header-title">转速监测</span>
            </div>
            <div class="header-right">
              <span class="header-unit">SPEED</span>
            </div>
          </div>
          <div class="card-corners">
            <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
          </div>
          <div class="card-body">
            <div class="gauge-wrap" ref="speedGaugeRef"></div>
            <div class="trend-wrap" ref="speedWaveRef"></div>
          </div>
          <div class="card-scan-line"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Root: one page, no scroll ─────────────────────────────────── */
.spindle-view {
  height: calc(100vh - 260px);
  overflow: hidden;
  padding: 8px 18px 0;
  position: relative;
  z-index: 1;
}

/* ── Monitoring Grid ───────────────────────────────────────────── */
.monitoring-grid {
  display: grid;
  grid-template-columns: 1fr 0.7fr 1fr;
  gap: 14px;
  height: 100%;
}

.left-panel,
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
}

.left-panel > .card,
.right-panel > .card {
  flex: 1;
  min-height: 0;
}

/* ── Card base ─────────────────────────────────────────────────── */
.card {
  position: relative;
  background: linear-gradient(135deg, rgba(6, 16, 40, 0.94), rgba(8, 20, 48, 0.78));
  border: 1px solid rgba(0, 180, 255, 0.2);
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow:
    inset 0 0 0 1px rgba(120, 223, 255, 0.04),
    inset 0 0 28px rgba(0, 120, 255, 0.04),
    0 8px 28px rgba(0, 0, 0, 0.28),
    0 0 22px rgba(0, 100, 255, 0.06);
  transition: box-shadow 0.4s ease, border-color 0.4s ease;
}

.card:hover {
  border-color: rgba(0, 210, 255, 0.36);
  box-shadow:
    inset 0 0 0 1px rgba(120, 223, 255, 0.06),
    inset 0 0 34px rgba(0, 140, 255, 0.06),
    0 10px 32px rgba(0, 0, 0, 0.34),
    0 0 30px rgba(0, 140, 255, 0.1);
}

/* ── Card corners ──────────────────────────────────────────────── */
.card-corners {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 3;
}

.c-tl, .c-tr, .c-bl, .c-br {
  position: absolute;
  width: 16px;
  height: 16px;
  opacity: 0.8;
}

.c-tl { top: 7px; left: 7px; border-top: 1.5px solid rgba(0, 210, 255, 0.5); border-left: 1.5px solid rgba(0, 210, 255, 0.5); }
.c-tr { top: 7px; right: 7px; border-top: 1.5px solid rgba(0, 210, 255, 0.5); border-right: 1.5px solid rgba(0, 210, 255, 0.5); }
.c-bl { bottom: 7px; left: 7px; border-bottom: 1.5px solid rgba(102, 126, 234, 0.5); border-left: 1.5px solid rgba(102, 126, 234, 0.5); }
.c-br { bottom: 7px; right: 7px; border-bottom: 1.5px solid rgba(102, 126, 234, 0.5); border-right: 1.5px solid rgba(102, 126, 234, 0.5); }

/* ── Card header ───────────────────────────────────────────────── */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border-bottom: 1px solid rgba(0, 160, 255, 0.12);
  background: linear-gradient(180deg, rgba(0, 140, 255, 0.06), transparent);
  position: relative;
  z-index: 2;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.header-icon::after {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 8px;
  border: 1px solid rgba(0, 210, 255, 0.3);
  animation: icon-pulse 2.5s ease-in-out infinite;
}

.vib-icon { background: radial-gradient(circle, rgba(0,229,255,0.25), rgba(0,100,200,0.15)); }
.temp-icon { background: radial-gradient(circle, rgba(255,171,64,0.25), rgba(200,80,20,0.15)); }
.current-icon { background: radial-gradient(circle, rgba(124,77,255,0.25), rgba(80,20,180,0.15)); }
.speed-icon { background: radial-gradient(circle, rgba(68,138,255,0.25), rgba(20,60,180,0.15)); }
.spindle-icon { background: radial-gradient(circle, rgba(0,229,255,0.25), rgba(0,140,200,0.15)); }

.header-title {
  font-size: 15px;
  font-weight: 700;
  color: rgba(225, 240, 255, 0.92);
  letter-spacing: 1.5px;
}

.header-badge {
  font-size: 11px;
  padding: 2px 10px;
  border-radius: 10px;
  letter-spacing: 1px;
  font-weight: 600;
}

.badge-normal { background: rgba(105,240,174,0.14); color: #69f0ae; border: 1px solid rgba(105,240,174,0.25); }
.badge-warning { background: rgba(255,171,64,0.14); color: #ffab40; border: 1px solid rgba(255,171,64,0.25); }
.badge-danger { background: rgba(255,82,82,0.14); color: #ff5252; border: 1px solid rgba(255,82,82,0.25); animation: danger-blink 1s ease-in-out infinite; }

.header-unit {
  font-size: 11px;
  letter-spacing: 2px;
  color: rgba(150, 200, 230, 0.55);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ── Card body ─────────────────────────────────────────────────── */
.card-body {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 4px;
  position: relative;
  z-index: 2;
  flex: 1;
  min-height: 0;
}

.gauge-wrap,
.trend-wrap {
  width: 100%;
  height: 100%;
  min-height: 0;
}

/* ── Card scan line ────────────────────────────────────────────── */
.card-scan-line {
  position: absolute;
  top: 0;
  left: -30%;
  width: 30%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(100, 200, 255, 0.06), transparent);
  transform: skewX(-20deg);
  animation: card-scan 8s linear infinite;
  pointer-events: none;
  z-index: 1;
}

/* ── Spindle Model ─────────────────────────────────────────────── */
.spindle-model-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.spindle-visual {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 14px 16px;
  z-index: 2;
  min-height: 0;
}

.spindle-outer {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.spindle-housing {
  position: relative;
  width: 78%;
  height: 80px;
  background: linear-gradient(180deg, rgba(40,60,100,0.5), rgba(20,30,60,0.7), rgba(40,60,100,0.5));
  border: 1.5px solid rgba(0, 180, 255, 0.35);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    inset 0 0 30px rgba(0, 140, 255, 0.08),
    0 0 20px rgba(0, 140, 255, 0.1);
  overflow: hidden;
}

.spindle-housing::before {
  content: '';
  position: absolute;
  inset: 3px;
  border-radius: 10px;
  border: 1px solid rgba(0, 180, 255, 0.1);
  pointer-events: none;
}

.spindle-rotor {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(70, 130, 210, 0.7), rgba(30, 60, 130, 0.8));
  border: 2px solid rgba(0, 210, 255, 0.5);
  position: relative;
  animation: rotor-spin 2s linear infinite;
  box-shadow:
    inset 0 0 16px rgba(0, 200, 255, 0.2),
    0 0 20px rgba(0, 180, 255, 0.25);
}

.rotor-core {
  position: absolute;
  top: 50%; left: 50%;
  width: 14px; height: 14px;
  border-radius: 50%;
  background: radial-gradient(circle, #fff, rgba(0, 210, 255, 0.8));
  transform: translate(-50%, -50%);
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.6);
}

.rotor-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(0, 200, 255, 0.3);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}

.r1 { width: 30px; height: 30px; }
.r2 { width: 42px; height: 42px; border-style: dashed; }
.r3 { width: 52px; height: 52px; border-style: dotted; }

.bearing {
  position: absolute;
  width: 24px;
  height: 40px;
  background: linear-gradient(180deg, rgba(60,80,120,0.6), rgba(30,50,90,0.8));
  border: 1px solid rgba(0, 180, 255, 0.3);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.b-left { left: 18px; top: 50%; transform: translateY(-50%); }
.b-right { right: 18px; top: 50%; transform: translateY(-50%); }

.bearing-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: rgba(0, 229, 255, 0.7);
  box-shadow: 0 0 8px rgba(0, 229, 255, 0.5);
  animation: bearing-glow 1.8s ease-in-out infinite;
}

.particle-stream {
  position: absolute;
  top: 50%;
  width: 60px;
  height: 2px;
  transform: translateY(-50%);
  pointer-events: none;
}

.ps-left {
  left: 8px;
  background: linear-gradient(90deg, transparent, rgba(0, 229, 255, 0.5));
  animation: particle-flow-left 2s ease-in-out infinite;
}

.ps-right {
  right: 8px;
  background: linear-gradient(270deg, transparent, rgba(0, 229, 255, 0.5));
  animation: particle-flow-right 2s ease-in-out infinite;
}

.spindle-overlay {
  display: flex;
  gap: 32px;
  margin-top: 12px;
  flex-shrink: 0;
}

.so-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.so-label {
  font-size: 11px;
  letter-spacing: 1.5px;
  color: rgba(160, 210, 240, 0.6);
  text-transform: uppercase;
}

.so-value {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 2px;
  text-shadow: 0 0 12px rgba(0, 229, 255, 0.3);
}

.so-value small {
  font-size: 13px;
  font-weight: 400;
  color: rgba(200, 220, 240, 0.6);
  letter-spacing: 1px;
}

.so-status.text-normal { color: #69f0ae; text-shadow: 0 0 10px rgba(105,240,174,0.3); }
.so-status.text-warning { color: #ffab40; text-shadow: 0 0 10px rgba(255,171,64,0.3); }
.so-status.text-danger { color: #ff5252; text-shadow: 0 0 10px rgba(255,82,82,0.3); animation: danger-blink 1s ease-in-out infinite; }

/* ── Animations ────────────────────────────────────────────────── */
@keyframes icon-pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.08); }
}

@keyframes card-scan {
  0% { transform: translateX(-160%) skewX(-20deg); }
  100% { transform: translateX(520%) skewX(-20deg); }
}

@keyframes rotor-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes bearing-glow {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

@keyframes particle-flow-left {
  0% { opacity: 0; transform: translateY(-50%) translateX(0); }
  50% { opacity: 0.8; }
  100% { opacity: 0; transform: translateY(-50%) translateX(-40px); }
}

@keyframes particle-flow-right {
  0% { opacity: 0; transform: translateY(-50%) translateX(0); }
  50% { opacity: 0.8; }
  100% { opacity: 0; transform: translateY(-50%) translateX(40px); }
}

@keyframes danger-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ── Responsive ────────────────────────────────────────────────── */
@media (max-width: 1400px) {
  .monitoring-grid {
    grid-template-columns: 1fr 1fr;
  }
  .center-panel {
    grid-column: 1 / -1;
    order: 3;
  }
}

@media (max-width: 1100px) {
  .monitoring-grid {
    grid-template-columns: 1fr;
  }
  .spindle-view {
    height: auto;
    overflow: visible;
    padding: 8px 10px 24px;
  }
  .left-panel,
  .right-panel {
    height: auto;
  }
  .left-panel > .card,
  .right-panel > .card {
    flex: none;
    min-height: 420px;
  }
}
</style>
