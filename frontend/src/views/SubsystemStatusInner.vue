<script setup lang="ts">
import { useSubsystemData } from '../composables/useSubsystemData'

const { subsystems } = useSubsystemData()
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
              {{ sub.status === 'normal' ? '正常' : sub.status === 'warning' ? '预警' : '故障' }}
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
