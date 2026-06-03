<template>
  <div class="border-box">
    <!-- 顶部装饰栏 -->
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
        <h2 class="title-text">{{ title }}</h2>
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
    
    <!-- 主体内容区 -->
    <div class="border-body">
      <div class="side-line left"></div>
      <div class="content-wrapper">
        <div class="content-left">
          <div class="equipment-info">
            <div class="info-item">
              <span class="info-label">设备型号</span>
              <span class="info-value">BM-2024</span>
            </div>
            <div class="info-item">
              <span class="info-label">类 型</span>
              <span class="info-value">数控主轴</span>
            </div>
          </div>
          <div class="equipment-image">
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="spindleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#4a90d9;stop-opacity:1" />
                  <stop offset="50%" style="stop-color:#2176c7;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#1e5aa8;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="innerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#2d5a87;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#1a3a5c;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#6ab0e8;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#4a90d9;stop-opacity:1" />
                </linearGradient>
                <filter id="glow">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                  <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>
              
              <circle cx="100" cy="100" r="85" fill="none" stroke="url(#accentGradient)" stroke-width="2" opacity="0.3"/>
              <circle cx="100" cy="100" r="75" fill="url(#innerGradient)" stroke="url(#spindleGradient)" stroke-width="3" filter="url(#glow)"/>
              
              <circle cx="100" cy="100" r="55" fill="none" stroke="url(#accentGradient)" stroke-width="2" opacity="0.6"/>
              <circle cx="100" cy="100" r="45" fill="url(#spindleGradient)" stroke="#6ab0e8" stroke-width="2"/>
              
              <circle cx="100" cy="100" r="30" fill="none" stroke="#6ab0e8" stroke-width="2" opacity="0.8"/>
              <circle cx="100" cy="100" r="20" fill="url(#innerGradient)" stroke="url(#accentGradient)" stroke-width="2"/>
              
              <circle cx="100" cy="100" r="8" fill="#6ab0e8" filter="url(#glow)"/>
              
              <line x1="100" y1="15" x2="100" y2="35" stroke="url(#accentGradient)" stroke-width="3" stroke-linecap="round"/>
              <line x1="100" y1="165" x2="100" y2="185" stroke="url(#accentGradient)" stroke-width="3" stroke-linecap="round"/>
              <line x1="15" y1="100" x2="35" y2="100" stroke="url(#accentGradient)" stroke-width="3" stroke-linecap="round"/>
              <line x1="165" y1="100" x2="185" y2="100" stroke="url(#accentGradient)" stroke-width="3" stroke-linecap="round"/>
              
              <line x1="45" y1="45" x2="60" y2="60" stroke="#6ab0e8" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
              <line x1="140" y1="140" x2="155" y2="155" stroke="#6ab0e8" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
              <line x1="155" y1="45" x2="140" y2="60" stroke="#6ab0e8" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
              <line x1="45" y1="155" x2="60" y2="140" stroke="#6ab0e8" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
              
              <rect x="85" y="70" width="30" height="60" rx="3" fill="url(#innerGradient)" stroke="url(#spindleGradient)" stroke-width="1.5" opacity="0.9"/>
              <rect x="90" y="80" width="20" height="40" rx="2" fill="none" stroke="#6ab0e8" stroke-width="1" opacity="0.7"/>
              <circle cx="100" cy="85" r="4" fill="#6ab0e8" opacity="0.8"/>
              <circle cx="100" cy="95" r="4" fill="#6ab0e8" opacity="0.8"/>
              <circle cx="100" cy="105" r="4" fill="#6ab0e8" opacity="0.8"/>
              
              <text x="100" y="160" text-anchor="middle" fill="#6ab0e8" font-size="10" font-family="Arial" opacity="0.7">SPINDLE</text>
            </svg>
          </div>
        </div>
        <div class="content-center">
          <div class="rated-section">
            <div class="rated-header">
              <div class="header-decoration left">
                <div class="header-line"></div>
                <div class="header-dot"></div>
              </div>
              <span class="rated-title">额定参数</span>
              <div class="header-decoration right">
                <div class="header-dot"></div>
                <div class="header-line"></div>
              </div>
            </div>
            <div class="rated-content">
              <div class="rated-item" v-for="(item, index) in ratedParams" :key="index">
                <span class="rated-label">{{ item.label }}</span>
                <span class="rated-value">{{ item.value }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="content-right">
          <div class="status-section">
            <div class="status-content">
              <div class="status-item" v-for="(item, index) in statusVariables" :key="index">
                <span class="status-label">{{ item.label }}</span>
                <div class="status-indicator" :class="item.value === 1 ? 'active-green' : 'active-red'">
                  <div class="indicator-inner"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="side-line right"></div>
    </div>
    
    <!-- 底部装饰栏 -->
    <div class="border-bottom">
      <div class="corner bottom-left"></div>
      <div class="bottom-center"></div>
      <div class="corner bottom-right"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SystemArea',
  props: {
    title: {
      type: String,
      required: true
    },
    ratedParams: {
      type: Array,
      default: () => []
    },
    statusVariables: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.border-box {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, rgba(10, 20, 40, 0.8), rgba(15, 25, 50, 0.6));
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 
    0 0 20px rgba(0, 191, 255, 0.2),
    inset 0 0 40px rgba(0, 191, 255, 0.03);
}

/* 顶部装饰栏 */
.border-top {
  display: flex;
  align-items: center;
  height: 28px;
  flex-shrink: 0;
  background: linear-gradient(180deg,
    rgba(0, 100, 150, 0.2) 0%,
    rgba(0, 80, 130, 0.15) 50%,
    rgba(0, 60, 110, 0.1) 100%);
  border-bottom: 1px solid rgba(0, 191, 255, 0.15);
}

.corner {
  width: 35px;
  height: 100%;
  position: relative;
}

.top-left::before,
.top-left::after,
.top-right::before,
.top-right::after {
  content: '';
  position: absolute;
  border: 2px solid #00bfff;
  border-radius: 4px;
}

.top-left::before {
  top: 4px;
  left: 4px;
  width: 10px;
  height: 10px;
  border-right: none;
  border-bottom: none;
}

.top-left::after {
  bottom: 4px;
  left: 4px;
  width: 10px;
  height: 10px;
  border-right: none;
  border-top: none;
}

.top-right::before {
  top: 4px;
  right: 4px;
  width: 10px;
  height: 10px;
  border-left: none;
  border-bottom: none;
}

.top-right::after {
  bottom: 4px;
  right: 4px;
  width: 10px;
  height: 10px;
  border-left: none;
  border-top: none;
}

.decoration {
  display: flex;
  gap: 6px;
  padding: 0 10px;
}

.decoration.right {
  transform: scaleX(-1);
}

.d-block {
  width: 14px;
  height: 6px;
  background: linear-gradient(90deg, rgba(0, 191, 255, 0.9), rgba(0, 191, 255, 0.3));
  clip-path: polygon(0 50%, 20% 0, 100% 0, 80% 50%, 100% 100%, 20% 100%);
}

.title-bar {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 2px 20px;
  min-width: 0;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(0, 120, 180, 0.1) 20%, 
    rgba(0, 140, 200, 0.15) 50%, 
    rgba(0, 120, 180, 0.1) 80%, 
    transparent 100%);
  border-radius: 6px;
}

.title-decoration {
  display: flex;
  align-items: center;
  gap: 5px;
}

.title-decoration.left {
  flex-direction: row;
}

.title-decoration.right {
  flex-direction: row;
}

.deco-wave {
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.8), rgba(0, 100, 180, 0.6));
  clip-path: polygon(0 50%, 30% 0%, 70% 0%, 100% 50%, 70% 100%, 30% 100%);
  box-shadow: 0 0 8px rgba(0, 191, 255, 0.6);
}

.deco-dot {
  width: 5px;
  height: 5px;
  background: #00e5ff;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(0, 229, 255, 0.9);
}

.deco-line {
  width: 18px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00bfff, transparent);
  border-radius: 1px;
}

.deco-diamond {
  width: 7px;
  height: 7px;
  background: #00bfff;
  transform: rotate(45deg);
  box-shadow: 0 0 10px rgba(0, 191, 255, 1);
}

.title-text {
  color: #87ceeb;
  font-size: 16px;
  font-weight: 700;
  text-align: center;
  text-shadow:
    0 0 6px rgba(135, 206, 235, 0.5),
    0 1px 2px rgba(0, 0, 0, 0.4);
  letter-spacing: 2px;
  padding: 2px 12px;
  white-space: nowrap;
}

/* 主体内容区 */
.border-body {
  flex: 1;
  display: flex;
  padding: 4px 6px;
  gap: 6px;
  min-height: 0;
  overflow: hidden;
}

.side-line {
  width: 4px;
  position: relative;
}

.side-line::before,
.side-line::after {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 16px;
  background: linear-gradient(180deg, #00bfff, transparent);
}

.side-line::before {
  top: 0;
}

.side-line::after {
  bottom: 0;
  transform: translateX(-50%) rotate(180deg);
}

.content-wrapper {
  flex: 1;
  display: flex;
  gap: 10px;
  min-height: 0;
}

.content-left {
  flex: 0.6;
  display: flex;
  flex-direction: column;
  background: transparent;
  overflow: hidden;
  min-height: 0;
}

.equipment-info {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 4px 6px;
  justify-content: center;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 3px 5px;
  background: rgba(0, 100, 180, 0.08);
  border-radius: 3px;
}

.info-label {
  font-size: 12px;
  color: rgba(180, 210, 240, 0.7);
}

.info-value {
  font-size: 12px;
  font-weight: 600;
  color: #a8d8ff;
  text-shadow: 0 0 4px rgba(168, 216, 255, 0.4);
}

.equipment-image {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2px;
  overflow: hidden;
}

.equipment-image svg {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
}

.content-center {
  flex: 1;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.rated-section {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
  border-radius: 8px;
  border: 1px solid rgba(0, 191, 255, 0.15);
  overflow: hidden;
  transition: all 0.3s ease;
}

.rated-section:hover {
  border-color: rgba(0, 191, 255, 0.3);
  box-shadow: 0 0 12px rgba(0, 191, 255, 0.12);
}

.rated-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 4px 8px;
  background: rgba(0, 100, 160, 0.12);
  border-bottom: 1px solid rgba(0, 191, 255, 0.12);
  flex-shrink: 0;
}

.header-decoration {
  display: flex;
  align-items: center;
  gap: 4px;
}

.header-line {
  width: 12px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 191, 255, 0.6), transparent);
}

.header-dot {
  width: 4px;
  height: 4px;
  background: rgba(0, 191, 255, 0.8);
  border-radius: 50%;
  box-shadow: 0 0 6px rgba(0, 191, 255, 0.6);
}

.rated-title {
  font-size: 12px;
  font-weight: 600;
  color: #87ceeb;
  text-align: center;
  letter-spacing: 2px;
  text-shadow: 0 0 8px rgba(135, 206, 235, 0.5);
}

.rated-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px 12px;
  overflow-y: auto;
}

.rated-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  background: rgba(0, 100, 180, 0.08);
  border-radius: 4px;
  border: 1px solid rgba(0, 191, 255, 0.1);
  transition: all 0.2s ease;
}

.rated-item:hover {
  background: rgba(0, 100, 180, 0.15);
  border-color: rgba(0, 191, 255, 0.25);
  transform: translateX(2px);
}

.rated-label {
  font-size: 11px;
  color: rgba(180, 210, 240, 0.8);
  letter-spacing: 0.5px;
}

.rated-value {
  font-size: 12px;
  font-weight: 600;
  color: #a8d8ff;
  text-shadow: 0 0 6px rgba(168, 216, 255, 0.4);
}

.content-right {
  flex: 1;
  display: flex;
  align-items: stretch;
  justify-content: center;
  min-height: 0;
}

.status-section {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.status-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0;
  min-height: 0;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  background: rgba(0, 100, 180, 0.08);
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin: 0;
}

.status-item:hover {
  background: rgba(0, 100, 180, 0.18);
  transform: translateX(2px);
}

.status-label {
  font-size: 12px;
  font-weight: 500;
  color: rgba(200, 225, 250, 0.9);
  letter-spacing: 0.5px;
}

.status-indicator {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.indicator-inner {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.active-green {
  background: rgba(0, 230, 118, 0.15);
  border: 2px solid rgba(0, 230, 118, 0.4);
  box-shadow: 0 0 10px rgba(0, 230, 118, 0.3);
}

.active-green .indicator-inner {
  background: radial-gradient(circle, #69f0ae 0%, #00e676 60%, #00c853 100%);
  box-shadow: 0 0 12px rgba(0, 230, 118, 1);
}

.active-red {
  background: rgba(255, 82, 82, 0.15);
  border: 2px solid rgba(255, 82, 82, 0.4);
  box-shadow: 0 0 10px rgba(255, 82, 82, 0.3);
}

.active-red .indicator-inner {
  background: radial-gradient(circle, #ff8a80 0%, #ff5252 60%, #d32f2f 100%);
  box-shadow: 0 0 12px rgba(255, 82, 82, 1);
}

/* 底部装饰栏 */
.border-bottom {
  display: flex;
  height: 10px;
  border-top: 1px solid rgba(0, 191, 255, 0.2);
}

.bottom-left,
.bottom-right {
  position: relative;
}

.bottom-left::before,
.bottom-right::before {
  content: '';
  position: absolute;
  top: 0;
  width: 16px;
  height: 100%;
  border-top: 2px solid #00bfff;
}

.bottom-left::before {
  left: 0;
  border-left: 2px solid #00bfff;
  border-radius: 4px 0 0 0;
}

.bottom-right::before {
  right: 0;
  border-right: 2px solid #00bfff;
  border-radius: 0 4px 0 0;
}

.bottom-center {
  flex: 1;
  border-top: 2px solid #00bfff;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(0, 191, 255, 0.4) 50%, 
    transparent 100%);
}
</style>
