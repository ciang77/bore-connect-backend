<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'

interface SubsystemMetrics {
  label: string
  value: string
  unit: string
}

interface SubsystemInfo {
  name: string
  nameEn?: string
  icon?: string
  status: 'normal' | 'warning' | 'fault' | 'running' | 'stopped'
  healthScore?: number
  metrics?: SubsystemMetrics[]
}

const props = defineProps<{
  subsystemData?: SubsystemInfo[]
}>()

const subsystems = ref<SubsystemInfo[]>([
  {
    name: '主轴系统', nameEn: 'SPINDLE',
    icon: 'spindle', status: 'normal', healthScore: 92,
    metrics: [
      { label: '振动监测', value: '3.20', unit: 'mm/s' },
      { label: '温度监测', value: '52.80', unit: '°C' },
      { label: '电流监测', value: '45.60', unit: 'A' },
      { label: '转速监测', value: '3200', unit: 'RPM' },
    ],
  },
  {
    name: '进给系统', nameEn: 'FEED',
    icon: 'feed', status: 'normal', healthScore: 88,
    metrics: [
      { label: '伺服电流', value: '12.30', unit: 'A' },
      { label: '跟随误差', value: '0.02', unit: 'mm' },
      { label: '位置误差', value: '0.01', unit: 'mm' },
      { label: '振动状态', value: '1.80', unit: 'mm/s' },
    ],
  },
  {
    name: '液压系统', nameEn: 'HYDRAULIC',
    icon: 'hydraulic', status: 'normal', healthScore: 90,
    metrics: [
      { label: '系统压力', value: '16.50', unit: 'MPa' },
      { label: '液压流量', value: '24.60', unit: 'L/min' },
      { label: '响应速度', value: '0.12', unit: 's' },
    ],
  },
  {
    name: '润滑系统', nameEn: 'LUBRICATION',
    icon: 'lube', status: 'warning', healthScore: 72,
    metrics: [
      { label: '润滑压力', value: '0.45', unit: 'MPa' },
      { label: '供油流量', value: '2.80', unit: 'L/min' },
      { label: '油液品质', value: '82', unit: '%' },
    ],
  },
])

let updateTimer: ReturnType<typeof setInterval> | undefined

function updateData() {
  // 主轴系统
  if (subsystems.value[0]?.metrics?.[0]) subsystems.value[0].metrics[0].value = (2.5 + Math.random() * 2.5).toFixed(2)
  if (subsystems.value[0]?.metrics?.[1]) subsystems.value[0].metrics[1].value = (48 + Math.random() * 10).toFixed(2)
  if (subsystems.value[0]?.metrics?.[2]) subsystems.value[0].metrics[2].value = (38 + Math.random() * 20).toFixed(2)
  if (subsystems.value[0]?.metrics?.[3]) subsystems.value[0].metrics[3].value = Math.floor(2800 + Math.random() * 1200).toString()

  // 进给系统
  if (subsystems.value[1]?.metrics?.[0]) subsystems.value[1].metrics[0].value = (10 + Math.random() * 6).toFixed(2)
  if (subsystems.value[1]?.metrics?.[1]) subsystems.value[1].metrics[1].value = (Math.random() * 0.05).toFixed(2)
  if (subsystems.value[1]?.metrics?.[2]) subsystems.value[1].metrics[2].value = (Math.random() * 0.03).toFixed(2)
  if (subsystems.value[1]?.metrics?.[3]) subsystems.value[1].metrics[3].value = (1.2 + Math.random() * 1.8).toFixed(2)

  // 液压系统
  if (subsystems.value[2]?.metrics?.[0]) subsystems.value[2].metrics[0].value = (14.5 + Math.random() * 4).toFixed(2)
  if (subsystems.value[2]?.metrics?.[1]) subsystems.value[2].metrics[1].value = (22 + Math.random() * 6).toFixed(2)
  if (subsystems.value[2]?.metrics?.[2]) subsystems.value[2].metrics[2].value = (0.08 + Math.random() * 0.1).toFixed(2)

  // 润滑系统
  if (subsystems.value[3]?.metrics?.[0]) subsystems.value[3].metrics[0].value = (0.3 + Math.random() * 0.3).toFixed(2)
  if (subsystems.value[3]?.metrics?.[1]) subsystems.value[3].metrics[1].value = (2.2 + Math.random() * 1.6).toFixed(2)
  if (subsystems.value[3]?.metrics?.[2]) subsystems.value[3].metrics[2].value = Math.floor(70 + Math.random() * 25).toString()

  subsystems.value.forEach((sub) => {
    if (sub.healthScore !== undefined) {
      sub.healthScore = Math.max(45, Math.min(98, sub.healthScore + Math.floor((Math.random() - 0.5) * 3)))
    }
    const r = Math.random()
    if (r < 0.04) sub.status = 'fault'
    else if (r < 0.12) sub.status = 'warning'
    else if (r < 0.84) sub.status = 'normal'
  })
}

function useExternalData() {
  if (props.subsystemData && props.subsystemData.length > 0) {
    subsystems.value = props.subsystemData.map(sub => ({
      ...sub,
      status: sub.status === 'running' ? 'normal' : sub.status === 'stopped' ? 'fault' : sub.status as 'normal' | 'warning' | 'fault',
      healthScore: sub.healthScore ?? Math.floor(60 + Math.random() * 30),
      metrics: sub.metrics ?? [
        { label: '运行状态', value: sub.status === 'running' ? '正常' : sub.status === 'warning' ? '预警' : '停止', unit: '' }
      ]
    }))
  }
}

onMounted(() => {
  useExternalData()
  if (!props.subsystemData || props.subsystemData.length === 0) {
    updateTimer = setInterval(updateData, 3000)
  }
})

watch(() => props.subsystemData, () => {
  useExternalData()
}, { deep: true })

onUnmounted(() => {
  if (updateTimer) clearInterval(updateTimer)
})
</script>

<template>
  <div class="subsystem-status-inner">
    <div class="subsystem-grid">
      <div
        v-for="sub in subsystems"
        :key="sub.name"
        class="subsystem-card-item"
        :class="'subsystem-card--' + sub.status"
      >
        <div class="sub-card-top">
          <div class="sub-card-title-row">
            <span class="sub-card-status-light" :class="'light-' + sub.status"></span>
            <span class="sub-card-name">{{ sub.name }}</span>
            <span class="sub-card-status-tag" :class="'substatus-' + sub.status">
              {{ sub.status === 'normal' || sub.status === 'running' ? '正常' : sub.status === 'warning' ? '预警' : '故障' }}
            </span>
          </div>
          <div class="sub-card-health">
            <span class="sub-health-label">健康评分</span>
            <span class="sub-health-score" :class="'health-' + sub.status">{{ sub.healthScore }}</span>
          </div>
        </div>
        <div class="sub-card-params">
          <template v-for="m in (sub.metrics || [])" :key="m.label">
            <span class="sub-param-label">{{ m.label }}</span>
            <span class="sub-param-value">
              {{ m.value }}<small class="sub-param-unit">{{ m.unit }}</small>
            </span>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.subsystem-status-inner {
  width: 100%;
  height: 100%;
}

.subsystem-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 4px;
  height: 100%;
  padding: 2px;
}

.subsystem-card-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 4px 6px;
  border-radius: 4px;
  background: rgba(0, 100, 200, 0.05);
  border: 1px solid rgba(0, 140, 255, 0.12);
  transition: all 0.3s ease;
  cursor: default;
  position: relative;
  overflow: hidden;
  min-height: 0;
}

.subsystem-card-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 4px;
  bottom: 4px;
  width: 2px;
  border-radius: 0 2px 2px 0;
  transition: all 0.3s ease;
}

.subsystem-card-item.subsystem-card--normal::before,
.subsystem-card-item.subsystem-card--running::before {
  background: #69f0ae;
  box-shadow: 0 0 6px rgba(105, 240, 174, 0.4);
}
.subsystem-card-item.subsystem-card--warning::before {
  background: #ffab40;
  box-shadow: 0 0 6px rgba(255, 171, 64, 0.4);
}
.subsystem-card-item.subsystem-card--fault::before,
.subsystem-card-item.subsystem-card--stopped::before {
  background: #ff5252;
  box-shadow: 0 0 6px rgba(255, 82, 82, 0.5);
  animation: fault-pulse 0.6s ease-in-out infinite;
}

.sub-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.sub-card-title-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.sub-card-status-light {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.light-normal,
.light-running { background: #69f0ae; box-shadow: 0 0 6px rgba(105, 240, 174, 0.6); }
.light-warning { background: #ffab40; box-shadow: 0 0 6px rgba(255, 171, 64, 0.6); animation: pulse-dot 1.8s ease-in-out infinite; }
.light-fault,
.light-stopped { background: #ff5252; box-shadow: 0 0 6px rgba(255, 82, 82, 0.6); animation: fault-pulse 0.6s ease-in-out infinite; }

.sub-card-name {
  font-size: 17px;
  font-weight: 700;
  color: rgba(225, 240, 255, 0.93);
  white-space: nowrap;
}

.sub-card-status-tag {
  font-size: 12px;
  padding: 1px 4px;
  border-radius: 4px;
  font-weight: 600;
  white-space: nowrap;
}

.substatus-normal,
.substatus-running { background: rgba(105, 240, 174, 0.13); color: #69f0ae; border: 1px solid rgba(105, 240, 174, 0.25); }
.substatus-warning { background: rgba(255, 171, 64, 0.13); color: #ffab40; border: 1px solid rgba(255, 171, 64, 0.25); }
.substatus-fault,
.substatus-stopped { background: rgba(255, 82, 82, 0.13); color: #ff5252; border: 1px solid rgba(255, 82, 82, 0.25); animation: danger-blink 1s ease-in-out infinite; }

.sub-card-health {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0;
}

.sub-health-label {
  font-size: 10px;
  color: rgba(150, 200, 230, 0.5);
}

.sub-health-score {
  font-size: 16px;
  font-weight: 700;
}

.health-normal,
.health-running { color: #69f0ae; text-shadow: 0 0 8px rgba(105, 240, 174, 0.35); }
.health-warning { color: #ffab40; text-shadow: 0 0 8px rgba(255, 171, 64, 0.35); }
.health-fault,
.health-stopped { color: #ff5252; text-shadow: 0 0 8px rgba(255, 82, 82, 0.4); }

.sub-card-params {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px 8px;
  align-content: center;
}

.sub-param-label {
  font-size: 12px;
  color: rgba(160, 210, 235, 0.65);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sub-param-value {
  font-size: 13px;
  font-weight: 700;
  color: rgba(225, 245, 255, 0.94);
  white-space: nowrap;
}

.sub-param-unit {
  font-size: 10px;
  font-weight: 400;
  color: rgba(170, 210, 235, 0.5);
  margin-left: 1px;
}

@keyframes fault-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@keyframes danger-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
