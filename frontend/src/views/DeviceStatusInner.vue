<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { fetchDeviceStatus, type DeviceStatus } from '../api/overview'
import { useEventSource } from '../composables/useEventSource'

type DeviceState = 'online' | 'warning' | 'stopped'

const deviceStatus = ref<DeviceStatus>({
  name: '',
  model: '',
  status: 'online',
  runtime: '',
  temperature: '',
  vibration: '',
  pressure: '',
  spindleSpeed: '',
  servoCurrent: '',
})

const statusText = computed(() => {
  switch (deviceStatus.value.status) {
    case 'online':
      return '在线'
    case 'warning':
      return '预警'
    case 'stopped':
      return '停机'
  }
})

async function loadData() {
  try {
    const res = await fetchDeviceStatus()
    if (res.code === 0 && res.data) {
      deviceStatus.value = res.data
    }
  } catch {
    // 接口失败保持上次数据
  }
}

// SSE 必须在 setup 同步阶段注册，不能放在 onMounted 的 await 之后
useEventSource<DeviceStatus>('/api/overview/device-status/stream', (data) => {
  deviceStatus.value = data
})

onMounted(async () => {
  // 首屏快速加载走 REST
  await loadData()
})
</script>

<template>
  <div class="device-status-inner">
    <div class="status-lamp-panel" :class="'lamp-' + deviceStatus.status">
      <div class="status-lamp" aria-hidden="true">
        <div class="lamp-core"></div>
        <div class="lamp-glow"></div>
      </div>
      <div class="lamp-label">{{ statusText }}</div>
    </div>

    <div class="device-main">
      <div class="device-info">
        <div class="device-name-row">
          <span class="device-name">{{ deviceStatus.name }}</span>
          <span class="device-model">{{ deviceStatus.model }}</span>
        </div>
        <div class="device-status-tag" :class="'status-' + deviceStatus.status">
          {{ statusText }}
        </div>
      </div>

      <div class="device-metrics">
        <div class="metric-item">
          <span class="metric-label">运行时长</span>
          <span class="metric-value">{{ deviceStatus.runtime }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">主轴转速</span>
          <span class="metric-value">{{ deviceStatus.spindleSpeed }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">伺服电流</span>
          <span class="metric-value">{{ deviceStatus.servoCurrent }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">设备温度</span>
          <span class="metric-value">{{ deviceStatus.temperature }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">振动值</span>
          <span class="metric-value">{{ deviceStatus.vibration }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">系统压力</span>
          <span class="metric-value">{{ deviceStatus.pressure }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.device-status-inner {
  width: 100%;
  height: 100%;
  padding: 8px;
  display: flex;
  gap: 10px;
}

.status-lamp-panel {
  width: 92px;
  min-width: 92px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-radius: 12px;
  border: 1px solid rgba(0, 140, 255, 0.12);
  background: radial-gradient(circle at 30% 20%, rgba(56, 189, 248, 0.10), rgba(0, 0, 0, 0.18));
}

.status-lamp {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  position: relative;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.10);
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.6);
}

.lamp-core {
  position: absolute;
  inset: 7px;
  border-radius: 50%;
  background: rgba(148, 163, 184, 0.25);
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.45);
}

.lamp-glow {
  position: absolute;
  inset: -10px;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.25s ease;
}

.lamp-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  color: rgba(226, 232, 240, 0.9);
}

.lamp-online .lamp-core {
  background: radial-gradient(circle at 30% 30%, rgba(0, 255, 153, 0.95), rgba(0, 255, 153, 0.15));
}

.lamp-online .lamp-glow {
  opacity: 1;
  background: radial-gradient(circle, rgba(0, 255, 153, 0.38), rgba(0, 255, 153, 0));
  animation: lamp-pulse 2s ease-in-out infinite;
}

.lamp-warning .lamp-core {
  background: radial-gradient(circle at 30% 30%, rgba(255, 184, 0, 0.95), rgba(255, 184, 0, 0.12));
}

.lamp-warning .lamp-glow {
  opacity: 1;
  background: radial-gradient(circle, rgba(255, 184, 0, 0.35), rgba(255, 184, 0, 0));
  animation: lamp-pulse 1.6s ease-in-out infinite;
}

.lamp-stopped .lamp-core {
  background: radial-gradient(circle at 30% 30%, rgba(255, 71, 87, 0.95), rgba(255, 71, 87, 0.12));
}

.lamp-stopped .lamp-glow {
  opacity: 1;
  background: radial-gradient(circle, rgba(255, 71, 87, 0.32), rgba(255, 71, 87, 0));
  animation: lamp-alert 0.8s ease-in-out infinite;
}

.device-main {
  flex: 1;
  min-width: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.device-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(0, 100, 200, 0.05);
  border: 1px solid rgba(0, 140, 255, 0.12);
  border-radius: 8px;
}

.device-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.device-name {
  font-size: 16px;
  font-weight: 700;
  color: rgba(225, 240, 255, 0.95);
  letter-spacing: 1px;
}

.device-model {
  font-size: 12px;
  color: rgba(150, 200, 230, 0.5);
  letter-spacing: 0.5px;
}

.device-status-tag {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 6px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.status-online {
  background: rgba(0, 255, 153, 0.14);
  color: #00ff99;
  border: 1px solid rgba(0, 255, 153, 0.22);
}

.status-warning {
  background: rgba(255, 184, 0, 0.14);
  color: #ffb800;
  border: 1px solid rgba(255, 184, 0, 0.22);
}

.status-stopped {
  background: rgba(255, 71, 87, 0.14);
  color: #ff4757;
  border: 1px solid rgba(255, 71, 87, 0.22);
}

.device-metrics {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  padding: 0;
}

.metric-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 10px;
  background: rgba(0, 100, 200, 0.03);
  border: 1px solid rgba(0, 140, 255, 0.08);
  border-radius: 6px;
}

.metric-label {
  font-size: 11px;
  color: rgba(160, 210, 235, 0.65);
  letter-spacing: 0.5px;
}

.metric-value {
  font-size: 16px;
  font-weight: 700;
  color: rgba(225, 245, 255, 0.95);
  letter-spacing: 0.5px;
}

@keyframes lamp-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.92); opacity: 0.65; }
}

@keyframes lamp-alert {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.86); opacity: 0.55; }
}

@media (max-width: 1400px) {
  .status-lamp-panel {
    width: 84px;
    min-width: 84px;
  }

  .device-metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
