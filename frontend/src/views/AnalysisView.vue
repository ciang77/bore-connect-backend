<template>
  <div class="view">
    <div class="content-wrapper">
      <div class="grid-container">
        <div class="grid-item device-model">
          <div class="device-model-split">
            <div class="border-box device-model-box">
              <div class="border-top">
                <div class="corner top-left"></div>
                <div class="decoration left">
                  <div class="d-block" v-for="i in 3" :key="'dm-l-' + i"></div>
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
                  <h2 class="title-text">设备型号</h2>
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
                  <div class="d-block" v-for="i in 3" :key="'dm-r-' + i"></div>
                </div>
                <div class="corner top-right"></div>
              </div>
              <div class="border-body">
                <div class="side-line left"></div>
                <div class="content-area">
                  <div class="device-model-content">
                    <div class="device-info-card compact">
                      <div class="info-grid">
                        <div class="info-item">
                          <span class="info-label">设备型号</span>
                          <span class="info-value">BM-2024 Pro</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">规 格</span>
                          <span class="info-value">CNC-800</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">额定功率</span>
                          <span class="info-value">15.0 kW</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">额定转速</span>
                          <span class="info-value">3000 RPM</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">工作电压</span>
                          <span class="info-value">380 V</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">设备重量</span>
                          <span class="info-value">1250 kg</span>
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

            <div class="border-box prediction-performance-box">
              <div class="border-top">
                <div class="corner top-left"></div>
                <div class="decoration left">
                  <div class="d-block" v-for="i in 3" :key="'pp-l-' + i"></div>
                </div>
                <div class="title-bar">
                  <div class="title-decoration left">
                    <div class="deco-line"></div>
                    <div class="deco-diamond"></div>
                    <div class="deco-dot"></div>
                  </div>
                  <h2 class="title-text">预测性能</h2>
                  <div class="title-decoration right">
                    <div class="deco-line"></div>
                    <div class="deco-diamond"></div>
                    <div class="deco-dot"></div>
                  </div>
                </div>
                <div class="decoration right">
                  <div class="d-block" v-for="i in 3" :key="'pp-r-' + i"></div>
                </div>
                <div class="corner top-right"></div>
              </div>
              <div class="border-body">
                <div class="side-line left"></div>
                <div class="content-area">
                  <div class="perf-wrapper">
                    <div class="battery-indicator perf-battery">
                      <div class="battery-cap"></div>
                      <div class="battery-outline">
                        <div
                          class="battery-fill"
                          :class="getMseClass(modelMSE)"
                          :style="{ height: getMsePercent(modelMSE) + '%' }"
                        ></div>
                        <div class="battery-text">
                          <div class="battery-text-title">MSE</div>
                          <div class="battery-text-value">{{ modelMSE.toFixed(3) }}</div>
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
        </div>

        <div class="grid-item deviation-rate">
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
                <h2 class="title-text">偏差率</h2>
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
                <div class="chart-container">
                  <div class="chart-body-area">
                    <div class="chart-y-axis">
                      <span v-for="tick in chartYAxisConfig.ticks" :key="tick">{{ tick }}{{ chartYAxisConfig.unit }}</span>
                    </div>
                    <div class="chart-bars">
                      <div class="bar-item" v-for="(item, index) in deviationData" :key="index">
                        <div class="bar-track" :style="{ '--bar-h': getBarHeight(item.value) + '%' }">
                          <div
                            class="bar-fill"
                            :class="getDeviationBarClass(item.value)"
                          ></div>
                          <div class="bar-tooltip">{{ item.value.toFixed(2) }}%</div>
                        </div>
                        <span class="bar-label">{{ item.label }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="chart-legend">
                    <div class="legend-item">
                      <div class="legend-color normal"></div>
                      <span>正常 (&lt;1%)</span>
                    </div>
                    <div class="legend-item">
                      <div class="legend-color warning"></div>
                      <span>警告 (1-3%)</span>
                    </div>
                    <div class="legend-item">
                      <div class="legend-color danger"></div>
                      <span>异常 (&gt;3%)</span>
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

        <div class="grid-item real-time-status">
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
                <h2 class="title-text">设备实时运行状态</h2>
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
                <div class="realtime-data-container">
                  <div class="subsystem-group" v-for="(subsystem, sIndex) in realtimeData" :key="sIndex">
                    <div class="subsystem-title">
                      <span class="subsystem-dot" :class="'dot-' + sIndex"></span>
                      {{ subsystem.name }}
                    </div>
                    <div class="data-table">
                      <div class="data-cell" v-for="(param, pIndex) in subsystem.params" :key="pIndex">
                        <div class="cell-label">{{ param.label }}</div>
                        <div class="cell-value" :class="getParamClass(param)">{{ Number(param.value).toFixed(2) }}</div>
                        <div class="cell-unit">{{ param.unit }}</div>
                        <div class="cell-bar">
                          <div class="cell-bar-fill" :class="getRealtimeBarClass(param)" :style="{ width: getPercent(param) + '%' }"></div>
                        </div>
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

        <div class="grid-item model-performance">
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
                <h2 class="title-text">主轴预测</h2>
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
                <div class="prediction-chart-container">
                  <div class="chart-header">
                    <div class="chart-title">振动信号预测</div>
                    <div class="chart-legend">
                      <span class="legend-item">
                        <span class="legend-line real-line"></span>
                        <span>真实值</span>
                      </span>
                      <span class="legend-item">
                        <span class="legend-line history-pred-line"></span>
                        <span>历史预测</span>
                      </span>
                      <span class="legend-item">
                        <span class="legend-line future-pred-line"></span>
                        <span>未来预测</span>
                      </span>
                    </div>
                  </div>
                  <div class="chart-body">
                    <div class="chart-y-axis-spindle">
                      <span v-for="tick in spindleYAxisTicks" :key="tick">{{ tick }}</span>
                    </div>
                    <svg class="prediction-svg" viewBox="0 0 1000 300" preserveAspectRatio="none">
                      <defs>
                        <linearGradient id="confidenceGrad" x1="0" y1="0" x2="0" y2="300" gradientUnits="userSpaceOnUse">
                          <stop offset="0%" stop-color="rgba(168, 85, 247, 0.35)"/>
                          <stop offset="100%" stop-color="rgba(168, 85, 247, 0.05)"/>
                        </linearGradient>
                        <linearGradient id="realLineGrad" x1="0" y1="0" x2="1000" y2="0" gradientUnits="userSpaceOnUse">
                          <stop offset="0%" stop-color="#00ff88"/>
                          <stop offset="100%" stop-color="#00cc6a"/>
                        </linearGradient>
                        <linearGradient id="predLineGrad" x1="0" y1="0" x2="1000" y2="0" gradientUnits="userSpaceOnUse">
                          <stop offset="0%" stop-color="#00d4ff"/>
                          <stop offset="50%" stop-color="#a855f7"/>
                          <stop offset="100%" stop-color="#7c3aed"/>
                        </linearGradient>
                        <filter id="glow">
                          <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
                          <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                          </feMerge>
                        </filter>
                      </defs>
                      <!-- 背景 -->
                      <rect x="80" y="18" width="630" height="246" fill="rgba(0, 255, 136, 0.015)" rx="2"/>
                      <rect x="710" y="18" width="270" height="246" fill="rgba(168, 85, 247, 0.02)" rx="2"/>
                      <!-- 网格线 -->
                      <line v-for="tick in spindleYAxisTicks" :key="'grid-' + tick"
                        x1="80" :y1="getYCoord(tick)" x2="980" :y2="getYCoord(tick)"
                        stroke="rgba(0, 191, 255, 0.12)" stroke-width="0.5" stroke-dasharray="3,3"/>
                      <!-- 分界线 -->
                      <line x1="710" y1="18" x2="710" y2="264" stroke="rgba(255, 255, 255, 0.2)" stroke-width="1" stroke-dasharray="5,3"/>
                      <!-- 区域标签 -->
                      <text x="395" y="55" fill="rgba(0, 255, 136, 0.5)" font-size="12" text-anchor="middle">历史数据区 (42s)</text>
                      <text x="845" y="55" fill="rgba(168, 85, 247, 0.5)" font-size="12" text-anchor="middle">预测区 (18s)</text>
                      <!-- 置信区间 -->
                      <polygon :points="confidenceAreaPoints" fill="url(#confidenceGrad)" opacity="0.5"/>
                      <polyline :points="confidenceUpperPoints" fill="none" stroke="rgba(168, 85, 247, 0.3)" stroke-width="0.8" stroke-dasharray="3,2"/>
                      <polyline :points="confidenceLowerPoints" fill="none" stroke="rgba(168, 85, 247, 0.3)" stroke-width="0.8" stroke-dasharray="3,2"/>
                      <polyline :points="historyPredPoints" fill="none" stroke="#00d4ff" stroke-width="2" stroke-dasharray="6,4"/>
                      <polyline :points="futurePredPoints" fill="none" stroke="#a855f7" stroke-width="2" filter="url(#glow)"/>
                      <!-- 真实值线 -->
                      <polyline :points="realValuePoints" fill="none" stroke="url(#realLineGrad)" stroke-width="2" filter="url(#glow)"/>
                    </svg>
                    <div class="chart-axis">
                      <div class="axis-labels">
                        <span v-for="(label, index) in timeLabels" :key="index" :style="{ left: getLabelPosition(index) + '%' }">{{ label }}</span>
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

        <div class="grid-item error-analysis">
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
                <h2 class="title-text">误差分析</h2>
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
                <div class="error-analysis-wrapper">
                  <div class="error-table-header">
                    <div class="error-table-title">
                      <svg class="title-icon" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14H6v-2h6v2zm4-4H6v-2h10v2zm0-4H6V7h10v2z"/>
                      </svg>
                      <span>误差分析数据表</span>
                    </div>
                    <div class="error-table-actions">
                      <button class="copy-btn" @click="copyErrorTable" :class="{ copied: copySuccess }" title="复制表格数据">
                        <svg v-if="!copySuccess" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="currentColor">
                          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                        </svg>
                        <span>{{ copySuccess ? '已复制' : '复制' }}</span>
                      </button>
                    </div>
                  </div>
                  <div class="error-table-container">
                    <table class="error-analysis-table" id="errorAnalysisTable">
                      <thead>
                        <tr class="row-subsystem">
                          <th class="col-indicator" rowspan="2">指标</th>
                          <th class="col-subsystem" v-for="(subsystem, sIndex) in errorAnalysisData" :key="'sub-' + sIndex" :colspan="2">
                            <div class="subsystem-name">{{ subsystem.name }}</div>
                          </th>
                        </tr>
                        <tr class="row-param">
                          <th class="col-param" v-for="(item, index) in flattenedErrorData" :key="'param-' + index">
                            {{ item.label }}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr class="row-actual" :class="{ 'row-alt': true }">
                          <td class="col-indicator-label">实际值</td>
                          <td class="col-value" v-for="(item, index) in flattenedErrorData" :key="'actual-' + index">
                            {{ formatValue(item.actual) }}
                          </td>
                        </tr>
                        <tr class="row-predicted">
                          <td class="col-indicator-label">预测值</td>
                          <td class="col-value" v-for="(item, index) in flattenedErrorData" :key="'pred-' + index">
                            {{ formatValue(item.predicted) }}
                          </td>
                        </tr>
                        <tr class="row-error" :class="{ 'row-alt': true }">
                          <td class="col-indicator-label">误差值</td>
                          <td class="col-error" v-for="(item, index) in flattenedErrorData" :key="'err-' + index" :class="getErrorClass(item.error)">
                            {{ item.error.toFixed(2) }}%
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div class="error-table-footer">
                    <div class="error-legend">
                      <span class="legend-item"><span class="legend-dot normal"></span>正常 (&lt;1%)</span>
                      <span class="legend-item"><span class="legend-dot warning"></span>警告 (1-3%)</span>
                      <span class="legend-item"><span class="legend-dot danger"></span>异常 (&gt;3%)</span>
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

        <div class="grid-item servo-current">
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
                <h2 class="title-text">伺服电机电流</h2>
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
                <div class="motor-current-container">
                  <div class="motor-grid">
                    <div class="motor-item" v-for="(motor, index) in motorCurrents" :key="index"
                      :class="{ 'motor-alert': motor.current > motor.maxCurrent || motor.current < motor.minCurrent }">
                      <div class="motor-header">
                        <span class="motor-dot" :class="{ 'dot-alert': motor.current > motor.maxCurrent || motor.current < motor.minCurrent }"></span>
                        <span class="motor-number">{{ motor.id }}</span>
                        <span class="motor-status" :class="motor.current > motor.maxCurrent || motor.current < motor.minCurrent ? 'status-alert' : 'status-ok'">
                          {{ motor.current > motor.maxCurrent || motor.current < motor.minCurrent ? '异常' : '正常' }}
                        </span>
                      </div>
                      <div class="motor-value" :class="{ 'value-alert': motor.current > motor.maxCurrent || motor.current < motor.minCurrent }">
                        {{ motor.current.toFixed(1) }}<small>A</small>
                      </div>
                      <div class="motor-bar-wrap">
                        <div class="motor-bar-range">
                          <span>{{ motor.minCurrent }}</span>
                          <span>{{ motor.maxCurrent }}</span>
                        </div>
                        <div class="motor-bar">
                          <div
                            class="motor-bar-fill"
                            :class="motor.current > motor.maxCurrent || motor.current < motor.minCurrent ? 'fill-alert' : 'fill-ok'"
                            :style="{ width: getMotorBarPercent(motor) + '%' }"
                          ></div>
                          <div class="motor-bar-dot"
                            :class="motor.current > motor.maxCurrent || motor.current < motor.minCurrent ? 'dot-alert' : ''"
                            :style="{ left: getMotorBarPercent(motor) + '%' }"
                          ></div>
                        </div>
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
      </div>
    </div>
  </div>
</template>

<script>
import { fetchMotorCurrents } from '../api/analysis'

export default {
  name: 'AnalysisView',
  data() {
    return {
      modelMAE: 2.847,
      modelMSE: 6.214,
      maeHistory: [3.2, 2.9, 3.1, 2.7, 3.0, 2.8, 2.9, 2.6, 2.7, 2.8],
      spindlePrediction: {
        history: [
          { time: -42, real: 0.042, pred: 0.042 }, { time: -41, real: 0.043, pred: 0.043 },
          { time: -40, real: 0.042, pred: 0.042 }, { time: -39, real: 0.043, pred: 0.043 },
          { time: -38, real: 0.044, pred: 0.044 }, { time: -37, real: 0.043, pred: 0.043 },
          { time: -36, real: 0.042, pred: 0.042 }, { time: -35, real: 0.043, pred: 0.043 },
          { time: -34, real: 0.044, pred: 0.044 }, { time: -33, real: 0.043, pred: 0.043 },
          { time: -32, real: 0.042, pred: 0.042 }, { time: -31, real: 0.043, pred: 0.043 },
          { time: -30, real: 0.044, pred: 0.044 }, { time: -29, real: 0.043, pred: 0.043 },
          { time: -28, real: 0.045, pred: 0.045 }, { time: -27, real: 0.044, pred: 0.044 },
          { time: -26, real: 0.043, pred: 0.043 }, { time: -25, real: 0.042, pred: 0.042 },
          { time: -24, real: 0.043, pred: 0.043 }, { time: -23, real: 0.044, pred: 0.044 },
          { time: -22, real: 0.043, pred: 0.043 }, { time: -21, real: 0.044, pred: 0.044 },
          { time: -20, real: 0.045, pred: 0.045 }, { time: -19, real: 0.044, pred: 0.044 },
          { time: -18, real: 0.043, pred: 0.043 }, { time: -17, real: 0.044, pred: 0.044 },
          { time: -16, real: 0.043, pred: 0.043 }, { time: -15, real: 0.044, pred: 0.044 },
          { time: -14, real: 0.042, pred: 0.042 }, { time: -13, real: 0.043, pred: 0.043 },
          { time: -12, real: 0.044, pred: 0.044 }, { time: -11, real: 0.043, pred: 0.043 },
          { time: -10, real: 0.045, pred: 0.045 }, { time: -9, real: 0.044, pred: 0.044 },
          { time: -8, real: 0.043, pred: 0.043 }, { time: -7, real: 0.044, pred: 0.044 },
          { time: -6, real: 0.043, pred: 0.043 }, { time: -5, real: 0.044, pred: 0.044 },
          { time: -4, real: 0.042, pred: 0.042 }, { time: -3, real: 0.043, pred: 0.043 },
          { time: -2, real: 0.044, pred: 0.044 }, { time: -1, real: 0.043, pred: 0.043 },
          { time: 0, real: 0.044, pred: 0.044 }
        ],
        future: [
          { time: 1, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 2, pred: 0.045, lower: 0.044, upper: 0.046 },
          { time: 3, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 4, pred: 0.045, lower: 0.044, upper: 0.046 },
          { time: 5, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 6, pred: 0.045, lower: 0.044, upper: 0.046 },
          { time: 7, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 8, pred: 0.045, lower: 0.044, upper: 0.046 },
          { time: 9, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 10, pred: 0.045, lower: 0.044, upper: 0.046 },
          { time: 11, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 12, pred: 0.045, lower: 0.044, upper: 0.046 },
          { time: 13, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 14, pred: 0.045, lower: 0.044, upper: 0.046 },
          { time: 15, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 16, pred: 0.045, lower: 0.044, upper: 0.046 },
          { time: 17, pred: 0.044, lower: 0.043, upper: 0.045 },
          { time: 18, pred: 0.045, lower: 0.044, upper: 0.046 }
        ]
      },
      deviationData: [],
      realtimeData: [
        {
          name: '主轴系统',
          params: [
            { label: '振动信号', value: 0.042, unit: 'mm/s', max: 0.071, status: 'normal' },
            { label: '电机电流', value: 28.5, unit: 'A', max: 32, status: 'normal' },
            { label: '轴承温度', value: 62, unit: '°C', max: 80, status: 'normal' },
            { label: '冷却液压', value: 0.42, unit: 'MPa', max: 0.5, status: 'normal' }
          ]
        },
        {
          name: '进给系统',
          params: [
            { label: 'X轴位置', value: 125.6, unit: 'mm', max: 500, status: 'normal' },
            { label: 'Y轴位置', value: 98.3, unit: 'mm', max: 400, status: 'normal' },
            { label: 'Z轴位置', value: 75.2, unit: 'mm', max: 300, status: 'normal' },
            { label: '跟随误差', value: 0.008, unit: 'mm', max: 0.015, status: 'normal' }
          ]
        },
        {
          name: '润滑系统',
          params: [
            { label: '供油压力', value: 0.38, unit: 'MPa', max: 0.45, status: 'normal' },
            { label: '油温', value: 42, unit: '°C', max: 60, status: 'normal' },
            { label: '流量', value: 2.3, unit: 'L/min', max: 3.0, status: 'normal' },
            { label: '油位', value: 85, unit: '%', max: 100, status: 'normal' }
          ]
        },
        {
          name: '液压系统',
          params: [
            { label: '系统压力', value: 6.8, unit: 'MPa', max: 7.5, status: 'normal' },
            { label: '泵流量', value: 38.5, unit: 'L/min', max: 45, status: 'normal' },
            { label: '油温', value: 48, unit: '°C', max: 65, status: 'normal' },
            { label: '蓄能器', value: 6.2, unit: 'MPa', max: 7.0, status: 'normal' }
          ]
        }
      ],
      errorAnalysisData: [
        {
          name: '主轴系统',
          params: [
            { label: '主轴转速', actual: 3000.12, predicted: 2998.45, error: 0.056 },
            { label: '主轴扭矩', actual: 47.85, predicted: 48.12, error: 0.564 }
          ]
        },
        {
          name: '进给系统',
          params: [
            { label: '进给速率', actual: 1200.08, predicted: 1195.32, error: 0.397 },
            { label: 'X轴位置', actual: 125.68, predicted: 126.15, error: 0.374 }
          ]
        },
        {
          name: '润滑系统',
          params: [
            { label: 'Y轴位置', actual: 98.32, predicted: 97.85, error: 0.477 },
            { label: '润滑压力', actual: 0.38, predicted: 0.392, error: 3.158 }
          ]
        },
        {
          name: '液压冷却系统',
          params: [
            { label: '液压压力', actual: 6.82, predicted: 6.75, error: 1.026 },
            { label: '冷却温度', actual: 22.5, predicted: 22.8, error: 1.333 }
          ]
        }
      ],
      motorCurrents: [],
      copySuccess: false
    }
  },
  mounted() {
    this.initMotorCurrents()
    this.initDeviationData()
    this.startDataUpdate()

    // SSE 实时推送替代电机电流轮询
    this._motorEs = new EventSource('/api/analysis/motor-currents/stream')
    this._motorEs.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        this.motorCurrents = data
      } catch { /* ignore malformed data */ }
    }
  },
  beforeUnmount() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer)
    }
    if (this._motorEs) {
      this._motorEs.close()
      this._motorEs = null
    }
  },
  computed: {
    trendPoints() {
      return this.maeHistory.map((val, i) => {
        const x = 10 + i * 20
        const y = 60 - (val / 10 * 55)
        return `${x},${y}`
      }).join(' ')
    },
    realValuePoints() {
      return this.spindlePrediction.history.map(point => {
        return `${this.getXCoord(point.time)},${this.getYCoord(point.real)}`
      }).join(' ')
    },
    historyPredPoints() {
      return this.spindlePrediction.history
        .map(point => `${this.getXCoord(point.time)},${this.getYCoord(point.pred)}`)
        .join(' ')
    },
    futurePredPoints() {
      const lastHistory = this.spindlePrediction.history[this.spindlePrediction.history.length - 1]
      const start = `${this.getXCoord(lastHistory.time)},${this.getYCoord(lastHistory.pred)}`
      const points = this.spindlePrediction.future
        .map(point => `${this.getXCoord(point.time)},${this.getYCoord(point.pred)}`)
      return [start, ...points].join(' ')
    },
    confidenceUpperPoints() {
      const lastHistory = this.spindlePrediction.history[this.spindlePrediction.history.length - 1]
      const start = `${this.getXCoord(lastHistory.time)},${this.getYCoord(lastHistory.pred)}`
      const points = this.spindlePrediction.future.map(point => {
        return `${this.getXCoord(point.time)},${this.getYCoord(point.upper)}`
      })
      return [start, ...points].join(' ')
    },
    confidenceLowerPoints() {
      const lastHistory = this.spindlePrediction.history[this.spindlePrediction.history.length - 1]
      const start = `${this.getXCoord(lastHistory.time)},${this.getYCoord(lastHistory.pred)}`
      const points = this.spindlePrediction.future.map(point => {
        return `${this.getXCoord(point.time)},${this.getYCoord(point.lower)}`
      })
      return [start, ...points].join(' ')
    },
    confidenceAreaPoints() {
      const lastHistory = this.spindlePrediction.history[this.spindlePrediction.history.length - 1]
      const start = `${this.getXCoord(lastHistory.time)},${this.getYCoord(lastHistory.pred)}`
      const upperPoints = this.spindlePrediction.future.map(point => {
        return `${this.getXCoord(point.time)},${this.getYCoord(point.upper)}`
      })
      const lowerPoints = [...this.spindlePrediction.future].reverse().map(point => {
        return `${this.getXCoord(point.time)},${this.getYCoord(point.lower)}`
      })
      return start + ' ' + upperPoints.join(' ') + ' ' + lowerPoints.join(' ') + ' ' + start
    },
    timeLabels() {
      const points = [-42, -28, -14, 0, 18]
      return points.map(i => {
        if (i === 0) return '现在'
        if (i < 0) return `${Math.abs(i)}s前`
        return `+${i}s`
      })
    },
    spindleYRange() {
      const allValues = [
        ...this.spindlePrediction.history.map(p => p.real),
        ...this.spindlePrediction.history.map(p => p.pred),
        ...this.spindlePrediction.future.map(p => p.lower),
        ...this.spindlePrediction.future.map(p => p.upper)
      ]
      const dataMin = Math.min(...allValues)
      const dataMax = Math.max(...allValues)
      const padding = (dataMax - dataMin) * 0.15
      const yMin = Math.floor((dataMin - padding) * 1000) / 1000
      const yMax = Math.ceil((dataMax + padding) * 1000) / 1000
      return { min: yMin, max: yMax }
    },
    spindleYAxisTicks() {
      const { min, max } = this.spindleYRange
      const range = max - min
      const rawStep = range / 6
      const magnitude = Math.pow(10, Math.floor(Math.log10(rawStep)))
      const normalized = rawStep / magnitude
      let step
      if (normalized <= 1) step = magnitude
      else if (normalized <= 2) step = 2 * magnitude
      else if (normalized <= 5) step = 5 * magnitude
      else step = 10 * magnitude
      step = Math.max(step, 0.001)
      const ticks = []
      let tick = Math.ceil(min / step) * step
      while (tick <= max + step * 0.01) {
        ticks.push(parseFloat(tick.toFixed(4)))
        tick += step
      }
      return ticks
    },
    flattenedErrorData() {
      const result = []
      this.errorAnalysisData.forEach(subsystem => {
        subsystem.params.forEach(param => {
          result.push({
            subsystem: subsystem.name,
            ...param
          })
        })
      })
      return result
    },
    chartYAxisConfig() {
      if (!this.deviationData || this.deviationData.length === 0) {
        return { max: 5, ticks: [5, 4, 3, 2, 1, 0], unit: '%' }
      }

      const values = this.deviationData.map(item => item.value)
      const maxValue = Math.max(...values)

      let yMax
      if (maxValue <= 1) {
        yMax = 1.5
      } else if (maxValue <= 3) {
        yMax = Math.ceil(maxValue * 1.2 * 10) / 10
      } else {
        yMax = Math.ceil(maxValue * 1.15 * 10) / 10
      }
      yMax = Math.max(yMax, 1.5)

      const tickCount = 5
      const tickStep = yMax / tickCount
      const ticks = []
      for (let i = tickCount; i >= 0; i--) {
        ticks.push(parseFloat((i * tickStep).toFixed(2)))
      }

      return { max: yMax, ticks, unit: '%', hasOutlier: maxValue > 3 }
    }
  },
  methods: {
    getTickStep(max) {
      if (max <= 10) return 2
      if (max <= 20) return 5
      if (max <= 50) return 10
      return 20
    },
    getXCoord(time) {
      return 80 + ((time - (-42)) / (18 - (-42))) * (980 - 80)
    },
    getYCoord(value) {
      const { min, max } = this.spindleYRange
      return 264 - ((value - min) / (max - min)) * (264 - 18)
    },
    getLabelPosition(index) {
      const totalLabels = this.timeLabels.length
      return 8 + (index / (totalLabels - 1)) * 90
    },
    async initMotorCurrents() {
      try {
        const res = await fetchMotorCurrents()
        if (res.code === 0 && res.data) {
          this.motorCurrents = res.data
        }
      } catch {
        // fallback to empty
      }
    },
    initDeviationData() {
      this.deviationData = []
      this.errorAnalysisData.forEach(subsystem => {
        subsystem.params.forEach(param => {
          this.deviationData.push({
            label: param.label,
            value: param.error,
            system: subsystem.name
          })
        })
      })
    },
    startDataUpdate() {
      this.updateTimer = setInterval(() => {
        this.updateData()
      }, 2000)
    },
    async updateData() {
      this.realtimeData.forEach(subsystem => {
        subsystem.params.forEach(param => {
          const variation = (Math.random() - 0.5) * 0.1 * param.max
          param.value = Math.max(0, Math.min(param.max * 1.2, param.value + variation))
        })
      })
      this.errorAnalysisData.forEach(subsystem => {
        subsystem.params.forEach(item => {
          const variation = (Math.random() - 0.5) * 0.01
          item.actual = Math.max(0, item.actual + variation)
          item.predicted = Math.max(0, item.predicted + variation)
          item.error = Math.abs((item.actual - item.predicted) / item.actual * 100)
        })
      })
      this.syncDeviationData()
      this.updateSpindlePrediction()

      this.modelMAE = Math.max(0.1, this.modelMAE + (Math.random() - 0.5) * 0.1)
      this.modelMSE = Math.max(0.1, this.modelMSE + (Math.random() - 0.5) * 0.25)
      this.maeHistory.push(this.modelMAE)
      if (this.maeHistory.length > 10) {
        this.maeHistory.shift()
      }
    },
    updateSpindlePrediction() {
      const last = this.spindlePrediction.history[this.spindlePrediction.history.length - 1]
      const newReal = last.real + (Math.random() - 0.5) * 0.002
      const clampedReal = Math.max(0.038, Math.min(0.052, newReal))
      const clampedPred = clampedReal + (Math.random() - 0.5) * 0.0008

      this.spindlePrediction.history.shift()
      this.spindlePrediction.history.forEach(p => { p.time-- })
      this.spindlePrediction.history.push({ time: 0, real: clampedReal, pred: clampedPred })

      this.spindlePrediction.future.shift()
      this.spindlePrediction.future.forEach(p => { p.time-- })
      const basePred = clampedPred + (Math.random() - 0.5) * 0.001
      const fp = Math.max(0.038, Math.min(0.052, basePred))
      const idx = this.spindlePrediction.future.length + 1
      const confidence = 0.001 + idx * 0.0003
      this.spindlePrediction.future.push({
        time: 18,
        pred: fp,
        lower: Math.max(0.035, fp - confidence),
        upper: Math.min(0.055, fp + confidence)
      })
    },
    syncDeviationData() {
      let idx = 0
      this.errorAnalysisData.forEach(subsystem => {
        subsystem.params.forEach(param => {
          if (this.deviationData[idx]) {
            this.deviationData[idx].value = param.error
          }
          idx++
        })
      })
    },
    getDeviationBarClass(value) {
      if (value < 1) return 'bar-normal'
      if (value < 3) return 'bar-warning'
      return 'bar-danger'
    },
    getBarHeight(value) {
      const { max } = this.chartYAxisConfig
      const pct = (value / max) * 100
      return Math.max(5, Math.min(100, pct))
    },
    getParamClass(param) {
      if (param.value > param.max) return 'param-danger'
      if (param.value > param.max * 0.9) return 'param-warning'
      return ''
    },
    getPercent(param) {
      return Math.min(100, Math.max(0, (param.value / param.max) * 100))
    },
    getRealtimeBarClass(param) {
      const pct = (param.value / param.max) * 100
      if (pct > 100) return 'bar-danger'
      if (pct > 90) return 'bar-warning'
      if (pct > 70) return 'bar-normal'
      return 'bar-low'
    },
    getErrorRowClass(error) {
      if (error < 1) return 'error-normal';
      if (error < 3) return 'error-warning';
      return 'error-danger';
    },
    getErrorCellClass(error) {
      if (error < 1) return 'cell-error-normal';
      if (error < 3) return 'cell-error-warning';
      return 'cell-error-danger';
    },
    getMaeClass(mae) {
      if (mae < 1) return 'mae-excellent'
      if (mae < 3) return 'mae-good'
      if (mae < 5) return 'mae-warning'
      return 'mae-poor'
    },
    getMaeRange(mae) {
      if (mae < 1) return '优秀'
      if (mae < 3) return '良好'
      if (mae < 5) return '一般'
      return '较差'
    },
    getMseClass(mse) {
      if (mse < 2) return 'mae-excellent'
      if (mse < 5) return 'mae-good'
      if (mse < 8) return 'mae-warning'
      return 'mae-poor'
    },
    getMsePercent(mse) {
      const quality = 1 - mse / 10
      return Math.max(0, Math.min(100, Math.round(quality * 100)))
    },
    getMotorBarPercent(motor) {
      const denom = motor.maxCurrent - motor.minCurrent
      if (!denom) return 50
      const r = (motor.current - motor.minCurrent) / denom
      return Math.max(0, Math.min(100, r * 100))
    },
    getTrendColor(index) {
      const mae = this.maeHistory[index] || 5
      if (mae < 1) return '#00ff88'
      if (mae < 3) return '#4a90d9'
      if (mae < 5) return '#ffa500'
      return '#ff4444'
    },
    getPointColor(mae) {
      if (mae < 1) return '#00ff88'
      if (mae < 3) return '#4a90d9'
      if (mae < 5) return '#ffa500'
      return '#ff4444'
    },
    getErrorClass(error) {
      if (error < 1) return 'error-normal'
      if (error < 3) return 'error-warning'
      return 'error-danger'
    },
    formatValue(val) {
      if (val >= 1000) {
        return val.toFixed(1)
      } else if (val >= 100) {
        return val.toFixed(2)
      } else if (val >= 10) {
        return val.toFixed(3)
      } else if (val >= 1) {
        return val.toFixed(4)
      } else {
        return val.toFixed(4)
      }
    },
    copyErrorTable() {
      const table = document.getElementById('errorAnalysisTable')
      if (!table) return
      
      const rows = table.querySelectorAll('tr')
      let text = ''
      
      rows.forEach(row => {
        const cells = row.querySelectorAll('th, td')
        const rowData = []
        cells.forEach(cell => {
          let textContent = cell.textContent?.trim() || ''
          textContent = textContent.replace(/[\r\n]+/g, ' ').replace(/\s+/g, ' ')
          rowData.push(textContent)
        })
        text += rowData.join('\t') + '\n'
      })
      
      navigator.clipboard.writeText(text).then(() => {
        this.copySuccess = true
        setTimeout(() => {
          this.copySuccess = false
        }, 2000)
      }).catch(err => {
        console.error('复制失败:', err)
      })
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
  width: 100%;
  height: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 8px;
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
  height: 38px;
  background: linear-gradient(180deg, rgba(20, 35, 65, 0.98), rgba(15, 28, 55, 0.95));
  border-bottom: 1px solid rgba(0, 191, 255, 0.1);
}

.border-bottom {
  display: flex;
  align-items: center;
  height: 16px;
  background: linear-gradient(180deg, rgba(15, 28, 55, 0.95), rgba(10, 20, 40, 0.98));
  border-top: 1px solid rgba(0, 191, 255, 0.1);
  position: relative;
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

.decoration {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 100%;
  padding: 0 6px;
}

.decoration.left {
  padding-right: 6px;
}

.decoration.right {
  padding-left: 6px;
}

.d-block {
  width: 3px;
  height: 14px;
  background: linear-gradient(180deg, rgba(0, 191, 255, 0.6), rgba(102, 126, 234, 0.4));
  border-radius: 1px;
}

.title-bar {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  height: 100%;
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

.title-text {
  font-size: 13px;
  font-weight: 600;
  color: #00d4ff;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
  margin: 0;
  white-space: nowrap;
}

.border-body {
  flex: 1;
  display: flex;
  position: relative;
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

.device-model-content {
  height: 100%;
  display: flex;
  align-items: stretch;
  padding: 6px;
  box-sizing: border-box;
}

.device-model-split {
  height: 100%;
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: stretch;
}

.device-model-box {
  flex: 1 1 58%;
  min-width: 0;
}

.prediction-performance-box {
  flex: 1 1 42%;
  min-width: 0;
}

.device-info-card {
  flex: 1;
  background: rgba(0, 100, 180, 0.08);
  border-radius: 4px;
  padding: 12px;
  min-width: 0;
  height: 100%;
  box-sizing: border-box;
}

.device-info-card.compact {
  padding: 8px;
}

.info-grid {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr;
  grid-auto-rows: minmax(0, 1fr);
  gap: 4px;
}

.info-label {
  font-size: 11px;
  color: rgba(180, 210, 240, 0.7);
  letter-spacing: 1px;
}

.info-value {
  font-size: 12px;
  font-weight: 600;
  color: #a8d8ff;
  text-shadow: 0 0 6px rgba(168, 216, 255, 0.4);
}

.info-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 2px 2px;
  border: none;
  background: transparent;
  border-radius: 0;
  min-width: 0;
}

.info-item .info-value {
  white-space: nowrap;
  overflow: visible;
  text-overflow: clip;
  max-width: none;
  text-align: right;
  line-height: 1.1;
}

.perf-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  box-sizing: border-box;
}

.perf-top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
}

.perf-label {
  font-size: 11px;
  color: rgba(180, 210, 240, 0.7);
  letter-spacing: 1px;
}

.perf-value {
  font-size: 20px;
  font-weight: 700;
  font-family: monospace;
}

.perf-battery {
  justify-content: center;
  flex-direction: column;
  gap: 6px;
}

.chart-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-body-area {
  flex: 1;
  min-height: 0;
  position: relative;
  display: flex;
  flex-direction: column;
}

.chart-y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: absolute;
  left: 4px;
  top: 8px;
  bottom: 24px;
  font-size: 10px;
  color: rgba(0, 191, 255, 0.5);
  z-index: 2;
  pointer-events: none;
}

.chart-bars {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: stretch;
  justify-content: space-around;
  padding: 8px 10px 24px 36px;
  gap: 6px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 60px;
  min-width: 0;
  height: 100%;
}

.bar-track {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  overflow: hidden;
}

.bar-fill {
  width: 60%;
  max-width: 36px;
  min-height: 3px;
  border-radius: 3px 3px 0 0;
  height: var(--bar-h, 0%);
  transition: height 0.5s ease;
}

.bar-tooltip {
  position: absolute;
  top: auto;
  bottom: min(calc(var(--bar-h, 0%) + 10px), calc(100% - 12px));
  left: 50%;
  transform: translateX(-50%);
  font-size: 9px;
  color: #fff;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s;
  background: rgba(0, 0, 0, 0.8);
  padding: 2px 5px;
  border-radius: 2px;
  pointer-events: none;
  z-index: 3;
}

.bar-track:hover .bar-tooltip {
  opacity: 1;
}

.bar-normal {
  background: linear-gradient(180deg, #00ff88, #00cc6a);
  box-shadow: 0 0 8px rgba(0, 255, 136, 0.4);
}

.bar-warning {
  background: linear-gradient(180deg, #ffab40, #ff9100);
  box-shadow: 0 0 8px rgba(255, 171, 64, 0.4);
}

.bar-danger {
  background: linear-gradient(180deg, #ff5252, #d32f2f);
  box-shadow: 0 0 8px rgba(255, 82, 82, 0.4);
}

.bar-label {
  font-size: 9px;
  color: rgba(0, 191, 255, 0.7);
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  text-align: center;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 8px;
  border-top: 1px solid rgba(0, 191, 255, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  color: rgba(255, 255, 255, 0.7);
}

.legend-color {
  width: 12px;
  height: 8px;
  border-radius: 2px;
}

.legend-color.normal {
  background: linear-gradient(180deg, #00ff88, #00cc6a);
}

.legend-color.warning {
  background: linear-gradient(180deg, #ffab40, #ff9100);
}

.legend-color.danger {
  background: linear-gradient(180deg, #ff5252, #d32f2f);
}

.realtime-data-container {
  display: flex;
  flex-direction: row;
  gap: 4px;
  height: 100%;
}

.subsystem-group {
  flex: 1;
  min-width: 0;
  height: 100%;
  background: linear-gradient(180deg, rgba(0, 100, 180, 0.12), rgba(0, 60, 120, 0.06));
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 4px;
  padding: 4px 5px;
  display: flex;
  flex-direction: column;
  transition: border-color 0.3s;
  box-sizing: border-box;
  overflow: hidden;
}

.subsystem-group:hover {
  border-color: rgba(0, 191, 255, 0.3);
}

.subsystem-title {
  font-size: 15px;
  font-weight: 600;
  color: #87ceeb;
  padding-bottom: 4px;
  margin-bottom: 3px;
  border-bottom: 1px solid rgba(0, 191, 255, 0.15);
  text-align: center;
  white-space: nowrap;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  flex-shrink: 0;
}

.subsystem-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #00ff88;
  box-shadow: 0 0 4px rgba(0, 255, 136, 0.6);
}

.dot-0 { background: #00ff88; box-shadow: 0 0 4px rgba(0, 255, 136, 0.6); }
.dot-1 { background: #00d4ff; box-shadow: 0 0 4px rgba(0, 212, 255, 0.6); }
.dot-2 { background: #ffa500; box-shadow: 0 0 4px rgba(255, 165, 0, 0.6); }
.dot-3 { background: #a855f7; box-shadow: 0 0 4px rgba(168, 85, 247, 0.6); }

.data-table {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
  min-height: 0;
}

.data-cell {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-rows: 1fr auto auto;
  align-items: center;
  padding: 3px 5px;
  background: rgba(0, 0, 0, 0.25);
  border-radius: 3px;
  border-left: 2px solid rgba(0, 191, 255, 0.2);
  transition: background 0.2s, border-color 0.2s;
  gap: 0 4px;
  box-sizing: border-box;
  overflow: hidden;
}

.data-cell:hover {
  background: rgba(0, 100, 180, 0.15);
  border-left-color: rgba(0, 191, 255, 0.5);
}

.cell-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.55);
  grid-column: 1;
  grid-row: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cell-value {
  font-size: 15px;
  font-weight: 700;
  color: #00ff88;
  grid-column: 2;
  grid-row: 1 / 3;
  text-align: right;
  font-family: 'Courier New', monospace;
}

.cell-value.param-warning {
  color: #ffa500;
  text-shadow: 0 0 4px rgba(255, 165, 0, 0.3);
}

.cell-value.param-danger {
  color: #ff4444;
  text-shadow: 0 0 4px rgba(255, 68, 68, 0.3);
}

.cell-unit {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.3);
  grid-column: 1;
  grid-row: 2;
}

.cell-bar {
  grid-column: 1 / 3;
  grid-row: 3;
  height: 3px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 1px;
  margin-top: 2px;
  overflow: hidden;
}

.cell-bar-fill {
  height: 100%;
  border-radius: 1px;
  transition: width 0.6s ease;
}

.cell-bar-fill.bar-low {
  background: linear-gradient(90deg, #00ff88, #00cc6a);
}

.cell-bar-fill.bar-normal {
  background: linear-gradient(90deg, #00d4ff, #0099cc);
}

.cell-bar-fill.bar-warning {
  background: linear-gradient(90deg, #ffa500, #ff8c00);
}

.cell-bar-fill.bar-danger {
  background: linear-gradient(90deg, #ff4444, #cc0000);
}

.error-analysis-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 2px;
  box-sizing: border-box;
  gap: 2px;
}

.error-table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2px;
}

.error-table-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #00d4ff;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
}

.title-icon {
  width: 16px;
  height: 16px;
  opacity: 0.8;
}

.error-table-actions {
  display: flex;
  gap: 8px;
}

.copy-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  background: rgba(0, 150, 255, 0.15);
  border: 1px solid rgba(0, 191, 255, 0.3);
  border-radius: 4px;
  color: #87ceeb;
  font-size: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.copy-btn:hover {
  background: rgba(0, 150, 255, 0.25);
  border-color: rgba(0, 191, 255, 0.5);
}

.copy-btn.copied {
  background: rgba(0, 255, 136, 0.15);
  border-color: rgba(0, 255, 136, 0.4);
  color: #00ff88;
}

.copy-btn svg {
  width: 12px;
  height: 12px;
}

.error-table-description {
  font-size: 10px;
  color: rgba(148, 163, 184, 0.7);
  padding: 0 4px;
  letter-spacing: 0.3px;
}

.error-table-container {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  border: 1px solid rgba(0, 191, 255, 0.2);
  border-radius: 6px;
  background: linear-gradient(180deg, rgba(8, 20, 40, 0.95), rgba(5, 15, 30, 0.92));
  min-height: 0;
  display: flex;
}

.error-analysis-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
  table-layout: fixed;
  height: 100%;
}

.error-analysis-table thead {
  position: sticky;
  top: 0;
  z-index: 2;
  background: linear-gradient(180deg, rgba(20, 60, 120, 0.98), rgba(15, 45, 90, 0.95));
}

.error-analysis-table th,
.error-analysis-table td {
  border: 1px solid rgba(0, 191, 255, 0.14);
}

.error-analysis-table thead th {
  border-color: rgba(0, 191, 255, 0.28);
}

.error-analysis-table tbody {
  background: linear-gradient(180deg, rgba(10, 30, 60, 0.9), rgba(8, 25, 50, 0.85));
}

.error-analysis-table tbody tr {
  height: 33.333%;
}

.row-subsystem th {
  background: linear-gradient(180deg, rgba(30, 80, 160, 0.95), rgba(20, 60, 120, 0.9));
  border-bottom: 1px solid rgba(0, 191, 255, 0.35);
}

.col-indicator {
  width: 60px;
  min-width: 60px;
  color: #00d4ff;
  font-weight: 700;
  font-size: 12px;
  text-align: center;
  vertical-align: middle;
  padding: 8px 4px;
  border-right: 1px solid rgba(0, 191, 255, 0.25);
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
}

.col-subsystem {
  text-align: center;
  color: #ffffff;
  font-weight: 700;
  font-size: 11px;
  padding: 8px 3px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  background: linear-gradient(180deg, rgba(0, 130, 220, 0.35), rgba(0, 100, 180, 0.25));
  border-right: 1px solid rgba(0, 191, 255, 0.15);
}

.col-subsystem:last-of-type {
  border-right: none;
}

.subsystem-name {
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.row-param th {
  background: rgba(0, 100, 180, 0.35);
  border-bottom: 1px solid rgba(0, 191, 255, 0.2);
}

.col-param {
  text-align: center;
  color: #00d4ff;
  font-weight: 600;
  font-size: 11px;
  padding: 6px 2px;
  letter-spacing: 0.3px;
  background: rgba(0, 80, 150, 0.25);
  border-right: 1px solid rgba(0, 191, 255, 0.12);
}

.col-param:last-child {
  border-right: none;
}

.row-actual td:first-child,
.row-predicted td:first-child,
.row-error td:first-child {
  border-right: 1px solid rgba(0, 191, 255, 0.2);
}

.row-actual:hover,
.row-predicted:hover,
.row-error:hover {
  background: rgba(0, 150, 255, 0.08);
}

.row-actual:hover td,
.row-predicted:hover td,
.row-error:hover td {
  background: rgba(0, 150, 255, 0.05);
}

.row-alt {
  background: rgba(0, 50, 100, 0.15);
}

.row-alt:hover {
  background: rgba(0, 150, 255, 0.12) !important;
}

.col-indicator-label {
  color: #87ceeb;
  font-weight: 700;
  font-size: 12px;
  padding: 8px 4px;
  text-align: center;
  width: 70px;
  min-width: 70px;
  background: rgba(0, 80, 150, 0.3);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  border-bottom: 1px solid rgba(0, 191, 255, 0.12);
}

.col-value {
  color: #e0f4ff;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 11px;
  font-weight: 500;
  text-align: left;
  padding: 8px 6px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(0, 191, 255, 0.08);
  transition: all 0.2s ease;
  line-height: 1.2;
}

.col-value:hover {
  background: rgba(0, 150, 255, 0.15);
  color: #ffffff;
}

.col-error {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 11px;
  font-weight: 700;
  text-align: left;
  padding: 8px 6px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(0, 191, 255, 0.08);
  transition: all 0.2s ease;
  white-space: nowrap;
  line-height: 1.2;
}

.col-error:hover {
  background: rgba(0, 150, 255, 0.12);
}

.error-normal {
  color: #00ff88;
  text-shadow: 0 0 8px rgba(0, 255, 136, 0.5);
}

.error-warning {
  color: #ffab40;
  text-shadow: 0 0 8px rgba(255, 171, 64, 0.5);
}

.error-danger {
  color: #ff5252;
  text-shadow: 0 0 8px rgba(255, 82, 82, 0.5);
}

.error-table-footer {
  display: flex;
  justify-content: center;
  padding: 2px;
}

.error-legend {
  display: flex;
  gap: 12px;
  font-size: 9px;
  color: rgba(148, 163, 184, 0.8);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.legend-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.legend-dot.normal {
  background: #00ff88;
  box-shadow: 0 0 4px rgba(0, 255, 136, 0.5);
}

.legend-dot.warning {
  background: #ffab40;
  box-shadow: 0 0 4px rgba(255, 171, 64, 0.5);
}

.legend-dot.danger {
  background: #ff5252;
  box-shadow: 0 0 4px rgba(255, 82, 82, 0.5);
}

@keyframes pulse-warning {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.2); }
}

@keyframes pulse-danger {
  0%, 100% { opacity: 1; box-shadow: 0 0 6px rgba(255, 82, 82, 0.6); }
  50% { opacity: 0.7; box-shadow: 0 0 12px rgba(255, 82, 82, 0.9); }
}

@media (max-width: 900px) {
  .error-analysis-table {
    font-size: 10px;
  }

  .col-indicator,
  .col-indicator-label {
    width: 55px;
    min-width: 55px;
    padding: 6px 4px;
  }

  .col-subsystem {
    padding: 6px 2px;
    font-size: 10px;
  }

  .col-param {
    padding: 4px 2px;
    font-size: 10px;
  }

  .col-value,
  .col-error {
    padding: 6px 4px;
  }

  .error-table-header {
    flex-direction: column;
    gap: 4px;
    align-items: flex-start;
  }

  .error-legend {
    flex-wrap: wrap;
    gap: 8px;
  }

  .device-model-content {
    padding: 4px;
  }

  .device-info-card {
    padding: 8px;
  }

  .device-model-split {
    flex-direction: column;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .prediction-chart-container {
    padding: 0;
  }

  .chart-header {
    flex-direction: column;
    gap: 2px;
    align-items: flex-start;
    padding: 2px 4px;
  }

  .chart-legend {
    gap: 6px;
    flex-wrap: wrap;
  }

  .chart-y-axis-spindle span {
    font-size: 7px;
  }

  .axis-labels span {
    font-size: 7px;
  }
}

.prediction-chart-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  box-sizing: border-box;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 6px;
  flex-shrink: 0;
}

.chart-title {
  font-size: 11px;
  color: #00d4ff;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 0 0 8px rgba(0, 212, 255, 0.4);
}

.chart-legend {
  display: flex;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 9px;
  color: rgba(200, 220, 240, 0.9);
}

.legend-line {
  width: 16px;
  height: 2px;
  border-radius: 1px;
}

.legend-line.real-line {
  background: linear-gradient(90deg, #00ff88, #00cc6a);
  box-shadow: 0 0 4px rgba(0, 255, 136, 0.5);
}

.legend-line.history-pred-line {
  background: repeating-linear-gradient(90deg, #00d4ff, #00d4ff 3px, transparent 3px, transparent 5px);
  box-shadow: 0 0 4px rgba(0, 212, 255, 0.3);
}

.legend-line.future-pred-line {
  background: linear-gradient(90deg, #a855f7, #7c3aed);
  box-shadow: 0 0 4px rgba(168, 85, 247, 0.5);
}

.chart-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  min-height: 0;
}

.chart-y-axis-spindle {
  position: absolute;
  left: 0;
  top: 6%;
  width: 7%;
  height: 82%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 2;
  pointer-events: none;
}

.chart-y-axis-spindle span {
  font-size: 8px;
  color: rgba(0, 191, 255, 0.85);
  text-align: right;
  width: 100%;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  text-shadow: 0 0 4px rgba(0, 191, 255, 0.3);
  line-height: 1;
}

.prediction-svg {
  width: 100%;
  flex: 1;
  min-height: 0;
  overflow: visible;
}

.chart-axis {
  position: relative;
  height: 18px;
  flex-shrink: 0;
}

.axis-labels {
  position: relative;
  width: 100%;
  height: 100%;
}

.axis-labels span {
  position: absolute;
  font-size: 8px;
  color: rgba(0, 191, 255, 0.75);
  transform: translateX(-50%);
  white-space: nowrap;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

.mae-label {
  font-size: 12px;
  color: rgba(180, 210, 240, 0.7);
  letter-spacing: 1px;
}

.mae-value {
  font-size: 28px;
  font-weight: 700;
  font-family: monospace;
}

.mae-excellent {
  color: #00ff88;
  text-shadow: 0 0 15px rgba(0, 255, 136, 0.6);
}

.mae-good {
  color: #4a90d9;
  text-shadow: 0 0 15px rgba(74, 144, 217, 0.6);
}

.mae-warning {
  color: #ffa500;
  text-shadow: 0 0 15px rgba(255, 165, 0, 0.6);
}

.mae-poor {
  color: #ff4444;
  text-shadow: 0 0 15px rgba(255, 68, 68, 0.6);
}

.battery-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 6px;
}

.battery-outline {
  width: 110px;
  height: 190px;
  border: 2px solid rgba(0, 191, 255, 0.40);
  border-radius: 12px;
  padding: 8px;
  background: rgba(0, 0, 0, 0.20);
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 0 22px rgba(0, 0, 0, 0.5);
}

.battery-fill {
  position: absolute;
  left: 8px;
  right: 8px;
  bottom: 8px;
  border-radius: 8px;
  transition: height 0.5s ease;
  opacity: 0.88;
}

.battery-fill.mae-excellent {
  background: linear-gradient(0deg, rgba(0, 255, 136, 0.95), rgba(0, 204, 106, 0.55));
}

.battery-fill.mae-good {
  background: linear-gradient(0deg, rgba(74, 144, 217, 0.95), rgba(33, 118, 199, 0.55));
}

.battery-fill.mae-warning {
  background: linear-gradient(0deg, rgba(255, 165, 0, 0.95), rgba(255, 140, 0, 0.55));
}

.battery-fill.mae-poor {
  background: linear-gradient(0deg, rgba(255, 68, 68, 0.95), rgba(204, 0, 0, 0.55));
}

.battery-cap {
  width: 40px;
  height: 10px;
  background: rgba(0, 191, 255, 0.28);
  border: 2px solid rgba(0, 191, 255, 0.40);
  border-bottom: none;
  border-radius: 6px 6px 0 0;
}

.battery-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-family: monospace;
  pointer-events: none;
}

.battery-text-title {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  color: rgba(200, 240, 255, 0.82);
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.25);
}

.battery-text-value {
  font-size: 18px;
  font-weight: 800;
  color: rgba(235, 250, 255, 0.95);
  text-shadow: 0 0 12px rgba(0, 212, 255, 0.32);
}

.mae-range {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
}

.trend-chart {
  width: 100%;
  padding: 8px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.trend-label {
  font-size: 10px;
  color: rgba(0, 191, 255, 0.6);
  margin-bottom: 4px;
}

.trend-svg {
  width: 100%;
  height: 60px;
}

.motor-current-container {
  height: 100%;
  overflow: hidden;
}

.motor-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 5px;
  padding: 4px 6px;
  height: 100%;
}

.motor-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 5px 8px;
  background: linear-gradient(135deg, rgba(10, 25, 50, 0.9), rgba(15, 30, 55, 0.8));
  border: 1px solid rgba(0, 180, 255, 0.18);
  border-radius: 6px;
  transition: all 0.3s ease;
  min-height: 0;
}

.motor-item:hover {
  border-color: rgba(0, 200, 255, 0.45);
  background: linear-gradient(135deg, rgba(10, 30, 60, 0.95), rgba(15, 35, 65, 0.85));
}

.motor-alert {
  border-color: rgba(255, 80, 80, 0.35);
  background: linear-gradient(135deg, rgba(40, 10, 15, 0.85), rgba(50, 15, 20, 0.75));
}

.motor-alert:hover {
  border-color: rgba(255, 80, 80, 0.6);
}

.motor-header {
  display: flex;
  align-items: center;
  gap: 5px;
}

.motor-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00d4ff;
  box-shadow: 0 0 6px rgba(0, 212, 255, 0.5);
  flex-shrink: 0;
}

.motor-dot.dot-alert {
  background: #ff4757;
  box-shadow: 0 0 8px rgba(255, 71, 87, 0.6);
  animation: blink-dot 1s ease-in-out infinite;
}

.motor-number {
  font-size: 12px;
  font-weight: 700;
  color: #e2e8f0;
  flex: 1;
}

.motor-status {
  font-size: 9px;
  padding: 1px 6px;
  border-radius: 3px;
  font-weight: 600;
}

.status-ok {
  color: #00ff99;
  background: rgba(0, 255, 153, 0.08);
  border: 1px solid rgba(0, 255, 153, 0.2);
}

.status-alert {
  color: #ff4757;
  background: rgba(255, 71, 87, 0.1);
  border: 1px solid rgba(255, 71, 87, 0.25);
}

.motor-value {
  font-size: 22px;
  font-weight: 800;
  color: #00ffcc;
  font-family: 'Consolas', monospace;
  text-align: center;
  line-height: 1;
  text-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
}

.motor-value small {
  font-size: 12px;
  font-weight: 400;
  color: rgba(0, 255, 204, 0.5);
  margin-left: 2px;
}

.value-alert {
  color: #ff6b6b;
  text-shadow: 0 0 10px rgba(255, 107, 107, 0.4);
}

.value-alert small {
  color: rgba(255, 107, 107, 0.5);
}

.motor-bar-wrap {
  margin-top: auto;
}

.motor-bar-range {
  display: flex;
  justify-content: space-between;
  font-size: 8px;
  color: rgba(148, 163, 184, 0.5);
  margin-bottom: 2px;
  padding: 0 1px;
}

.motor-bar {
  position: relative;
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: visible;
}

.motor-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

.fill-ok {
  background: linear-gradient(90deg, #00d4ff, #00ff88);
  box-shadow: 0 0 6px rgba(0, 255, 136, 0.3);
}

.fill-alert {
  background: linear-gradient(90deg, #ff6b6b, #ff4757);
  box-shadow: 0 0 6px rgba(255, 71, 87, 0.4);
}

.motor-bar-dot {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: #fff;
  border-radius: 50%;
  border: 2px solid #00d4ff;
  box-shadow: 0 0 6px rgba(0, 212, 255, 0.5);
  transition: left 0.5s ease;
}

.motor-bar-dot.dot-alert {
  border-color: #ff4757;
  box-shadow: 0 0 6px rgba(255, 71, 87, 0.6);
}

@keyframes blink-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

@media (max-width: 1400px) {
  .motor-grid {
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(5, 1fr);
  }
}
</style>
