<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()

// ── Color constants ────────────────────────────────────────────────
const CYAN = '#00e5ff'
const BLUE = '#448aff'
const PURPLE = '#7c4dff'
const GREEN = '#69f0ae'
const ORANGE = '#ffab40'
const RED = '#ff5252'

// ── Module 1: Device Status ────────────────────────────────────────
const deviceName = ref('龙门镗铣床')
const deviceId = ref('CNC-HUB-01')
const deviceStatus = ref<'running' | 'standby' | 'stop' | 'fault'>('running')
const powerOnDuration = ref('1268h 32m')
const todayRuntime = ref('6h 45m')
const machiningStatus = ref('加工中')
const workpiece = ref('机体端盖-0627B')
const isOnline = ref(true)

const statusText = computed(() => {
  const map = { running: '运行中', standby: '待机', stop: '停机', fault: '故障' }
  return map[deviceStatus.value]
})
const statusClass = computed(() => `status-${deviceStatus.value}`)

function cycleDeviceStatus() {
  const states: ('running' | 'standby' | 'stop' | 'fault')[] = ['running', 'running', 'running', 'running', 'running', 'standby', 'running', 'running', 'running', 'fault']
  deviceStatus.value = states[Math.floor(Math.random() * states.length)]
  if (deviceStatus.value === 'fault') {
    setTimeout(() => { deviceStatus.value = 'running' }, 4000 + Math.random() * 4000)
  }
}

// ── Module 2: Motor Health ─────────────────────────────────────────
const healthScore = ref(87.5)

const healthLevel = computed(() => {
  if (healthScore.value >= 90) return { text: '健康', cls: 'badge-normal' }
  if (healthScore.value >= 70) return { text: '轻度异常', cls: 'badge-warning' }
  if (healthScore.value >= 50) return { text: '需要维护', cls: 'badge-warning' }
  return { text: '故障风险', cls: 'badge-danger' }
})

// ── Module 3: Alarms & Events ──────────────────────────────────────
interface AlarmEvent {
  time: string
  level: 'critical' | 'warning' | 'info'
  type: string
  system: string
  description: string
  isAlarm: boolean
}

const alarmEvents = ref<AlarmEvent[]>([])
const alarmTypes = ['振动异常', '温度异常', '电流异常', '润滑异常', '液压异常', '通讯异常', '其他故障']
const alarmSystems = ['主轴系统', '进给系统', '润滑系统', '液压系统', '控制系统']

function generateAlarmEvents() {
  const events: AlarmEvent[] = []
  const now = new Date()
  for (let i = 0; i < 10; i++) {
    const isAlarm = Math.random() > 0.35
    const level = isAlarm ? (Math.random() > 0.5 ? 'critical' : 'warning') : 'info'
    const t = new Date(now.getTime() - i * 1000 * 60 * (5 + Math.floor(Math.random() * 40)))
    events.push({
      time: `${t.getHours().toString().padStart(2, '0')}:${t.getMinutes().toString().padStart(2, '0')}:${t.getSeconds().toString().padStart(2, '0')}`,
      level,
      type: isAlarm ? alarmTypes[Math.floor(Math.random() * alarmTypes.length)] : ['设备启动', '设备停机', '参数超限', '故障解除', '维护记录'][Math.floor(Math.random() * 5)],
      system: alarmSystems[Math.floor(Math.random() * alarmSystems.length)],
      description: isAlarm
        ? ['数值超出阈值', '传感器信号异常', '持续上升趋势', '瞬时峰值'][Math.floor(Math.random() * 4)]
        : ['操作员手动', '自动触发', '计划维护', '系统复位'][Math.floor(Math.random() * 4)],
      isAlarm,
    })
  }
  return events
}

// ── Module 4: Subsystem Status ─────────────────────────────────────
interface SubsystemInfo {
  name: string
  nameEn: string
  routeName: string
  icon: string
  status: 'normal' | 'warning' | 'fault'
  healthScore: number
  metrics: { label: string; value: string; unit: string }[]
}

const subsystems = ref<SubsystemInfo[]>([
  {
    name: '主轴系统', nameEn: 'SPINDLE', routeName: 'dashboard',
    icon: 'spindle', status: 'normal', healthScore: 92,
    metrics: [
      { label: '振动监测', value: '3.20', unit: 'mm/s' },
      { label: '温度监测', value: '52.80', unit: '°C' },
      { label: '电流监测', value: '45.60', unit: 'A' },
      { label: '转速监测', value: '3200', unit: 'RPM' },
    ],
  },
  {
    name: '进给系统', nameEn: 'FEED', routeName: 'dashboard',
    icon: 'feed', status: 'normal', healthScore: 88,
    metrics: [
      { label: '伺服电流', value: '12.30', unit: 'A' },
      { label: '跟随误差', value: '0.02', unit: 'mm' },
      { label: '位置误差', value: '0.01', unit: 'mm' },
      { label: '振动状态', value: '1.80', unit: 'mm/s' },
    ],
  },
  {
    name: '液压系统', nameEn: 'HYDRAULIC', routeName: 'smart-analysis',
    icon: 'hydraulic', status: 'normal', healthScore: 90,
    metrics: [
      { label: '系统压力', value: '16.50', unit: 'MPa' },
      { label: '液压流量', value: '24.60', unit: 'L/min' },
      { label: '响应速度', value: '0.12', unit: 's' },
    ],
  },
  {
    name: '润滑系统', nameEn: 'LUBRICATION', routeName: 'system-status',
    icon: 'lube', status: 'warning', healthScore: 72,
    metrics: [
      { label: '润滑压力', value: '0.45', unit: 'MPa' },
      { label: '供油流量', value: '2.80', unit: 'L/min' },
      { label: '油液品质', value: '82', unit: '%' },
    ],
  },
])

function navigateTo(routeName: string) {
  if (routeName !== 'dashboard') {
    router.push({ name: routeName })
  }
}

// ── Module 5: Alarm Distribution (Donut) ───────────────────────────
const alarmDistribution = ref([
  { name: '振动异常', value: 28 },
  { name: '温度异常', value: 22 },
  { name: '电流异常', value: 18 },
  { name: '润滑异常', value: 12 },
  { name: '液压异常', value: 8 },
  { name: '通讯异常', value: 7 },
  { name: '其他故障', value: 5 },
])

const donutColors = [RED, ORANGE, PURPLE, BLUE, '#26c6da', '#ab47bc', '#78909c']

// ── Module 6: Trend Analysis ───────────────────────────────────────
const trendTimeRange = ref<'24h' | '7d'>('24h')
const servoCurrentTrend = ref<number[]>([])
const vibrationTrend = ref<number[]>([])
const temperatureTrend = ref<number[]>([])
const trendTimeLabels = ref<string[]>([])

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

// ── ECharts refs ───────────────────────────────────────────────────
const healthGaugeRef = ref<HTMLDivElement>()
const donutChartRef = ref<HTMLDivElement>()
const trendChartRef = ref<HTMLDivElement>()

let healthGaugeInst: echarts.ECharts | null = null
let donutChartInst: echarts.ECharts | null = null
let healthTrendChartInst: echarts.ECharts | null = null
let allCharts: echarts.ECharts[] = []

let updateTimer: ReturnType<typeof setInterval> | undefined
let resizeHandler: (() => void) | undefined
let statusCycleTimer: ReturnType<typeof setInterval> | undefined

// ── Chart option builders ──────────────────────────────────────────
function buildHealthGaugeOption(val: number) {
  const color = val >= 90 ? GREEN : val >= 70 ? ORANGE : RED
  const legendItems = [
    { color: GREEN, label: '健康 ≥90' },
    { color: ORANGE, label: '异常 70-90' },
    { color: RED, label: '故障 <70' },
  ]
  return {
    graphic: legendItems.map((item, i) => [
      {
        type: 'rect',
        right: 18,
        top: 18 + i * 26,
        shape: { width: 14, height: 10, r: 2 },
        style: { fill: item.color, shadowBlur: 6, shadowColor: item.color },
      },
      {
        type: 'text',
        right: 38,
        top: 14 + i * 26,
        style: { text: item.label, fill: 'rgba(210,230,248,0.78)', fontSize: 12, fontWeight: 500 },
      },
    ]).flat(),
    series: [{
      type: 'gauge',
      startAngle: 210,
      endAngle: -30,
      center: ['50%', '52%'],
      radius: '82%',
      min: 0,
      max: 100,
      splitNumber: 10,
      axisLine: {
        show: true,
        lineStyle: {
          width: 22,
          color: [
            [0.5, RED],
            [0.7, ORANGE],
            [0.9, GREEN],
            [1, GREEN],
          ],
        },
      },
      pointer: {
        length: '72%',
        width: 8,
        itemStyle: { color, shadowBlur: 18, shadowColor: color },
      },
      axisTick: { distance: -22, length: 6, lineStyle: { width: 1.5, color: 'rgba(180,215,240,0.5)' } },
      splitLine: { distance: -26, length: 16, lineStyle: { width: 3, color: 'rgba(180,215,240,0.6)' } },
      axisLabel: { distance: 32, color: 'rgba(200,230,250,0.8)', fontSize: 14, formatter: '{value}' },
      anchor: { show: true, size: 16, itemStyle: { borderWidth: 2, borderColor: color } },
      title: { offsetCenter: [0, '92%'], color: 'rgba(200,230,250,0.7)', fontSize: 12 },
      detail: {
        valueAnimation: true,
        fontSize: 36,
        fontWeight: 'bold',
        offsetCenter: [0, '52%'],
        formatter: '{value}%',
        color: '#fff',
        textShadowColor: color,
        textShadowBlur: 14,
      },
      data: [{ value: val, name: '主轴电机健康度' }],
    }],
  }
}

function buildDonutChartOption(data: { name: string; value: number }[]) {
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(6,14,38,0.94)',
      borderColor: 'rgba(0,200,255,0.4)',
      textStyle: { color: '#f0f4fa', fontSize: 14 },
      formatter: (params: any) =>
        `<b style="font-size:15px">${params.name}</b><br/>数量: <b style="color:${params.color};font-size:18px">${params.value}</b><br/>占比: <b style="font-size:15px">${params.percent}%</b>`,
    },
    series: [{
      type: 'pie',
      radius: ['48%', '74%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 4, borderColor: 'rgba(6,18,46,0.8)', borderWidth: 3 },
      label: {
        show: true,
        position: 'outside',
        formatter: '{b}',
        color: 'rgba(210,230,248,0.85)',
        fontWeight: 'bold',
        fontSize: 12,
      },
      labelLine: {
        show: true,
        length: 16,
        length2: 36,
        lineStyle: { color: 'rgba(150,200,240,0.35)', width: 1.5 },
      },
      emphasis: {
        label: { show: true, fontSize: 18, fontWeight: 'bold' },
        scaleSize: 12,
      },
      data: data.map((item, i) => ({
        value: item.value,
        name: item.name,
        itemStyle: { color: donutColors[i] },
        label: {
          color: 'rgba(210,230,248,0.85)',
          fontWeight: 'bold',
          fontSize: 12,
        },
      })),
    }],
  }
}

function buildTrendOption(labels: string[], currentData: number[], vibrationData: number[], tempData: number[]) {
  const currentColor = '#448aff'
  const vibrationColor = '#69f0ae'
  const tempColor = '#ffab40'
  return {
    grid: { left: 56, right: 140, top: 44, bottom: 28 },
    xAxis: {
      type: 'category',
      data: labels,
      boundaryGap: false,
      axisLine: { lineStyle: { color: 'rgba(100,160,230,0.45)', width: 1 } },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(210,230,248,0.72)',
        fontSize: 12,
        fontWeight: 500,
        interval: Math.floor(labels.length / 8),
      },
    },
    yAxis: [
      {
        type: 'value',
        name: '伺服电流 (A)',
        nameTextStyle: { color: currentColor, fontSize: 13, fontWeight: 600 },
        axisLabel: { color: 'rgba(210,230,248,0.75)', fontSize: 12 },
        splitLine: { lineStyle: { color: 'rgba(80,140,210,0.15)', type: 'dashed', width: 1 } },
      },
      {
        type: 'value',
        name: '温度 (°C)',
        nameTextStyle: { color: tempColor, fontSize: 13, fontWeight: 600 },
        axisLabel: { color: 'rgba(210,230,248,0.75)', fontSize: 12 },
        splitLine: { show: false },
      },
      {
        type: 'value',
        name: '振动 (mm/s)',
        offset: 80,
        nameTextStyle: { color: vibrationColor, fontSize: 13, fontWeight: 600 },
        axisLabel: { color: 'rgba(210,230,248,0.75)', fontSize: 12 },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        name: '伺服电流',
        type: 'line',
        yAxisIndex: 0,
        data: currentData,
        smooth: true,
        symbol: 'none',
        lineStyle: { color: currentColor, width: 2, shadowBlur: 8, shadowColor: currentColor },
      },
      {
        name: '温度',
        type: 'line',
        yAxisIndex: 1,
        data: tempData,
        smooth: true,
        symbol: 'none',
        lineStyle: { color: tempColor, width: 2, shadowBlur: 8, shadowColor: tempColor },
      },
      {
        name: '振动信号',
        type: 'line',
        yAxisIndex: 2,
        data: vibrationData,
        smooth: true,
        symbol: 'none',
        lineStyle: { color: vibrationColor, width: 2, shadowBlur: 8, shadowColor: vibrationColor },
      },
    ],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(6,14,38,0.94)',
      borderColor: 'rgba(0,200,255,0.4)',
      textStyle: { color: '#f0f4fa', fontSize: 14 },
      formatter: (params: any) => {
        let html = `<b>${params[0].axisValue}</b><br/>`
        params.forEach((p: any) => {
          const unit = p.seriesName === '温度' ? '°C' : p.seriesName === '伺服电流' ? 'A' : 'mm/s'
          html += `<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${p.color};margin-right:6px;"></span>${p.seriesName}: <b style="font-size:16px">${p.value} ${unit}</b><br/>`
        })
        return html
      },
    },
  }
}

// ── Init charts ────────────────────────────────────────────────────
function initCharts() {
  if (healthGaugeRef.value) {
    healthGaugeInst = echarts.init(healthGaugeRef.value)
    healthGaugeInst.setOption(buildHealthGaugeOption(healthScore.value))
  }
  if (donutChartRef.value) {
    donutChartInst = echarts.init(donutChartRef.value)
    donutChartInst.setOption(buildDonutChartOption(alarmDistribution.value))
  }
  if (trendChartRef.value) {
    healthTrendChartInst = echarts.init(trendChartRef.value)
    healthTrendChartInst.setOption(
      buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value)
    )
  }
  allCharts = [healthGaugeInst, donutChartInst, healthTrendChartInst].filter(Boolean) as echarts.ECharts[]
}

// ── Update data ────────────────────────────────────────────────────
function updateData() {
  // Spindle motor health drift
  const drift = (Math.random() - 0.5) * 1.4
  healthScore.value = +Math.max(42, Math.min(98, healthScore.value + drift)).toFixed(1)

  // Update trend series
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

  // Update charts
  healthGaugeInst?.setOption(buildHealthGaugeOption(healthScore.value))
  healthTrendChartInst?.setOption(
    buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value)
  )

  // Randomly update alarm distribution
  if (Math.random() < 0.3) {
    const idx = Math.floor(Math.random() * alarmDistribution.value.length)
    alarmDistribution.value[idx] = {
      ...alarmDistribution.value[idx],
      value: Math.max(1, alarmDistribution.value[idx].value + Math.floor((Math.random() - 0.5) * 3)),
    }
    donutChartInst?.setOption(buildDonutChartOption(alarmDistribution.value))
  }

  // Update alarm events
  alarmEvents.value = generateAlarmEvents()

  // Randomly update today runtime
  const hours = Math.floor(Math.random() * 2) + 6
  const mins = Math.floor(Math.random() * 60)
  todayRuntime.value = `${hours}h ${mins}m`

  // Update subsystem metrics randomly
  // 主轴系统: 振动监测, 温度监测, 电流监测, 转速监测
  subsystems.value[0].metrics[0].value = (2.5 + Math.random() * 2.5).toFixed(2)
  subsystems.value[0].metrics[1].value = (48 + Math.random() * 10).toFixed(2)
  subsystems.value[0].metrics[2].value = (38 + Math.random() * 20).toFixed(2)
  subsystems.value[0].metrics[3].value = Math.floor(2800 + Math.random() * 1200).toString()

  // 进给系统: 伺服电流, 跟随误差, 位置误差, 振动状态
  subsystems.value[1].metrics[0].value = (10 + Math.random() * 6).toFixed(2)
  subsystems.value[1].metrics[1].value = (Math.random() * 0.05).toFixed(2)
  subsystems.value[1].metrics[2].value = (Math.random() * 0.03).toFixed(2)
  subsystems.value[1].metrics[3].value = (1.2 + Math.random() * 1.8).toFixed(2)

  // 液压系统: 系统压力, 液压流量, 响应速度
  subsystems.value[2].metrics[0].value = (14.5 + Math.random() * 4).toFixed(2)
  subsystems.value[2].metrics[1].value = (22 + Math.random() * 6).toFixed(2)
  subsystems.value[2].metrics[2].value = (0.08 + Math.random() * 0.1).toFixed(2)

  // 润滑系统: 润滑压力, 供油流量, 油液品质
  subsystems.value[3].metrics[0].value = (0.3 + Math.random() * 0.3).toFixed(2)
  subsystems.value[3].metrics[1].value = (2.2 + Math.random() * 1.6).toFixed(2)
  subsystems.value[3].metrics[2].value = Math.floor(70 + Math.random() * 25).toString()

  // Random health score drift and status changes
  subsystems.value.forEach((sub) => {
    sub.healthScore = Math.max(45, Math.min(98, sub.healthScore + Math.floor((Math.random() - 0.5) * 3)))
    const r = Math.random()
    if (r < 0.04) sub.status = 'fault'
    else if (r < 0.12) sub.status = 'warning'
    else if (r < 0.84) sub.status = 'normal'
  })
}

// ── Lifecycle ──────────────────────────────────────────────────────
onMounted(async () => {
  alarmEvents.value = generateAlarmEvents()

  const trendResult = generateTrendData(288, 24)
  trendTimeLabels.value = trendResult.labels
  servoCurrentTrend.value = trendResult.currentData
  vibrationTrend.value = trendResult.vibrationData
  temperatureTrend.value = trendResult.tempData

  await nextTick()
  initCharts()

  updateTimer = setInterval(updateData, 3000)
  statusCycleTimer = setInterval(cycleDeviceStatus, 12000)

  resizeHandler = () => allCharts.forEach(c => c.resize())
  window.addEventListener('resize', resizeHandler)
})

onUnmounted(() => {
  if (updateTimer) clearInterval(updateTimer)
  if (statusCycleTimer) clearInterval(statusCycleTimer)
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  allCharts.forEach(c => c.dispose())
})
</script>

<template>
  <div class="dashboard-view">
    <div class="dashboard-grid">
      <!-- ════════════════════════════════════════════════════════════
           MODULE 1: Device Running Status
           ════════════════════════════════════════════════════════════ -->
      <div class="card device-status-card">
        <div class="card-header">
          <div class="header-left">
            <span class="header-icon device-icon"></span>
            <span class="header-title">设备运行状态</span>
            <span class="header-badge" :class="statusClass">{{ statusText }}</span>
          </div>
          <div class="header-right">
            <span class="header-unit">DEVICE STATUS</span>
          </div>
        </div>
        <div class="card-corners">
          <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
        </div>
        <div class="card-body device-body">
          <div class="device-visual">
            <div class="device-icon-large">
              <div class="device-shape">
                <div class="device-core" :class="statusClass"></div>
                <div class="device-ring r1"></div>
                <div class="device-ring r2"></div>
                <div class="device-ring r3"></div>
              </div>
              <div class="device-particles" :class="{ 'particles-active': deviceStatus === 'running' }">
                <span class="dp dp1"></span><span class="dp dp2"></span><span class="dp dp3"></span>
                <span class="dp dp4"></span><span class="dp dp5"></span><span class="dp dp6"></span>
              </div>
            </div>
            <div class="device-status-bar">
              <div class="status-indicator" :class="statusClass">
                <span class="si-dot"></span>
                <span class="si-text">{{ statusText }}</span>
              </div>
              <div class="online-indicator" :class="{ online: isOnline }">
                <span class="oi-dot"></span>
                <span class="oi-text">{{ isOnline ? '在线' : '离线' }}</span>
              </div>
            </div>
          </div>
          <div class="device-info">
            <div class="info-row">
              <span class="info-label">设备名称</span>
              <span class="info-value">{{ deviceName }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">设备编号</span>
              <span class="info-value mono">{{ deviceId }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">开机时长</span>
              <span class="info-value">{{ powerOnDuration }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">当日运行</span>
              <span class="info-value">{{ todayRuntime }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">加工状态</span>
              <span class="info-value highlight">{{ machiningStatus }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">当前工件</span>
              <span class="info-value">{{ workpiece }}</span>
            </div>
          </div>
        </div>
        <div class="card-scan-line"></div>
      </div>

      <!-- ════════════════════════════════════════════════════════════
           MODULE 2: Motor Health
           ════════════════════════════════════════════════════════════ -->
      <div class="card motor-health-card">
        <div class="card-header">
          <div class="header-left">
            <span class="header-icon motor-icon"></span>
            <span class="header-title">电机健康度</span>
            <span class="header-badge" :class="healthLevel.cls">{{ healthLevel.text }}</span>
          </div>
          <div class="header-right">
            <span class="header-unit">MOTOR HEALTH</span>
          </div>
        </div>
        <div class="card-corners">
          <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
        </div>
        <div class="card-body motor-body">
          <div class="gauge-fullwrap" ref="healthGaugeRef"></div>
        </div>
        <div class="card-scan-line"></div>
      </div>

      <!-- ════════════════════════════════════════════════════════════
           MODULE 3: Real-time Alarms & Events
           ════════════════════════════════════════════════════════════ -->
      <div class="card alarm-card">
        <div class="card-header">
          <div class="header-left">
            <span class="header-icon alarm-icon"></span>
            <span class="header-title">实时报警与事件</span>
            <span class="header-badge badge-danger">{{ alarmEvents.filter(e => e.level === 'critical').length }} 严重</span>
          </div>
          <div class="header-right">
            <span class="header-unit">ALARMS & EVENTS</span>
          </div>
        </div>
        <div class="card-corners">
          <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
        </div>
        <div class="card-body alarm-body">
          <div class="alarm-list">
            <div
              v-for="(event, idx) in alarmEvents"
              :key="idx"
              class="alarm-row"
              :class="'alarm-' + event.level"
            >
              <div class="alarm-time">{{ event.time }}</div>
              <div class="alarm-dot" :class="'dot-' + event.level"></div>
              <div class="alarm-content">
                <div class="alarm-type-row">
                  <span class="alarm-type-badge" :class="'type-' + event.level">
                    {{ event.isAlarm ? (event.level === 'critical' ? '严重' : '一般') : '事件' }}
                  </span>
                  <span class="alarm-type">{{ event.type }}</span>
                  <span class="alarm-system">{{ event.system }}</span>
                </div>
                <div class="alarm-desc">{{ event.description }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="card-scan-line"></div>
      </div>

      <!-- ════════════════════════════════════════════════════════════
           MODULE 4: Subsystem Running Status
           ════════════════════════════════════════════════════════════ -->
      <div class="card subsystem-card">
        <div class="card-header">
          <div class="header-left">
            <span class="header-icon subsystem-icon"></span>
            <span class="header-title">子系统运行状态</span>
          </div>
          <div class="header-right">
            <span class="header-unit">SUBSYSTEM STATUS</span>
          </div>
        </div>
        <div class="card-corners">
          <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
        </div>
        <div class="card-body subsystem-body">
          <div
            v-for="sub in subsystems"
            :key="sub.name"
            class="subsystem-card-item"
            :class="'subsystem-card--' + sub.status + (sub.routeName !== 'dashboard' ? ' clickable' : '')"
            @click="navigateTo(sub.routeName)"
          >
            <!-- Card header: name + status light + health score -->
            <div class="sub-card-top">
              <div class="sub-card-title-row">
                <span class="sub-card-status-light" :class="'light-' + sub.status"></span>
                <span class="sub-card-name">{{ sub.name }}</span>
                <span class="sub-card-status-tag" :class="'substatus-' + sub.status">
                  {{ sub.status === 'normal' ? '正常' : sub.status === 'warning' ? '预警' : '故障' }}
                </span>
              </div>
              <div class="sub-card-health">
                <span class="sub-health-label">健康评分</span>
                <span class="sub-health-score" :class="'health-' + sub.status">{{ sub.healthScore }}</span>
              </div>
            </div>
            <!-- Card body: monitoring parameters (two-column table) -->
            <div class="sub-card-params">
              <template v-for="m in sub.metrics" :key="m.label">
                <span class="sub-param-label">{{ m.label }}</span>
                <span class="sub-param-value">
                  {{ m.value }}<small class="sub-param-unit">{{ m.unit }}</small>
                </span>
              </template>
            </div>
          </div>
        </div>
        <div class="card-scan-line"></div>
      </div>

      <!-- ════════════════════════════════════════════════════════════
           MODULE 5: Alarm Type Distribution (Donut Chart)
           ════════════════════════════════════════════════════════════ -->
      <div class="card donut-card">
        <div class="card-header">
          <div class="header-left">
            <span class="header-icon chart-icon"></span>
            <span class="header-title">报警类型分布</span>
          </div>
          <div class="header-right">
            <span class="header-unit">ALARM DISTRIBUTION</span>
          </div>
        </div>
        <div class="card-corners">
          <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
        </div>
        <div class="card-body donut-body">
          <div class="chart-fullwrap" ref="donutChartRef"></div>
        </div>
        <div class="card-scan-line"></div>
      </div>

      <!-- ════════════════════════════════════════════════════════════
           MODULE 6: Key Parameter Trend Analysis
           ════════════════════════════════════════════════════════════ -->
      <div class="card trend-card">
        <div class="card-header">
          <div class="header-left">
            <span class="header-icon trend-icon"></span>
            <span class="header-title">关键参数趋势分析</span>
          </div>
          <div class="header-right trend-controls">
            <button
              class="range-btn"
              :class="{ active: trendTimeRange === '24h' }"
              @click="switchTimeRange('24h')"
            >24H</button>
            <button
              class="range-btn"
              :class="{ active: trendTimeRange === '7d' }"
              @click="switchTimeRange('7d')"
            >7D</button>
          </div>
        </div>
        <div class="card-corners">
          <span class="c-tl"></span><span class="c-tr"></span><span class="c-bl"></span><span class="c-br"></span>
        </div>
        <div class="card-body trend-body">
          <div class="chart-fullwrap" ref="trendChartRef"></div>
        </div>
        <div class="card-scan-line"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Root ─────────────────────────────────────────────────────────── */
.dashboard-view {
  height: calc(100vh - 210px);
  overflow: hidden;
  padding: 6px 18px 0;
  position: relative;
  z-index: 1;
}

/* ── Dashboard Grid: 3 columns x 2 rows ──────────────────────────── */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 12px;
  height: 100%;
}

/* ── Card base (same as SpindleSystemView) ────────────────────────── */
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

/* ── Card corners ─────────────────────────────────────────────────── */
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

/* ── Card header ──────────────────────────────────────────────────── */
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

.device-icon { background: radial-gradient(circle, rgba(0,229,255,0.25), rgba(0,100,200,0.15)); }
.motor-icon { background: radial-gradient(circle, rgba(105,240,174,0.25), rgba(20,160,80,0.15)); }
.alarm-icon { background: radial-gradient(circle, rgba(255,82,82,0.25), rgba(180,20,20,0.15)); }
.subsystem-icon { background: radial-gradient(circle, rgba(68,138,255,0.25), rgba(20,60,180,0.15)); }
.chart-icon { background: radial-gradient(circle, rgba(124,77,255,0.25), rgba(80,20,180,0.15)); }
.trend-icon { background: radial-gradient(circle, rgba(0,229,255,0.25), rgba(0,140,200,0.15)); }

.header-title {
  font-size: 16px;
  font-weight: 700;
  color: rgba(225, 240, 255, 0.92);
  letter-spacing: 1.5px;
}

.header-badge {
  font-size: 13px;
  padding: 2px 10px;
  border-radius: 10px;
  letter-spacing: 1px;
  font-weight: 600;
}

.badge-normal { background: rgba(105,240,174,0.14); color: #69f0ae; border: 1px solid rgba(105,240,174,0.25); }
.badge-warning { background: rgba(255,171,64,0.14); color: #ffab40; border: 1px solid rgba(255,171,64,0.25); }
.badge-danger { background: rgba(255,82,82,0.14); color: #ff5252; border: 1px solid rgba(255,82,82,0.25); animation: danger-blink 1s ease-in-out infinite; }

.status-running { background: rgba(105,240,174,0.14); color: #69f0ae; border: 1px solid rgba(105,240,174,0.25); }
.status-standby { background: rgba(68,138,255,0.14); color: #448aff; border: 1px solid rgba(68,138,255,0.25); }
.status-stop { background: rgba(255,171,64,0.14); color: #ffab40; border: 1px solid rgba(255,171,64,0.25); }
.status-fault { background: rgba(255,82,82,0.14); color: #ff5252; border: 1px solid rgba(255,82,82,0.25); animation: danger-blink 1s ease-in-out infinite; }

.header-unit {
  font-size: 12px;
  letter-spacing: 2px;
  color: rgba(150, 200, 230, 0.55);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ── Card body ────────────────────────────────────────────────────── */
.card-body {
  position: relative;
  z-index: 2;
  flex: 1;
  min-height: 0;
}

/* ── Card scan line ───────────────────────────────────────────────── */
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

/* ═══════════════════════════════════════════════════════════════════
   MODULE 1: Device Status
   ═══════════════════════════════════════════════════════════════════ */
.device-body {
  display: flex;
  flex-direction: row;
  padding: 16px 18px;
  gap: 18px;
}

.device-visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  min-width: 160px;
}

.device-icon-large {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.device-shape {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.device-core {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 40%, rgba(255,255,255,0.3), rgba(0,229,255,0.4));
  position: relative;
  z-index: 2;
  transition: all 0.5s ease;
}

.device-core.status-running {
  background: radial-gradient(circle at 40% 40%, rgba(255,255,255,0.3), #69f0ae);
  box-shadow: 0 0 24px rgba(105,240,174,0.5), 0 0 48px rgba(105,240,174,0.2);
}
.device-core.status-standby {
  background: radial-gradient(circle at 40% 40%, rgba(255,255,255,0.3), #448aff);
  box-shadow: 0 0 24px rgba(68,138,255,0.5), 0 0 48px rgba(68,138,255,0.2);
}
.device-core.status-stop {
  background: radial-gradient(circle at 40% 40%, rgba(255,255,255,0.3), #ffab40);
  box-shadow: 0 0 24px rgba(255,171,64,0.5), 0 0 48px rgba(255,171,64,0.2);
}
.device-core.status-fault {
  background: radial-gradient(circle at 40% 40%, rgba(255,255,255,0.3), #ff5252);
  box-shadow: 0 0 24px rgba(255,82,82,0.5), 0 0 48px rgba(255,82,82,0.2);
  animation: fault-pulse 0.6s ease-in-out infinite;
}

.device-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(0, 200, 255, 0.25);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
.device-ring.r1 { width: 58px; height: 58px; animation: ring-rotate 3s linear infinite; }
.device-ring.r2 { width: 74px; height: 74px; border-style: dashed; animation: ring-rotate 5s linear infinite reverse; }
.device-ring.r3 { width: 90px; height: 90px; border-style: dotted; animation: ring-rotate 7s linear infinite; }

.device-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.dp {
  position: absolute;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: rgba(0, 229, 255, 0.6);
  opacity: 0;
}

.particles-active .dp { animation: particle-float 2s ease-in-out infinite; }
.dp1 { top: 20%; left: 10%; animation-delay: 0s; }
.dp2 { top: 5%; left: 50%; animation-delay: 0.4s; }
.dp3 { top: 20%; right: 10%; animation-delay: 0.8s; }
.dp4 { bottom: 20%; left: 15%; animation-delay: 1.2s; }
.dp5 { bottom: 5%; left: 50%; animation-delay: 1.6s; }
.dp6 { bottom: 20%; right: 15%; animation-delay: 2s; }

.device-status-bar {
  display: flex;
  gap: 16px;
}

.status-indicator,
.online-indicator {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 14px;
  letter-spacing: 1px;
}

.si-dot, .oi-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.status-indicator.status-running .si-dot { background: #69f0ae; box-shadow: 0 0 8px rgba(105,240,174,0.6); }
.status-indicator.status-standby .si-dot { background: #448aff; box-shadow: 0 0 8px rgba(68,138,255,0.6); }
.status-indicator.status-stop .si-dot { background: #ffab40; box-shadow: 0 0 8px rgba(255,171,64,0.6); }
.status-indicator.status-fault .si-dot { background: #ff5252; box-shadow: 0 0 8px rgba(255,82,82,0.6); animation: fault-pulse 0.6s ease-in-out infinite; }

.si-text { color: rgba(210,230,245,0.85); }

.online-indicator .oi-dot { background: #69f0ae; box-shadow: 0 0 8px rgba(105,240,174,0.6); animation: pulse-dot 2.2s ease-in-out infinite; }
.online-indicator:not(.online) .oi-dot { background: #ff5252; box-shadow: 0 0 8px rgba(255,82,82,0.6); animation: none; }
.oi-text { color: rgba(210,230,245,0.65); font-size: 14px; }

.device-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  justify-content: center;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 12px;
  background: rgba(0, 140, 255, 0.04);
  border: 1px solid rgba(0, 160, 255, 0.08);
  border-radius: 8px;
}

.info-label {
  font-size: 14px;
  color: rgba(160, 210, 240, 0.65);
  letter-spacing: 1px;
}

.info-value {
  font-size: 16px;
  color: rgba(225, 240, 255, 0.9);
  font-weight: 600;
  letter-spacing: 1px;
}

.info-value.mono {
  font-family: 'Courier New', monospace;
  color: #00e5ff;
  text-shadow: 0 0 8px rgba(0, 229, 255, 0.3);
}

.info-value.highlight {
  color: #69f0ae;
  text-shadow: 0 0 8px rgba(105, 240, 174, 0.3);
}

/* ═══════════════════════════════════════════════════════════════════
   MODULE 2: Motor Health
   ═══════════════════════════════════════════════════════════════════ */
.motor-body {
  padding: 4px;
}

.gauge-fullwrap {
  width: 100%;
  height: 100%;
}

/* ═══════════════════════════════════════════════════════════════════
   MODULE 3: Alarms & Events
   ═══════════════════════════════════════════════════════════════════ */
.alarm-body {
  padding: 8px 10px;
  overflow: hidden;
}

.alarm-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
  height: 100%;
  overflow-y: auto;
}

.alarm-list::-webkit-scrollbar {
  width: 3px;
}
.alarm-list::-webkit-scrollbar-track {
  background: transparent;
}
.alarm-list::-webkit-scrollbar-thumb {
  background: rgba(0, 180, 255, 0.15);
  border-radius: 2px;
}

.alarm-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(0, 100, 200, 0.04);
  border: 1px solid rgba(0, 140, 255, 0.06);
  transition: all 0.3s ease;
  position: relative;
}

.alarm-row::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  border-radius: 3px 0 0 3px;
}

.alarm-row.alarm-critical::before { background: #ff5252; box-shadow: 0 0 6px rgba(255,82,82,0.4); }
.alarm-row.alarm-warning::before { background: #ffab40; box-shadow: 0 0 6px rgba(255,171,64,0.4); }
.alarm-row.alarm-info::before { background: #448aff; box-shadow: 0 0 6px rgba(68,138,255,0.4); }

.alarm-row:hover {
  background: rgba(0, 140, 255, 0.08);
  border-color: rgba(0, 180, 255, 0.15);
}

.alarm-time {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: rgba(200, 225, 245, 0.75);
  min-width: 68px;
  padding-top: 2px;
}

.alarm-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}

.dot-critical { background: #ff5252; box-shadow: 0 0 8px rgba(255,82,82,0.5); animation: danger-blink 1s ease-in-out infinite; }
.dot-warning { background: #ffab40; box-shadow: 0 0 6px rgba(255,171,64,0.4); }
.dot-info { background: #448aff; box-shadow: 0 0 6px rgba(68,138,255,0.4); }

.alarm-content {
  flex: 1;
  min-width: 0;
}

.alarm-type-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 3px;
}

.alarm-type-badge {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 6px;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.type-critical { background: rgba(255,82,82,0.18); color: #ff5252; border: 1px solid rgba(255,82,82,0.3); }
.type-warning { background: rgba(255,171,64,0.18); color: #ffab40; border: 1px solid rgba(255,171,64,0.3); }
.type-info { background: rgba(68,138,255,0.18); color: #448aff; border: 1px solid rgba(68,138,255,0.3); }

.alarm-type {
  font-size: 14px;
  color: rgba(225, 240, 255, 0.85);
  font-weight: 600;
}

.alarm-system {
  font-size: 13px;
  color: rgba(170, 215, 240, 0.6);
  margin-left: auto;
}

.alarm-desc {
  font-size: 13px;
  color: rgba(170, 210, 240, 0.55);
}

/* ═══════════════════════════════════════════════════════════════════
   MODULE 4: Subsystem Status
   ═══════════════════════════════════════════════════════════════════ */
.subsystem-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 6px;
  padding: 4px 8px;
}

/* ── Subsystem card item ────────────────────────────────────────── */
.subsystem-card-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 5px 8px;
  border-radius: 8px;
  background: rgba(0, 100, 200, 0.05);
  border: 1px solid rgba(0, 140, 255, 0.12);
  transition: all 0.3s ease;
  cursor: default;
  position: relative;
  overflow: hidden;
}

.subsystem-card-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6px;
  bottom: 6px;
  width: 3px;
  border-radius: 0 3px 3px 0;
  transition: all 0.3s ease;
}

.subsystem-card-item.subsystem-card--normal::before {
  background: #69f0ae;
  box-shadow: 0 0 10px rgba(105, 240, 174, 0.4);
}
.subsystem-card-item.subsystem-card--warning::before {
  background: #ffab40;
  box-shadow: 0 0 10px rgba(255, 171, 64, 0.4);
}
.subsystem-card-item.subsystem-card--fault::before {
  background: #ff5252;
  box-shadow: 0 0 10px rgba(255, 82, 82, 0.5);
  animation: fault-pulse 0.6s ease-in-out infinite;
}

.subsystem-card-item.clickable {
  cursor: pointer;
}

.subsystem-card-item.clickable:hover {
  border-color: rgba(0, 200, 255, 0.35);
  background: rgba(0, 140, 255, 0.1);
  box-shadow:
    inset 0 0 24px rgba(0, 140, 255, 0.08),
    0 0 18px rgba(0, 140, 255, 0.08);
  transform: translateY(-1px);
}

/* ── Card top: title row + health score ─────────────────────────── */
.sub-card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.sub-card-title-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.sub-card-status-light {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.light-normal { background: #69f0ae; box-shadow: 0 0 10px rgba(105, 240, 174, 0.6); }
.light-warning { background: #ffab40; box-shadow: 0 0 10px rgba(255, 171, 64, 0.6); animation: pulse-dot 1.8s ease-in-out infinite; }
.light-fault { background: #ff5252; box-shadow: 0 0 10px rgba(255, 82, 82, 0.6); animation: fault-pulse 0.6s ease-in-out infinite; }

.sub-card-name {
  font-size: 14px;
  font-weight: 700;
  color: rgba(225, 240, 255, 0.93);
  letter-spacing: 1px;
}

.sub-card-status-tag {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 6px;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.substatus-normal { background: rgba(105, 240, 174, 0.13); color: #69f0ae; border: 1px solid rgba(105, 240, 174, 0.25); }
.substatus-warning { background: rgba(255, 171, 64, 0.13); color: #ffab40; border: 1px solid rgba(255, 171, 64, 0.25); }
.substatus-fault { background: rgba(255, 82, 82, 0.13); color: #ff5252; border: 1px solid rgba(255, 82, 82, 0.25); animation: danger-blink 1s ease-in-out infinite; }

.sub-card-health {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0;
}

.sub-health-label {
  font-size: 10px;
  color: rgba(150, 200, 230, 0.5);
  letter-spacing: 0.5px;
}

.sub-health-score {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.health-normal { color: #69f0ae; text-shadow: 0 0 12px rgba(105, 240, 174, 0.35); }
.health-warning { color: #ffab40; text-shadow: 0 0 12px rgba(255, 171, 64, 0.35); }
.health-fault { color: #ff5252; text-shadow: 0 0 12px rgba(255, 82, 82, 0.4); }

/* ── Card params table (unified two-column) ─────────────────────── */
.sub-card-params {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2px 14px;
  align-items: center;
}

.sub-param-label {
  font-size: 12px;
  color: rgba(160, 210, 235, 0.65);
  letter-spacing: 0.5px;
  text-align: left;
}

.sub-param-value {
  font-size: 14px;
  font-weight: 700;
  color: rgba(225, 245, 255, 0.94);
  letter-spacing: 0.5px;
  text-align: left;
}

.sub-param-unit {
  font-size: 10px;
  font-weight: 400;
  color: rgba(170, 210, 235, 0.5);
  margin-left: 2px;
}

/* ═══════════════════════════════════════════════════════════════════
   MODULE 5 & 6: Charts
   ═══════════════════════════════════════════════════════════════════ */
.donut-body {
  padding: 8px;
}

.trend-body {
  padding: 4px;
}

.chart-fullwrap {
  width: 100%;
  height: 100%;
  min-height: 200px;
}

/* ── Trend range buttons ──────────────────────────────────────────── */
.trend-controls {
  gap: 4px;
}

.range-btn {
  padding: 4px 14px;
  border: 1px solid rgba(0, 180, 255, 0.2);
  border-radius: 8px;
  background: transparent;
  color: rgba(200, 220, 240, 0.6);
  font-size: 14px;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all 0.25s ease;
}

.range-btn:hover {
  border-color: rgba(0, 200, 255, 0.4);
  color: rgba(220, 240, 255, 0.85);
}

.range-btn.active {
  background: linear-gradient(180deg, rgba(0, 180, 255, 0.18), rgba(0, 100, 200, 0.12));
  border-color: rgba(0, 229, 255, 0.5);
  color: #00e5ff;
  box-shadow: 0 0 12px rgba(0, 180, 255, 0.15);
}

/* ═══════════════════════════════════════════════════════════════════
   Animations
   ═══════════════════════════════════════════════════════════════════ */
@keyframes icon-pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.08); }
}

@keyframes card-scan {
  0% { transform: translateX(-160%) skewX(-20deg); }
  100% { transform: translateX(520%) skewX(-20deg); }
}

@keyframes danger-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes fault-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.08); opacity: 0.7; }
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.3); }
}

@keyframes ring-rotate {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes particle-float {
  0%, 100% { opacity: 0; transform: translateY(0) scale(0.5); }
  30% { opacity: 0.8; }
  70% { opacity: 0.8; }
  100% { opacity: 0; transform: translateY(-14px) scale(1.2); }
}

/* ═══════════════════════════════════════════════════════════════════
   Layout lock — prevent grid collapse on zoom
   ═══════════════════════════════════════════════════════════════════ */
.dashboard-view {
  min-width: 1280px;
}
</style>
