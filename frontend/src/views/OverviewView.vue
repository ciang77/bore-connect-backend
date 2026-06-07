<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, GaugeChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import { fetchTrendData, fetchAlertStatus, toggleAlert, fetchAlarms } from '../api/overview'
import SubsystemStatusInner from './SubsystemStatusInner.vue'
import DeviceStatusInner from './DeviceStatusInner.vue'

use([
  CanvasRenderer,
  LineChart,
  GaugeChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
])

// --- 报警数据 ---
interface Alarm {
  id: number
  time: string
  level: 'info' | 'warning' | 'error'
  subsystem: string
  msg: string
}

const alarms = ref<Alarm[]>([])

const loadAlarms = async () => {
  try {
    const res = await fetchAlarms()
    if (res.code === 0) alarms.value = res.data
  } catch (e) { /* ignore */ }
}

const isAlertEnabled = ref(false)

const toggleAlertSwitch = async () => {
  try {
    const res = await toggleAlert(!isAlertEnabled.value)
    if (res.code === 200) {
      isAlertEnabled.value = res.data.enabled
      console.log(res.msg)
    }
  } catch (e) {
    console.error('切换实时报警失败:', e)
  }
}

// --- 运行数据（日、月、年）---
interface RuntimeData {
  daily: {
    runtime: number
    anomalyCount: number
    anomalyDuration: number
    normalRate: number
  }
  monthly: {
    runtime: number
    anomalyCount: number
    anomalyDuration: number
    normalRate: number
  }
  yearly: {
    runtime: number
    anomalyCount: number
    anomalyDuration: number
    normalRate: number
  }
}

const runtimeData = ref<RuntimeData>({
  daily: { runtime: 18.5, anomalyCount: 3, anomalyDuration: 2.5, normalRate: 99.2 },
  monthly: { runtime: 480, anomalyCount: 12, anomalyDuration: 8.5, normalRate: 98.8 },
  yearly: { runtime: 5820, anomalyCount: 89, anomalyDuration: 72.3, normalRate: 99.1 },
})

// 总运行时间
const totalRuntime = computed(() => {
  return (runtimeData.value.daily.runtime + runtimeData.value.monthly.runtime + runtimeData.value.yearly.runtime).toFixed(1)
})

// 平均健康度
const avgHealth = computed(() => {
  return ((runtimeData.value.daily.normalRate + runtimeData.value.monthly.normalRate + runtimeData.value.yearly.normalRate) / 3).toFixed(1)
})

// --- 电机健康度数据 ---
interface Motor {
  id: string
  name: string
  type: 'main' | 'X' | 'Y' | 'Z' | 'W' | 'C'
  health: number
  status: 'running' | 'idle' | 'warning' | 'error'
}

const motors = ref<Motor[]>([
  { id: 'M-001', name: '主电机', type: 'main', health: 96, status: 'running' },
  { id: 'X-001', name: 'X轴电机1', type: 'X', health: 94, status: 'running' },
  { id: 'X-002', name: 'X轴电机2', type: 'X', health: 92, status: 'running' },
  { id: 'X-003', name: 'X轴电机3', type: 'X', health: 95, status: 'running' },
  { id: 'X-004', name: 'X轴电机4', type: 'X', health: 93, status: 'running' },
  { id: 'Y-001', name: 'Y轴电机1', type: 'Y', health: 91, status: 'warning' },
  { id: 'Y-002', name: 'Y轴电机2', type: 'Y', health: 97, status: 'running' },
  { id: 'Z-001', name: 'Z轴电机', type: 'Z', health: 95, status: 'running' },
  { id: 'W-001', name: 'W轴电机1', type: 'W', health: 98, status: 'running' },
  { id: 'W-002', name: 'W轴电机2', type: 'W', health: 96, status: 'running' },
  { id: 'W-003', name: 'W轴电机3', type: 'W', health: 94, status: 'running' },
  { id: 'W-004', name: 'W轴电机4', type: 'W', health: 92, status: 'running' },
  { id: 'C-001', name: 'C轴电机', type: 'C', health: 93, status: 'running' },
])

// --- 报警类型占比数据 ---
const alarmTypeData = ref([
  { value: 35, name: '温度异常', itemStyle: { color: '#8b5cf6' }, alarmLevel: 'high' },
  { value: 22, name: '压力异常', itemStyle: { color: '#06b6d4' }, alarmLevel: 'high' },
  { value: 18, name: '振动超标', itemStyle: { color: '#10b981' }, alarmLevel: 'medium' },
  { value: 12, name: '电流波动', itemStyle: { color: '#f59e0b' }, alarmLevel: 'medium' },
  { value: 8, name: '润滑不足', itemStyle: { color: '#6366f1' }, alarmLevel: 'low' },
  { value: 5, name: '通信中断', itemStyle: { color: '#ec4899' }, alarmLevel: 'high' },
  { value: 4, name: '油位过低', itemStyle: { color: '#0ea5e9' }, alarmLevel: 'low' },
  { value: 3, name: '过载报警', itemStyle: { color: '#84cc16' }, alarmLevel: 'high' },
])

// --- 统计数据计算 ---
const totalAlarms = computed(() => {
  return alarmTypeData.value.reduce((sum, item) => sum + item.value, 0)
})

const highLevelCount = computed(() => {
  return alarmTypeData.value
    .filter(item => item.alarmLevel === 'high')
    .reduce((sum, item) => sum + item.value, 0)
})

const mediumLevelCount = computed(() => {
  return alarmTypeData.value
    .filter(item => item.alarmLevel === 'medium')
    .reduce((sum, item) => sum + item.value, 0)
})

const lowLevelCount = computed(() => {
  return alarmTypeData.value
    .filter(item => item.alarmLevel === 'low')
    .reduce((sum, item) => sum + item.value, 0)
})

// --- 报警类型饼状图配置（南丁格尔玫瑰图）---
const alarmPieOption = computed(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'item',
    formatter: (params: any) => {
      const levelMap: Record<string, string> = {
        high: '<span style="color:#8b5cf6">高优先级</span>',
        medium: '<span style="color:#f59e0b">中优先级</span>',
        low: '<span style="color:#10b981">低优先级</span>'
      }
      return `<div style="padding:8px 12px;">
        <div style="font-weight:600;color:#fff;font-size:13px;margin-bottom:6px;">${params.name}</div>
        <div style="color:#94a3b8;font-size:12px;margin-bottom:2px;">数量: <span style="color:#38bdf8;font-weight:600">${params.value}</span> 次</div>
        <div style="color:#94a3b8;font-size:12px;margin-bottom:2px;">占比: <span style="color:#4ade80;font-weight:600">${params.percent.toFixed(1)}%</span></div>
        <div style="color:#94a3b8;font-size:12px;">级别: ${levelMap[params.data.alarmLevel] || '未知'}</div>
      </div>`
    },
    backgroundColor: 'rgba(15, 23, 42, 0.98)',
    borderColor: 'rgba(56, 189, 248, 0.3)',
    borderWidth: 1,
    padding: [12, 16],
    textStyle: {
      color: '#fff',
      fontSize: 12
    },
    extraCssText: 'border-radius: 8px;'
  },
  legend: {
    show: false
  },
  series: [
    {
      name: '报警类型',
      type: 'pie',
      radius: ['18%', '58%'],
      center: ['50%', '50%'],
      roseType: 'radius',
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 6,
        borderColor: 'rgba(15, 23, 42, 0.98)',
        borderWidth: 2
      },
      label: {
        show: true,
        position: 'outside',
        fontSize: 11,
        color: '#e2e8f0',
        fontWeight: 500,
        formatter: (params: any) => {
          return `${params.name}\n${params.value}次`
        },
        alignTo: 'labelLine',
        align: 'center',
        verticalAlign: 'middle',
        lineHeight: 16,
        padding: [0, 0, 0, 0],
        distanceFromLabelLine: 8
      },
      emphasis: {
        scale: true,
        scaleSize: 8,
        itemStyle: {
          shadowBlur: 15,
          shadowOffsetX: 0,
          shadowColor: 'rgba(139, 92, 246, 0.5)'
        },
        label: {
          color: '#fff',
          fontWeight: 600,
          fontSize: 12
        }
      },
      labelLine: {
        show: true,
        length: 15,
        length2: 20,
        smooth: true,
        smoothness: 0.3,
        lineStyle: {
          color: 'rgba(148, 163, 184, 0.5)',
          width: 1.5,
          type: 'solid'
        },
        maxSurfaceAngle: 80
      },
      data: alarmTypeData.value,
      animationType: 'scale',
      animationEasing: 'cubicOut',
      animationDelay: (idx: number) => idx * 50,
      animationDuration: 1000
    }
  ]
}))

// --- 设备运行状态仪表盘（色块分割版）---
const statusGaugeOption = computed(() => {
  const healthValue = parseFloat(avgHealth.value)
  const segments = 30
  
  const activeSegments = Math.round((healthValue / 100) * segments)
  
  const colorData: { name: string; value: number; itemStyle: { color: string } }[] = []
  for (let i = 0; i < segments; i++) {
    let color = 'rgba(255, 71, 87, 0.7)'
    if (i >= segments * 0.5) color = 'rgba(255, 184, 0, 0.7)'
    if (i >= segments * 0.75) color = 'rgba(0, 255, 153, 0.7)'
    colorData.push({
      name: '',
      value: 1,
      itemStyle: { color }
    })
  }
  
  const lineData: [number, number][] = []
  for (let i = 0; i <= activeSegments; i++) {
    const angle = 180 - (i * 180) / segments
    lineData.push([angle, 100])
  }
  
  return {
    backgroundColor: 'transparent',
    series: [
      {
        type: 'pie',
        radius: ['55%', '85%'],
        center: ['50%', '50%'],
        startAngle: 180,
        endAngle: 0,
        clockwise: false,
        itemStyle: {
          borderWidth: 1,
          borderColor: 'rgba(0, 212, 255, 0.15)'
        },
        label: { show: false },
        labelLine: { show: false },
        data: colorData
      },
      {
        type: 'line',
        coordinateSystem: 'polar',
        startAngle: 180,
        endAngle: 0,
        polar: {
          center: ['50%', '50%'],
          radius: '50%',
          startAngle: 180,
          endAngle: 0,
          axisLine: { show: false },
          axisTick: { show: false },
          axisLabel: { show: false },
          splitLine: { show: false }
        },
        lineStyle: {
          width: 2,
          type: 'dashed',
          color: '#00d4ff',
          shadowColor: 'rgba(0, 212, 255, 0.8)',
          shadowBlur: 8
        },
        symbol: 'none',
        data: lineData
      },
      {
        type: 'pie',
        radius: ['0%', '0%'],
        center: ['50%', '50%'],
        label: {
          show: true,
          position: 'center',
          fontSize: 18,
          fontWeight: 'bold',
          color: '#fff',
          textShadowColor: 'rgba(0, 212, 255, 0.6)',
          textShadowBlur: 8,
          formatter: `${healthValue}%`
        },
        labelLine: { show: false },
        data: [{ value: 1 }]
      }
    ]
  }
})

// --- 设备健康度仪表盘 ---
const healthGaugeOption = computed(() => {
  const healthValue = parseFloat(avgHealth.value)

  const axisLineWidth = 22

  return {
    backgroundColor: 'transparent',
    series: [
      {
        type: 'gauge',
        startAngle: 225,
        endAngle: -45,
        min: 0,
        max: 100,
        splitNumber: 10,
        radius: '90%',
        center: ['50%', '54%'],
        axisLine: {
          lineStyle: {
            width: axisLineWidth,
            color: [
              [0.6, '#e74c3c'],
              [0.8, '#f39c12'],
              [1, '#27ae60'],
            ],
          },
        },
        pointer: {
          length: '56%',
          width: 4,
          itemStyle: {
            color: '#ecf0f1',
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 6,
          },
        },
        axisTick: {
          distance: -axisLineWidth,
          length: 6,
          lineStyle: {
            color: '#7f8c8d',
            width: 1,
          },
        },
        splitLine: {
          distance: -axisLineWidth,
          length: 18,
          lineStyle: {
            color: '#95a5a6',
            width: 2,
          },
        },
        axisLabel: {
          color: '#bdc3c7',
          distance: axisLineWidth + 12,
          fontSize: 12,
          fontWeight: 500,
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}%',
          color: '#ecf0f1',
          fontSize: 28,
          fontWeight: 'bold',
          offsetCenter: [0, '32%'],
          textShadowColor: 'rgba(0, 0, 0, 0.8)',
          textShadowBlur: 14,
        },
        data: [
          {
            value: healthValue,
          },
        ],
      },
    ],
  }
})

// --- 趋势图表配置 ---
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

const trendChartRef = ref<HTMLDivElement>()
let healthTrendChartInst: echarts.ECharts | null = null
let updateTimer: ReturnType<typeof setInterval> | undefined
let resizeHandler: (() => void) | undefined

async function loadTrendData(range: '24h' | '7d') {
  try {
    const res = await fetchTrendData(range)
    if (res.code === 0 && res.data) {
      trendTimeLabels.value = res.data.labels
      servoCurrentTrend.value = res.data.servoCurrent
      vibrationTrend.value = res.data.vibration
      temperatureTrend.value = res.data.temperature
      healthTrendChartInst?.setOption(
        buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value), true
      )
    }
  } catch {
    // keep last data on error
  }
}

function toggleParameter(param: 'servo' | 'temp' | 'vibration') {
  if (param === 'servo') showServoCurrent.value = !showServoCurrent.value
  if (param === 'temp') showTemperature.value = !showTemperature.value
  if (param === 'vibration') showVibration.value = !showVibration.value
  healthTrendChartInst?.setOption(
    buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value), true
  )
}

function switchTimeRange(range: '24h' | '7d') {
  trendTimeRange.value = range
  loadTrendData(range)
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
        show: true,
      },
      {
        type: 'value',
        name: '温度 (°C)',
        nameTextStyle: { color: ORANGE, fontSize: 11, fontWeight: 500 },
        axisLabel: { color: 'rgba(148, 163, 184, 0.75)', fontSize: 10 },
        splitLine: { show: false },
        min: 35,
        max: 70,
        show: true,
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
        show: true,
      },
    ],
    series: [
      {
        name: '伺服电流',
        type: 'line',
        yAxisIndex: 0,
        data: showServoCurrent.value ? currentData : [],
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: BLUE, width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(68, 138, 255, 0.25)' },
            { offset: 1, color: 'rgba(68, 138, 255, 0.02)' },
          ]),
        },
      },
      {
        name: '温度',
        type: 'line',
        yAxisIndex: 1,
        data: showTemperature.value ? tempData : [],
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: ORANGE, width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 171, 64, 0.2)' },
            { offset: 1, color: 'rgba(255, 171, 64, 0.02)' },
          ]),
        },
      },
      {
        name: '振动信号',
        type: 'line',
        yAxisIndex: 2,
        data: showVibration.value ? vibrationData : [],
        smooth: 0.3,
        symbol: 'none',
        lineStyle: { color: GREEN, width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(105, 240, 174, 0.2)' },
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

function initTrendChart() {
  if (trendChartRef.value) {
    healthTrendChartInst = echarts.init(trendChartRef.value)
    healthTrendChartInst.setOption(
      buildTrendOption(trendTimeLabels.value, servoCurrentTrend.value, vibrationTrend.value, temperatureTrend.value)
    )
  }
}

function updateTrendData() {
  loadTrendData(trendTimeRange.value)
}

// --- 动态数据更新 ---
let timer: number | null = null

const updateData = () => {
  runtimeData.value.daily.runtime = Number((18.5 + Math.random() * 0.5 - 0.25).toFixed(1))
  runtimeData.value.daily.normalRate = Number((99.2 + Math.random() * 0.2 - 0.1).toFixed(1))
  loadAlarms()
}

onMounted(async () => {
  timer = window.setInterval(updateData, 3000)

  // 初始化实时报警开关状态
  try {
    const res = await fetchAlertStatus()
    if (res.code === 200) isAlertEnabled.value = res.data.enabled
  } catch (e) { /* ignore */ }

  // 初始化告警列表
  loadAlarms()

  // 初始化趋势数据
  await loadTrendData('24h')

  await nextTick()
  initTrendChart()

  updateTimer = setInterval(updateTrendData, 3000)
  resizeHandler = () => healthTrendChartInst?.resize()
  window.addEventListener('resize', resizeHandler)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  if (updateTimer) clearInterval(updateTimer)
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  healthTrendChartInst?.dispose()
})

// --- 状态标签颜色 ---
const getStatusColor = (status: string) => {
  switch (status) {
    case 'running': return 'status-running'
    case 'idle': return 'status-idle'
    case 'warning': return 'status-warning'
    case 'error': return 'status-error'
    case 'stopped': return 'status-stopped'
    default: return ''
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'running': return '运行中'
    case 'idle': return '待机'
    case 'warning': return '报警'
    case 'error': return '故障'
    case 'stopped': return '停机'
    default: return ''
  }
}

const getSubsystemStatusColor = (status: string) => {
  switch (status) {
    case 'running': return 'subsystem-running'
    case 'warning': return 'subsystem-warning'
    case 'stopped': return 'subsystem-stopped'
    default: return ''
  }
}

const getLevelText = (level: string) => {
  switch (level) {
    case 'info': return '信息'
    case 'warning': return '警告'
    case 'error': return '故障'
    default: return ''
  }
}
</script>

<template>
  <div class="view">
    <div class="content-wrapper">
      <div class="grid-container">
        <!-- 第一行第一列：设备运行状态 -->
        <div class="grid-item status-section">
          <div class="border-box">
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
                <h2 class="title-text">设备运行状态</h2>
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
              <div class="content-area">
                <DeviceStatusInner />
              </div>
              <div class="side-line right"></div>
            </div>
            <div class="border-bottom">
              <div class="corner bottom-left"></div>
              <div class="bottom-center"></div>
              <div class="corner bottom-right"></div>
            </div>
          </div>
        </div>

        <!-- 第一行第二列：子系统运行状态 -->
        <div class="grid-item subsystem-section">
          <div class="border-box">
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
                <h2 class="title-text">子系统运行状态</h2>
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
              <div class="content-area">
                <SubsystemStatusInner />
              </div>
              <div class="side-line right"></div>
            </div>
            <div class="border-bottom">
              <div class="corner bottom-left"></div>
              <div class="bottom-center"></div>
              <div class="corner bottom-right"></div>
            </div>
          </div>
        </div>

        <!-- 第一行第三列：运行趋势 -->
        <div class="grid-item trend-section">
          <div class="border-box">
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
              </div>
              <div class="side-line right"></div>
            </div>
            <div class="trend-control-bar">
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
            <div class="border-bottom">
              <div class="corner bottom-left"></div>
              <div class="bottom-center"></div>
              <div class="corner bottom-right"></div>
            </div>
          </div>
        </div>

        <!-- 第二行第一列：电机健康度 -->
        <div class="grid-item health-section">
          <div class="border-box">
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
                <h2 class="title-text">设备健康度</h2>
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
              <div class="content-area health-content-wrapper">
                <div class="health-gauge-wrapper">
                  <v-chart class="health-gauge" :option="healthGaugeOption" autoresize />
                  <div class="health-legend">
                    <div class="legend-item">
                      <span class="legend-color" style="background: #e74c3c;"></span>
                      <span class="legend-text">0-60 预警</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-color" style="background: #f39c12;"></span>
                      <span class="legend-text">60-80 注意</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-color" style="background: #27ae60;"></span>
                      <span class="legend-text">80-100 正常</span>
                    </div>
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
        </div>

        <!-- 第二行第二列：报警类型分布 -->
        <div class="grid-item pie-section">
          <div class="border-box">
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
                <h2 class="title-text">报警类型分布</h2>
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
              <div class="content-area">
                <div class="pie-content">
                  <div class="pie-chart-wrapper">
                    <v-chart class="pie-chart" :option="alarmPieOption" autoresize />
                  </div>
                  <div class="pie-legend-panel">
                    <div class="legend-title">报警类型详情</div>
                    <div class="legend-list">
                      <div 
                        v-for="item in alarmTypeData" 
                        :key="item.name" 
                        class="legend-item"
                      >
                        <span 
                          class="legend-color" 
                          :style="{ backgroundColor: item.itemStyle.color }"
                        ></span>
                        <span class="legend-name">{{ item.name }}</span>
                        <span class="legend-value">{{ item.value }}</span>
                      </div>
                    </div>
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
        </div>

        <!-- 第二行第三列：实时报警与事件记录 -->
        <div class="grid-item alarm-section">
          <div class="border-box">
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
                <h2 class="title-text">实时报警与事件记录</h2>
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
              <div class="content-area alarm-container">
                <div class="alarm-scroll-enhanced">
                  <div v-for="alarm in alarms" :key="alarm.id" class="alarm-row-enhanced" :class="alarm.level">
                    <div class="alarm-indicator"></div>
                    <span class="alarm-time">{{ alarm.time }}</span>
                    <span class="alarm-subsystem">{{ alarm.subsystem }}</span>
                    <span class="alarm-msg">{{ alarm.msg }}</span>
                    <div class="alarm-level-badge" :class="alarm.level">{{ getLevelText(alarm.level) }}</div>
                  </div>
                </div>
                <div class="alarm-actions-fixed">
                  <div class="log-switch-enhanced" :class="{ active: isAlertEnabled }" @click="toggleAlertSwitch">
                    <div class="switch-track-enhanced">
                      <div class="switch-thumb-enhanced"></div>
                    </div>
                    <span class="switch-label">实时报警</span>
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

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 10px;
  width: 100%;
  height: 100%;
}

.grid-item {
  min-height: 0;
  overflow: hidden;
}

.grid-item .border-box {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.grid-item .border-body {
  flex: 1;
  display: flex;
  min-height: 0;
}

.grid-item .content-area {
  flex: 1;
  overflow: hidden;
  padding: 4px;
  box-sizing: border-box;
}

.border-box {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, rgba(10, 20, 40, 0.95), rgba(15, 25, 50, 0.9));
  border-radius: 4px;
  overflow: visible;
  position: relative;
  border: 1px solid rgba(0, 191, 255, 0.15);
}

.border-top {
  display: flex;
  align-items: center;
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
  position: relative;
}

.title-bar {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  height: 100%;
}

.title-decoration.left,
.title-decoration.right {
  display: flex;
  align-items: center;
  gap: 4px;
}

.title-text {
  font-size: 14px;
  font-weight: 600;
  color: #00d4ff;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
  margin: 0;
  white-space: nowrap;
}

.decoration {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 100%;
  padding: 0 8px;
}

.decoration.left {
  padding-right: 8px;
}

.decoration.right {
  padding-left: 8px;
}

.d-block {
  width: 3px;
  height: 16px;
  background: linear-gradient(180deg, rgba(0, 191, 255, 0.6), rgba(102, 126, 234, 0.4));
  border-radius: 1px;
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

.deco-diamond {
  width: 6px;
  height: 6px;
  background: rgba(0, 191, 255, 0.6);
  transform: rotate(45deg);
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
  background: linear-gradient(180deg, transparent, rgba(0, 191, 255, 0.3), transparent);
}

.side-line.left {
  background: linear-gradient(180deg, transparent, rgba(0, 191, 255, 0.3) 20%, rgba(0, 191, 255, 0.3) 80%, transparent);
}

.side-line.right {
  background: linear-gradient(180deg, transparent, rgba(0, 191, 255, 0.3) 20%, rgba(0, 191, 255, 0.3) 80%, transparent);
}

.status-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
  overflow-y: auto;
  padding: 4px 0;
}

.status-header-compact {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 4px;
}

.gauge-mini {
  width: 90px;
  height: 70px;
  flex-shrink: 0;
}

.status-gauge {
  width: 100%;
  height: 100%;
}

.runtime-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.runtime-main {
  display: flex;
  flex-direction: column;
}

.runtime-label {
  font-size: 10px;
  color: #64748b;
  margin-bottom: 2px;
}

.runtime-value-row {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.runtime-value {
  font-size: 22px;
  font-weight: 700;
  color: #00d4ff;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
}

.runtime-unit {
  font-size: 11px;
  color: #64748b;
}

.runtime-stats {
  display: flex;
  gap: 8px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4px 8px;
  background: rgba(0, 191, 255, 0.06);
  border-radius: 4px;
  border: 1px solid rgba(0, 191, 255, 0.1);
}

.stat-value {
  font-size: 13px;
  font-weight: 600;
  color: #ff6b6b;
}

.stat-label {
  font-size: 8px;
  color: #64748b;
  margin-top: 2px;
}

.dimension-compact {
  display: flex;
  gap: 6px;
}

.dimension-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px 4px;
  background: rgba(0, 191, 255, 0.06);
  border-radius: 6px;
  border: 1px solid rgba(0, 191, 255, 0.12);
  transition: all 0.2s ease;
}

.dimension-card:hover {
  background: rgba(0, 191, 255, 0.1);
  border-color: rgba(0, 191, 255, 0.25);
}

.dimension-card.highlight {
  background: rgba(255, 107, 107, 0.08);
  border-color: rgba(255, 107, 107, 0.2);
}

.dimension-card.highlight .dimension-value {
  color: #ff6b6b;
}

.dimension-value {
  font-size: 14px;
  font-weight: 600;
  color: #00ff99;
  text-shadow: 0 0 6px rgba(0, 255, 153, 0.3);
}

.dimension-label {
  font-size: 9px;
  color: #64748b;
  margin-top: 3px;
}

.alarm-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.alarm-scroll-enhanced {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 4px;
}

.alarm-scroll-enhanced::-webkit-scrollbar {
  width: 8px;
}

.alarm-scroll-enhanced::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.alarm-scroll-enhanced::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #00d4ff, #667eea);
  border-radius: 4px;
  transition: all 0.2s ease;
}

.alarm-scroll-enhanced::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #00ffff, #8b5cf6);
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.5);
}

.alarm-scroll-enhanced::-webkit-scrollbar-corner {
  background: transparent;
}

.alarm-row-enhanced {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 4px;
  font-size: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.alarm-row-enhanced:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(0, 191, 255, 0.1);
}

.alarm-row-enhanced.warning {
  border-left: 3px solid #ffb800;
  background: rgba(255, 184, 0, 0.05);
}

.alarm-row-enhanced.error {
  border-left: 3px solid #ff4757;
  background: rgba(255, 71, 87, 0.05);
}

.alarm-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.alarm-row-enhanced.warning .alarm-indicator {
  background: #ffb800;
  box-shadow: 0 0 6px #ffb800;
}

.alarm-row-enhanced.error .alarm-indicator {
  background: #ff4757;
  box-shadow: 0 0 6px #ff4757;
}

.alarm-row-enhanced.info .alarm-indicator {
  background: #00d4ff;
  box-shadow: 0 0 6px #00d4ff;
}

.alarm-time {
  color: #64748b;
  min-width: 60px;
  font-size: 11px;
}

.alarm-subsystem {
  font-weight: 600;
  min-width: 65px;
  font-size: 11px;
}

.alarm-msg {
  flex: 1;
  color: #e2e8f0;
  font-size: 12px;
}

.alarm-level-badge {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 9px;
  font-weight: 600;
  flex-shrink: 0;
}

.alarm-level-badge.info {
  background: rgba(0, 191, 255, 0.15);
  color: #00d4ff;
}

.alarm-level-badge.warning {
  background: rgba(255, 184, 0, 0.15);
  color: #ffb800;
}

.alarm-level-badge.error {
  background: rgba(255, 71, 87, 0.15);
  color: #ff4757;
}

.alarm-actions-fixed {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  padding: 10px 0 4px 0;
  border-top: 1px solid rgba(0, 191, 255, 0.15);
  background: linear-gradient(180deg, rgba(15, 25, 50, 0.95), rgba(10, 20, 40, 0.98));
  margin-top: 4px;
}

.log-switch-enhanced {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  padding: 6px 10px;
  border-radius: 6px;
  transition: all 0.2s ease;
  background: rgba(0, 191, 255, 0.05);
  border: 1px solid rgba(0, 191, 255, 0.1);
}

.log-switch-enhanced:hover {
  background: rgba(0, 191, 255, 0.1);
  border-color: rgba(0, 191, 255, 0.25);
}

.switch-label {
  font-size: 11px;
  color: #94a3b8;
}

.switch-track-enhanced {
  width: 38px;
  height: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  position: relative;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}

.switch-thumb-enhanced {
  width: 16px;
  height: 16px;
  background: linear-gradient(135deg, #94a3b8, #64748b);
  border-radius: 50%;
  position: absolute;
  top: 1px;
  left: 1px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.log-switch-enhanced.active .switch-track-enhanced {
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.3), rgba(102, 126, 234, 0.3));
  border-color: rgba(0, 212, 255, 0.5);
}

.log-switch-enhanced.active .switch-thumb-enhanced {
  left: 19px;
  background: linear-gradient(135deg, #00d4ff, #00ff88);
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.6), 0 2px 4px rgba(0, 0, 0, 0.3);
}

.export-btn-enhanced {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.15), rgba(102, 126, 234, 0.15));
  border: 1px solid rgba(0, 191, 255, 0.35);
  padding: 7px 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 191, 255, 0.1);
}

.export-btn-enhanced:hover {
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.25), rgba(102, 126, 234, 0.25));
  border-color: rgba(0, 191, 255, 0.7);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 191, 255, 0.25);
}

.export-btn-enhanced:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 191, 255, 0.15);
}

.btn-icon {
  width: 16px;
  height: 16px;
  color: #00d4ff;
  filter: drop-shadow(0 0 4px rgba(0, 212, 255, 0.5));
}

.export-btn-enhanced span {
  font-size: 12px;
  color: #00d4ff;
  font-weight: 600;
  text-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
}

.motor-scroll-enhanced {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 4px;
}

.motor-scroll-enhanced::-webkit-scrollbar {
  width: 8px;
}

.motor-scroll-enhanced::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.motor-scroll-enhanced::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #00d4ff, #667eea);
  border-radius: 4px;
  transition: all 0.2s ease;
}

.motor-scroll-enhanced::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #00ffff, #8b5cf6);
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.5);
}

.motor-scroll-enhanced::-webkit-scrollbar-corner {
  background: transparent;
}

.motor-grid-enhanced {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.motor-card-enhanced {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.02));
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 8px;
  padding: 10px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.3s ease;
}

.motor-card-enhanced:hover {
  border-color: rgba(0, 191, 255, 0.4);
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.08), rgba(102, 126, 234, 0.04));
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 191, 255, 0.1);
}

.motor-gauge-wrapper {
  width: 60px;
  height: 60px;
  position: relative;
  margin-bottom: 6px;
}

.mini-gauge {
  width: 100%;
  height: 100%;
}

.gauge-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.gauge-value {
  font-size: 11px;
  font-weight: 700;
  color: #00d4ff;
  text-shadow: 0 0 8px rgba(0, 212, 255, 0.5);
}

.motor-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.motor-card-enhanced .motor-name {
  font-size: 11px;
  color: #e2e8f0;
  font-weight: 600;
  text-align: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 9px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 600;
}

.indicator-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
}

.status-running {
  background: rgba(0, 255, 153, 0.12);
  color: #00ff99;
}

.status-running .indicator-dot {
  background: #00ff99;
  box-shadow: 0 0 6px #00ff99;
}

.status-idle {
  background: rgba(148, 163, 184, 0.12);
  color: #94a3b8;
}

.status-idle .indicator-dot {
  background: #94a3b8;
}

.status-warning {
  background: rgba(255, 184, 0, 0.12);
  color: #ffb800;
}

.status-warning .indicator-dot {
  background: #ffb800;
  box-shadow: 0 0 6px #ffb800;
}

.status-error,
.status-stopped {
  background: rgba(255, 71, 87, 0.12);
  color: #ff4757;
}

.status-error .indicator-dot,
.status-stopped .indicator-dot {
  background: #ff4757;
  box-shadow: 0 0 6px #ff4757;
}

.motor-progress {
  width: 100%;
  margin-top: 6px;
}

.progress-track {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

.progress-fill.status-running {
  background: linear-gradient(90deg, #00ff99, #00d4ff);
  box-shadow: 0 0 8px rgba(0, 255, 153, 0.5);
}

.progress-fill.status-idle {
  background: linear-gradient(90deg, #94a3b8, #64748b);
}

.progress-fill.status-warning {
  background: linear-gradient(90deg, #ffb800, #ff8c00);
  box-shadow: 0 0 8px rgba(255, 184, 0, 0.5);
}

.progress-fill.status-error,
.progress-fill.status-stopped {
  background: linear-gradient(90deg, #ff4757, #ff6b6b);
  box-shadow: 0 0 8px rgba(255, 71, 87, 0.5);
}

.health-content-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
  border-radius: 12px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.health-content-wrapper:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%);
}

.health-gauge-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.health-gauge {
  width: 100%;
  height: 100%;
  min-height: 200px;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.2));
  transition: filter 0.3s ease;
}

.health-gauge:hover {
  filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.25));
}

.health-legend {
  position: absolute;
  top: 8px;
  right: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  backdrop-filter: blur(4px);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: rgba(236, 240, 241, 0.85);
  white-space: nowrap;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  flex-shrink: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.legend-text {
  font-weight: 500;
  letter-spacing: 0.5px;
}

.subsystem-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding: 4px;
}

.subsystem-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.subsystem-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.subsystem-running .subsystem-indicator {
  background: #00ff99;
  box-shadow: 0 0 8px #00ff99;
}

.subsystem-warning .subsystem-indicator {
  background: #ffb800;
  box-shadow: 0 0 8px #ffb800;
}

.subsystem-stopped .subsystem-indicator {
  background: #ff4757;
  box-shadow: 0 0 8px #ff4757;
}

.subsystem-name {
  flex: 1;
  font-size: 12px;
  color: #e2e8f0;
}

.subsystem-status {
  font-size: 11px;
  font-weight: 600;
}

.subsystem-running .subsystem-status {
  color: #00ff99;
}

.subsystem-warning .subsystem-status {
  color: #ffb800;
}

.subsystem-stopped .subsystem-status {
  color: #ff4757;
}

.trend-content-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.trend-chart-ref {
  flex: 1;
  min-height: 0;
  width: 100%;
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

.pie-stats {
  display: flex;
  justify-content: space-around;
  padding: 10px 16px;
  background: rgba(56, 189, 248, 0.05);
  border-radius: 8px;
  margin-bottom: 10px;
  border: 1px solid rgba(56, 189, 248, 0.1);
}

.pie-stats .stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
}

.pie-stats .stat-item:not(:last-child) {
  border-right: 1px solid rgba(148, 163, 184, 0.15);
}

.pie-stats .stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #38bdf8;
  text-shadow: 0 0 8px rgba(56, 189, 248, 0.3);
}

.pie-stats .stat-label {
  font-size: 10px;
  color: #94a3b8;
  font-weight: 400;
}

.pie-stats .stat-item.highlight .stat-value {
  color: #ef4444;
  text-shadow: 0 0 8px rgba(239, 68, 68, 0.3);
}

.pie-stats .stat-item.warning .stat-value {
  color: #f59e0b;
  text-shadow: 0 0 8px rgba(245, 158, 11, 0.3);
}

.pie-stats .stat-item.normal .stat-value {
  color: #10b981;
  text-shadow: 0 0 8px rgba(16, 185, 129, 0.3);
}

.pie-content {
  flex: 1;
  width: 100%;
  height: 100%;
  min-height: 200px;
  display: flex;
  gap: 16px;
  align-items: stretch;
}

.pie-chart-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 150px;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 8px;
  border: 1px solid rgba(56, 189, 248, 0.08);
}

.pie-chart {
  width: 100%;
  height: 100%;
  min-height: 160px;
}

.pie-legend-panel {
  width: 130px;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-radius: 8px;
  padding: 12px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.pie-legend-panel .legend-title {
  font-size: 11px;
  color: #94a3b8;
  text-align: center;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  margin-bottom: 8px;
  flex-shrink: 0;
}

.pie-legend-panel .legend-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 4px 2px;
  scroll-behavior: smooth;
}

.pie-legend-panel .legend-list::-webkit-scrollbar {
  width: 4px;
}

.pie-legend-panel .legend-list::-webkit-scrollbar-track {
  background: rgba(148, 163, 184, 0.05);
  border-radius: 2px;
}

.pie-legend-panel .legend-list::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.25);
  border-radius: 2px;
}

.pie-legend-panel .legend-list::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.4);
}

.pie-legend-panel .legend-list::-webkit-scrollbar-corner {
  background: transparent;
}

.pie-legend-panel .legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 3px 6px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.pie-legend-panel .legend-item:hover {
  background: rgba(56, 189, 248, 0.1);
}

.pie-legend-panel .legend-color {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  flex-shrink: 0;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
}

.pie-legend-panel .legend-name {
  flex: 1;
  font-size: 11px;
  color: #cbd5e1;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pie-legend-panel .legend-value {
  font-size: 11px;
  color: #38bdf8;
  font-weight: 600;
  flex-shrink: 0;
}

@media (max-width: 1400px) {
  .grid-container {
    gap: 8px;
  }
  
  .status-header-compact {
    flex-direction: column;
    gap: 8px;
  }
  
  .dimension-compact {
    flex-wrap: wrap;
  }
  
  .motor-grid-enhanced {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1100px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(3, 1fr);
  }
  
  .pie-content {
    flex-direction: column;
  }
  
  .pie-chart-wrapper {
    width: 100%;
    min-height: 180px;
  }
  
  .pie-legend-panel {
    width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .view {
    padding: 6px;
  }
  
  .grid-container {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(6, auto);
    gap: 6px;
  }
  
  .grid-item {
    min-height: 200px;
  }
  
  .status-header-compact {
    flex-direction: row;
  }
  
  .dimension-compact {
    flex-wrap: nowrap;
  }
  
  .motor-grid-enhanced {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .alarm-scroll-enhanced {
    max-height: 200px;
  }
}
</style>
