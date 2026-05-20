<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const data = [
  { name: '电气类故障', value: 35 },
  { name: '机械类故障', value: 28 },
  { name: '液压类故障', value: 25 },
]

const colors = ['#00e5ff', '#667eea', '#a78bfa']

function initChart() {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(10, 14, 39, 0.9)',
      borderColor: 'rgba(0, 180, 255, 0.3)',
      textStyle: { color: '#e0e6f0', fontFamily: 'Microsoft YaHei' },
      formatter: (p: any) => `${p.name}<br/>数量：${p.value}　占比：${p.percent}%`,
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '68%'],
        center: ['50%', '52%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 6,
          borderColor: 'rgba(10, 14, 39, 0.8)',
          borderWidth: 3,
        },
        label: {
          show: true,
          color: 'rgba(200, 215, 240, 0.8)',
          fontSize: 13,
          fontFamily: 'Microsoft YaHei',
          formatter: '{b}\n{d}%',
          lineHeight: 20,
        },
        labelLine: {
          show: true,
          length: 16,
          length2: 24,
          lineStyle: {
            color: 'rgba(0, 180, 255, 0.3)',
            width: 1,
          },
        },
        emphasis: {
          scaleSize: 8,
          itemStyle: {
            shadowBlur: 20,
            shadowColor: 'rgba(0, 180, 255, 0.4)',
          },
        },
        data: data.map((d, i) => ({
          ...d,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
              { offset: 0, color: colors[i] },
              { offset: 1, color: colors[i] + '66' },
            ]),
          },
        })),
      },
      // 外圈装饰环
      {
        type: 'pie',
        radius: ['72%', '74%'],
        center: ['50%', '52%'],
        silent: true,
        label: { show: false },
        data: [{ value: 1, itemStyle: { color: 'rgba(0, 180, 255, 0.08)' } }],
      },
    ],
  }

  chart.setOption(option)
}

function handleResize() {
  chart?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})
onUnmounted(() => {
  chart?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div class="chart-card">
    <div class="card-header">
      <div class="card-header-deco"></div>
      <span class="card-title">故障类型分布</span>
      <span class="card-total">合计 <em>88</em> 次</span>
    </div>
    <div ref="chartRef" class="chart-body"></div>
  </div>
</template>

<style scoped>
.chart-card {
  background: rgba(10, 14, 39, 0.6);
  border: 1px solid rgba(0, 180, 255, 0.12);
  border-radius: 12px;
  overflow: hidden;
  backdrop-filter: blur(8px);
}
.card-header {
  display: flex;
  align-items: center;
  padding: 14px 18px;
  border-bottom: 1px solid rgba(0, 180, 255, 0.08);
  position: relative;
}
.card-header-deco {
  width: 3px;
  height: 16px;
  background: linear-gradient(180deg, #00e5ff, #667eea);
  border-radius: 2px;
  margin-right: 10px;
  flex-shrink: 0;
}
.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #e0e6f0;
  letter-spacing: 1px;
}
.card-total {
  margin-left: auto;
  font-size: 13px;
  color: rgba(200, 215, 240, 0.5);
}
.card-total em {
  font-style: normal;
  color: #00e5ff;
  font-weight: 700;
  font-size: 15px;
}
.chart-body {
  width: 100%;
  height: 280px;
}
</style>
