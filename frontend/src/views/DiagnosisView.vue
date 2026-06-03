<template>
  <div class="view">
    <div class="content-wrapper">
      <div class="side-panel left-panel">
        <SystemArea
          title="主轴系统"
          :rated-params="spindleRated"
          :status-variables="spindleStatus"
        />
        <SystemArea
          title="润滑系统"
          :rated-params="lubricationRated"
          :status-variables="lubricationStatus"
        />
      </div>

      <div class="center-bar">
        <div class="center-connector top-connector"></div>
        <div class="center-content">
          <div class="maze-container">
            <svg viewBox="0 0 160 400" preserveAspectRatio="none" class="maze-svg">
              <defs>
                <linearGradient id="mazeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#667eea" stop-opacity="0.9"/>
                  <stop offset="50%" stop-color="#a855f7" stop-opacity="0.7"/>
                  <stop offset="100%" stop-color="#667eea" stop-opacity="0.9"/>
                </linearGradient>
                <linearGradient id="accentGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#00d4ff" stop-opacity="0.8"/>
                  <stop offset="100%" stop-color="#667eea" stop-opacity="0.6"/>
                </linearGradient>
                <linearGradient id="boundaryGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#667eea" stop-opacity="0.5"/>
                  <stop offset="50%" stop-color="#a855f7" stop-opacity="0.3"/>
                  <stop offset="100%" stop-color="#667eea" stop-opacity="0.5"/>
                </linearGradient>
                <filter id="glowMaze">
                  <feGaussianBlur stdDeviation="1.2" result="coloredBlur"/>
                  <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
                <filter id="glowAccent">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                  <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>

              <g class="maze-boundary">
                <line x1="10" y1="0" x2="10" y2="400" stroke="url(#boundaryGrad)" stroke-width="2" stroke-dasharray="5 8"/>
                <line x1="150" y1="0" x2="150" y2="400" stroke="url(#boundaryGrad)" stroke-width="2" stroke-dasharray="5 8"/>
                <line x1="80" y1="0" x2="80" y2="400" stroke="url(#boundaryGrad)" stroke-width="1" stroke-dasharray="2 4" opacity="0.5"/>
                <path d="M10 0 L20 0" stroke="url(#mazeGrad)" stroke-width="2.5" fill="none"/>
                <path d="M150 0 L140 0" stroke="url(#mazeGrad)" stroke-width="2.5" fill="none"/>
                <path d="M10 400 L20 400" stroke="url(#mazeGrad)" stroke-width="2.5" fill="none"/>
                <path d="M150 400 L140 400" stroke="url(#mazeGrad)" stroke-width="2.5" fill="none"/>
              </g>

              <g class="maze-center">
                <line x1="80" y1="0" x2="80" y2="400" stroke="url(#mazeGrad)" stroke-width="1.5" opacity="0.4"/>
              </g>

              <g class="maze-paths-left" filter="url(#glowMaze)">
                <path class="path-main" d="M80 0 L80 40 L50 40 L50 90 L80 90 L80 140 L45 140 L45 190 L80 190 L80 250 L55 250 L55 300 L80 300 L80 360 L50 360 L50 400" 
                      stroke="url(#mazeGrad)" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>

                <path class="path-alternate" d="M30 60 L55 60 L55 110 L40 110 L40 150 L60 150 L60 200 L35 200 L35 250 L55 250 L55 290 L35 290 L35 330 L60 330 L60 370 L45 370" 
                      stroke="url(#mazeGrad)" stroke-width="1.8" fill="none" stroke-linecap="round" opacity="0.75"/>

                <path class="path-branch b1" d="M50 40 L50 65 L35 65" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b2" d="M80 90 L80 115 L95 115" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b3" d="M45 140 L45 165 L60 165" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b4" d="M80 190 L80 220 L65 220" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b5" d="M55 250 L55 275 L40 275" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b6" d="M80 300 L80 330 L95 330" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
              </g>

              <g class="maze-paths-right" filter="url(#glowMaze)">
                <path class="path-main" d="M80 0 L80 40 L110 40 L110 90 L80 90 L80 140 L115 140 L115 190 L80 190 L80 250 L105 250 L105 300 L80 300 L80 360 L110 360 L110 400" 
                      stroke="url(#mazeGrad)" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>

                <path class="path-alternate" d="M130 60 L105 60 L105 110 L120 110 L120 150 L100 150 L100 200 L125 200 L125 250 L105 250 L105 290 L125 290 L125 330 L100 330 L100 370 L115 370" 
                      stroke="url(#mazeGrad)" stroke-width="1.8" fill="none" stroke-linecap="round" opacity="0.75"/>

                <path class="path-branch b1" d="M110 40 L110 65 L125 65" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b2" d="M80 90 L80 115 L65 115" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b3" d="M115 140 L115 165 L100 165" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b4" d="M80 190 L80 220 L95 220" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b5" d="M105 250 L105 275 L120 275" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                <path class="path-branch b6" d="M80 300 L80 330 L65 330" stroke="url(#mazeGrad)" stroke-width="1.5" fill="none" stroke-linecap="round"/>
              </g>

              <g class="maze-decoration-left">
                <path class="deco-line d1" d="M20 80 L30 80 L30 90" stroke="url(#accentGrad)" stroke-width="1.2" fill="none" opacity="0.7"/>
                <path class="deco-line d2" d="M25 170 L35 170" stroke="url(#accentGrad)" stroke-width="1.2" fill="none" opacity="0.6"/>
                <path class="deco-line d3" d="M18 280 L28 280 L28 295" stroke="url(#accentGrad)" stroke-width="1.2" fill="none" opacity="0.7"/>
                <path class="deco-line d4" d="M30 350 L22 350" stroke="url(#accentGrad)" stroke-width="1.2" fill="none" opacity="0.5"/>

                <circle class="node n1" cx="80" cy="40" r="4" fill="url(#accentGrad)" filter="url(#glowAccent)"/>
                <circle class="node n2" cx="50" cy="90" r="3" fill="url(#mazeGrad)" filter="url(#glowMaze)"/>
                <circle class="node n3" cx="80" cy="140" r="4" fill="url(#accentGrad)" filter="url(#glowAccent)"/>
                <circle class="node n4" cx="45" cy="190" r="3" fill="url(#mazeGrad)" filter="url(#glowMaze)"/>
                <circle class="node n5" cx="80" cy="250" r="4" fill="url(#accentGrad)" filter="url(#glowAccent)"/>
                <circle class="node n6" cx="55" cy="300" r="3" fill="url(#mazeGrad)" filter="url(#glowMaze)"/>
                <circle class="node n7" cx="80" cy="360" r="4" fill="url(#accentGrad)" filter="url(#glowAccent)"/>
              </g>

              <g class="maze-decoration-right">
                <path class="deco-line d1" d="M140 80 L130 80 L130 90" stroke="url(#accentGrad)" stroke-width="1.2" fill="none" opacity="0.7"/>
                <path class="deco-line d2" d="M135 170 L125 170" stroke="url(#accentGrad)" stroke-width="1.2" fill="none" opacity="0.6"/>
                <path class="deco-line d3" d="M142 280 L132 280 L132 295" stroke="url(#accentGrad)" stroke-width="1.2" fill="none" opacity="0.7"/>
                <path class="deco-line d4" d="M130 350 L138 350" stroke="url(#accentGrad)" stroke-width="1.2" fill="none" opacity="0.5"/>

                <circle class="node n1" cx="80" cy="40" r="4" fill="url(#accentGrad)" filter="url(#glowAccent)"/>
                <circle class="node n2" cx="110" cy="90" r="3" fill="url(#mazeGrad)" filter="url(#glowMaze)"/>
                <circle class="node n3" cx="80" cy="140" r="4" fill="url(#accentGrad)" filter="url(#glowAccent)"/>
                <circle class="node n4" cx="115" cy="190" r="3" fill="url(#mazeGrad)" filter="url(#glowMaze)"/>
                <circle class="node n5" cx="80" cy="250" r="4" fill="url(#accentGrad)" filter="url(#glowAccent)"/>
                <circle class="node n6" cx="105" cy="300" r="3" fill="url(#mazeGrad)" filter="url(#glowMaze)"/>
                <circle class="node n7" cx="80" cy="360" r="4" fill="url(#accentGrad)" filter="url(#glowAccent)"/>
              </g>

              <g class="particle-flow-left">
                <circle class="particle p1" r="3" fill="#00d4ff" filter="url(#glowAccent)">
                  <animateMotion dur="10s" repeatCount="indefinite" path="M80 0 L80 40 L50 40 L50 90 L80 90 L80 140 L45 140 L45 190 L80 190"/>
                </circle>
                <circle class="particle p2" r="2.5" fill="#a855f7" filter="url(#glowAccent)">
                  <animateMotion dur="8s" repeatCount="indefinite" path="M80 190 L80 250 L55 250 L55 300 L80 300 L80 360 L50 360 L50 400"/>
                </circle>
              </g>

              <g class="particle-flow-right">
                <circle class="particle p3" r="3" fill="#00d4ff" filter="url(#glowAccent)">
                  <animateMotion dur="10s" repeatCount="indefinite" path="M80 0 L80 40 L110 40 L110 90 L80 90 L80 140 L115 140 L115 190 L80 190"/>
                </circle>
                <circle class="particle p4" r="2.5" fill="#a855f7" filter="url(#glowAccent)">
                  <animateMotion dur="8s" repeatCount="indefinite" path="M80 190 L80 250 L105 250 L105 300 L80 300 L80 360 L110 360 L110 400"/>
                </circle>
              </g>

              <g class="ambient-particles">
                <circle class="ambient-dot ad1" r="2" fill="#667eea">
                  <animate attributeName="opacity" dur="3s" repeatCount="indefinite" values="0.2;0.8;0.2"/>
                </circle>
                <circle class="ambient-dot ad2" r="1.5" fill="#a855f7">
                  <animate attributeName="opacity" dur="2.5s" repeatCount="indefinite" values="0.3;0.9;0.3"/>
                </circle>
                <circle class="ambient-dot ad3" r="2" fill="#00d4ff">
                  <animate attributeName="opacity" dur="4s" repeatCount="indefinite" values="0.2;0.7;0.2"/>
                </circle>
                <circle class="ambient-dot ad4" r="1.5" fill="#667eea">
                  <animate attributeName="opacity" dur="3.5s" repeatCount="indefinite" values="0.4;0.8;0.4"/>
                </circle>
              </g>
            </svg>
          </div>
        </div>
        <div class="center-connector bottom-connector"></div>
      </div>

      <div class="side-panel right-panel">
        <SystemArea
          title="进给系统"
          :rated-params="feedRated"
          :status-variables="feedStatus"
        />
        <SystemArea
          title="液压系统"
          :rated-params="hydraulicRated"
          :status-variables="hydraulicStatus"
        />
      </div>
    </div>
  </div>
</template>

<script>
import SystemArea from '@/components/SystemArea.vue'

export default {
  name: 'DiagnosisView',
  components: {
    SystemArea
  },
  data() {
    return {
      spindleRated: [
        { label: '额定转速', value: '3000 RPM' },
        { label: '额定功率', value: '15 kW' },
        { label: '额定扭矩', value: '48 Nm' },
        { label: '额定电压', value: '380 V' },
        { label: '额定电流', value: '32 A' }
      ],
      spindleStatus: this.generateStatus(['主轴运行', '定向完成', '换刀完成', '过载保护', '急停触发', '温度异常', '振动超限']),
      
      lubricationRated: [
        { label: '额定压力', value: '0.4 MPa' },
        { label: '供油流量', value: '2.5 L/min' },
        { label: '油箱容量', value: '20 L' },
        { label: '过滤精度', value: '10 μm' },
        { label: '工作粘度', value: '46 cSt' }
      ],
      lubricationStatus: this.generateStatus(['油泵运行', '压力正常', '油位正常', '温度正常', '过滤器堵塞', '油路泄漏', '压力低报警']),
      
      feedRated: [
        { label: 'X轴行程', value: '500 mm' },
        { label: 'Y轴行程', value: '400 mm' },
        { label: 'Z轴行程', value: '300 mm' },
        { label: '快移速度', value: '12000 mm/min' },
        { label: '定位精度', value: '0.01 mm' }
      ],
      feedStatus: this.generateStatus(['X轴原点', 'Y轴原点', 'Z轴原点', '伺服使能', '限位触发', '跟随误差', '定位完成']),
      
      hydraulicRated: [
        { label: '额定压力', value: '7.0 MPa' },
        { label: '泵流量', value: '40 L/min' },
        { label: '电机功率', value: '11 kW' },
        { label: '油箱容积', value: '100 L' },
        { label: '工作压力', value: '6.5 MPa' }
      ],
      hydraulicStatus: this.generateStatus(['油泵运行', '卸荷状态', '蓄能器压力', '冷却器运行', '滤油器堵塞', '液位低报警', '压力正常'])
    }
  },
  methods: {
    generateStatus(labels) {
      return labels.map(label => ({
        label: label,
        value: Math.random() > 0.2 ? 1 : 0
      }))
    }
  }
}
</script>

<style scoped>
.view {
  height: 100%;
  overflow: hidden;
  display: flex;
  align-items: stretch;
}

.content-wrapper {
  display: flex;
  width: 100%;
  height: 100%;
  gap: 0;
}

.side-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 6px 0;
}

.left-panel {
  padding-right: 10px;
}

.right-panel {
  padding-left: 10px;
}

.center-bar {
  width: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.center-connector {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99, 126, 234, 0.7), transparent);
  flex-shrink: 0;
}

.top-connector {
  margin-bottom: 6px;
}

.bottom-connector {
  margin-top: 6px;
}

.center-content {
  flex: 1;
  width: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 0;
}

.maze-container {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 160px;
}

.maze-svg {
  width: 100%;
  height: 100%;
}

.maze-paths-left .path-main,
.maze-paths-right .path-main {
  stroke-dasharray: 1200;
  stroke-dashoffset: 1200;
  animation: drawPath 5s ease-out forwards;
}

@keyframes drawPath {
  to {
    stroke-dashoffset: 0;
  }
}

.node {
  opacity: 0;
  animation: nodeAppear 0.6s ease-out forwards;
}

.n1 { animation-delay: 0.3s; }
.n2 { animation-delay: 0.5s; }
.n3 { animation-delay: 0.8s; }
.n4 { animation-delay: 1.1s; }
.n5 { animation-delay: 1.4s; }
.n6 { animation-delay: 1.7s; }
.n7 { animation-delay: 2.0s; }

@keyframes nodeAppear {
  0% {
    opacity: 0;
    transform: scale(0);
  }
  50% {
    transform: scale(1.4);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.particle {
  opacity: 0.9;
}

.ambient-particles .ambient-dot {
  opacity: 0.5;
}

.ambient-dot.ad1 { cx: 35; cy: 50; }
.ambient-dot.ad2 { cx: 125; cy: 120; }
.ambient-dot.ad3 { cx: 55; cy: 220; }
.ambient-dot.ad4 { cx: 105; cy: 310; }

.deco-line {
  opacity: 0;
  animation: decoAppear 1s ease-out forwards;
}

.d1 { animation-delay: 0.4s; }
.d2 { animation-delay: 0.7s; }
.d3 { animation-delay: 1.0s; }
.d4 { animation-delay: 1.3s; }

@keyframes decoAppear {
  0% {
    opacity: 0;
    transform: translateX(-5px);
  }
  100% {
    opacity: 0.7;
    transform: translateX(0);
  }
}

.maze-decoration-right .deco-line {
  animation-name: decoAppearRight;
}

@keyframes decoAppearRight {
  0% {
    opacity: 0;
    transform: translateX(5px);
  }
  100% {
    opacity: 0.7;
    transform: translateX(0);
  }
}
</style>
