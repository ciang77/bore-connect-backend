<script setup lang="ts">
</script>

<template>
  <div class="view">
    <div class="placeholder">
      <span class="placeholder-icon">◆</span>
      <h2 class="placeholder-title">智能分析</h2>
      <p class="placeholder-sub">SMART ANALYSIS</p>
    </div>
  </div>
</template>

<style scoped>
.view {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder {
  text-align: center;
  opacity: 0.5;
}

.placeholder-icon {
  font-size: 48px;
  color: #00e5ff;
  text-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
}

.placeholder-title {
  font-size: 24px;
  font-weight: 700;
  color: rgba(225, 240, 255, 0.7);
  letter-spacing: 4px;
  margin-top: 16px;
}

.placeholder-sub {
  font-size: 12px;
  letter-spacing: 2px;
  color: rgba(150, 200, 230, 0.4);
  margin-top: 8px;
}
</style>
