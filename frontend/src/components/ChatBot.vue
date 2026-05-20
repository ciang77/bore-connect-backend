<script setup lang="ts">
import { ref, nextTick, onUnmounted, watch } from 'vue'

const open = ref(false)
const model = ref('qwen')
const input = ref('')
const sending = ref(false)
const status = ref('')
const messages = ref<{ role: 'user' | 'assistant'; content: string }[]>([])

let controller: AbortController | null = null

const widgetPos = ref({ x: 0, y: 0 })
const isDragging = ref(false)
const hasDragged = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const dragOffset = ref({ x: 0, y: 0 })
const snapSide = ref<'left' | 'right'>('right')

const chatSize = ref({ w: 400, h: 560 })
const isResizing = ref(false)
const resizeStart = ref({ x: 0, y: 0 })
const resizeOffset = ref({ w: 0, h: 0 })

const models = [
  { value: 'qwen', label: 'Qwen 3.6' },
  { value: 'deepseek', label: 'DeepSeek V4' },
]

// ── drag logic ──
function onDragStart(e: MouseEvent | TouchEvent) {
  isDragging.value = true
  hasDragged.value = false
  const p = 'touches' in e ? e.touches[0] : e
  dragStart.value = { x: p.clientX, y: p.clientY }
  dragOffset.value = { x: widgetPos.value.x, y: widgetPos.value.y }
  document.addEventListener('mousemove', onDragMove)
  document.addEventListener('mouseup', onDragEnd)
  document.addEventListener('touchmove', onDragMove, { passive: false })
  document.addEventListener('touchend', onDragEnd)
}

function onDragMove(e: MouseEvent | TouchEvent) {
  if (!isDragging.value) return
  e.preventDefault()
  const p = 'touches' in e ? e.touches[0] : e
  const dx = p.clientX - dragStart.value.x
  const dy = p.clientY - dragStart.value.y
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) hasDragged.value = true
  widgetPos.value = {
    x: dragOffset.value.x + dx,
    y: dragOffset.value.y + dy,
  }
}

function onDragEnd() {
  isDragging.value = false
  document.removeEventListener('mousemove', onDragMove)
  document.removeEventListener('mouseup', onDragEnd)
  document.removeEventListener('touchmove', onDragMove)
  document.removeEventListener('touchend', onDragEnd)
}

// ── snap to nearest edge ──
function snapToEdge() {
  const viewportCenter = window.innerWidth / 2
  const btnActualX = window.innerWidth + widgetPos.value.x - 30
  if (btnActualX < viewportCenter) {
    snapSide.value = 'left'
    widgetPos.value = { x: 20 - window.innerWidth, y: widgetPos.value.y }
  } else {
    snapSide.value = 'right'
    widgetPos.value = { x: -20, y: widgetPos.value.y }
  }
}

function initPosition() {
  widgetPos.value = { x: -20, y: -20 }
  snapSide.value = 'right'
}
initPosition()

// ── resize logic ──
function onResizeStart(e: MouseEvent | TouchEvent) {
  isResizing.value = true
  const p = 'touches' in e ? e.touches[0] : e
  resizeStart.value = { x: p.clientX, y: p.clientY }
  resizeOffset.value = { w: chatSize.value.w, h: chatSize.value.h }
  document.addEventListener('mousemove', onResizeMove)
  document.addEventListener('mouseup', onResizeEnd)
  document.addEventListener('touchmove', onResizeMove, { passive: false })
  document.addEventListener('touchend', onResizeEnd)
  e.preventDefault()
}

function onResizeMove(e: MouseEvent | TouchEvent) {
  if (!isResizing.value) return
  const p = 'touches' in e ? e.touches[0] : e
  const dx = p.clientX - resizeStart.value.x
  const dy = p.clientY - resizeStart.value.y
  chatSize.value = {
    w: Math.max(300, Math.min(800, resizeOffset.value.w + dx)),
    h: Math.max(400, Math.min(window.innerHeight - 80, resizeOffset.value.h + dy)),
  }
}

function onResizeEnd() {
  isResizing.value = false
  document.removeEventListener('mousemove', onResizeMove)
  document.removeEventListener('mouseup', onResizeEnd)
  document.removeEventListener('touchmove', onResizeMove)
  document.removeEventListener('touchend', onResizeEnd)
}

// ── chat logic ──
function abort() {
  if (controller) {
    controller.abort()
    controller = null
  }
}

async function send() {
  const text = input.value.trim()
  if (!text || sending.value) return

  abort()
  input.value = ''
  status.value = ''
  sending.value = true

  messages.value.push({ role: 'user', content: text })
  const aiIdx = messages.value.length
  messages.value.push({ role: 'assistant', content: '' })

  await nextTick()
  scrollBottom()

  controller = new AbortController()

  try {
    const resp = await fetch('/api/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question: text,
        model: model.value,
        temperature: 0.2,
        max_tokens: 2048,
      }),
      signal: controller.signal,
    })

    if (!resp.ok) {
      status.value = `请求失败 (${resp.status})`
      messages.value.pop()
      messages.value.pop()
      sending.value = false
      return
    }

    const reader = resp.body!.getReader()
    const decoder = new TextDecoder()
    let buf = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buf += decoder.decode(value, { stream: true })
      const lines = buf.split('\n')
      buf = lines.pop()!

      for (const line of lines) {
        if (!line) continue
        try {
          const data = JSON.parse(line)
          if (data.done) return
          if (data.delta) messages.value[aiIdx].content += data.delta
        } catch { /* skip */ }
      }
    }

    if (buf) {
      try {
        const data = JSON.parse(buf)
        if (!data.done && data.delta) messages.value[aiIdx].content += data.delta
      } catch { /* skip */ }
    }
  } catch (err: any) {
    if (err.name === 'AbortError') return
    status.value = '连接异常或中断'
  } finally {
    controller = null
    sending.value = false
  }
}

function stop() {
  status.value = '已停止'
  abort()
  sending.value = false
}

function scrollBottom() {
  nextTick(() => {
    const el = document.getElementById('msg-area')
    if (el) el.scrollTop = el.scrollHeight
  })
}

function toggleOpen() {
  if (hasDragged.value) return
  open.value = !open.value
  if (open.value) scrollBottom()
}

watch(open, (val) => {
  if (!val) snapToEdge()
})

// esc to close
function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && open.value) open.value = false
}
window.addEventListener('keydown', onKeydown)

onUnmounted(() => {
  abort()
  window.removeEventListener('keydown', onKeydown)
  document.removeEventListener('mousemove', onDragMove)
  document.removeEventListener('mouseup', onDragEnd)
  document.removeEventListener('mousemove', onResizeMove)
  document.removeEventListener('mouseup', onResizeEnd)
})
</script>

<template>
  <div
    class="widget-root"
    :class="{ dragging: isDragging }"
    :style="{ transform: `translate(${widgetPos.x}px, ${widgetPos.y}px)` }"
  >
    <!-- Chat Window -->
    <Transition name="pop">
      <div
        v-if="open"
        class="chat-window"
        :class="snapSide"
        :style="{ width: chatSize.w + 'px', height: chatSize.h + 'px' }"
      >
        <!-- Header (drag handle) -->
        <div class="chat-header" @mousedown="onDragStart" @touchstart.prevent="onDragStart">
          <span class="chat-title">AI 助手</span>
          <div class="header-actions">
            <select
              v-model="model"
              class="model-select"
              @mousedown.stop
              @touchstart.stop
            >
              <option v-for="m in models" :key="m.value" :value="m.value">
                {{ m.label }}
              </option>
            </select>
            <button class="btn-close" @click="open = false" title="关闭 (Esc)">&times;</button>
          </div>
        </div>

        <!-- Messages -->
        <div id="msg-area" class="msg-area">
          <div v-if="messages.length === 0" class="empty-hint">
            👋 有什么可以帮你的？
          </div>
          <div
            v-for="(msg, i) in messages"
            :key="i"
            :class="['msg', msg.role]"
          >
            <div class="msg-content">{{ msg.content }}</div>
          </div>
          <div v-if="status" class="status-line">{{ status }}</div>
        </div>

        <!-- Input -->
        <div class="input-area">
          <input
            v-model="input"
            placeholder="输入问题，Enter 发送..."
            @keyup.enter="send"
            :disabled="sending"
          />
          <button class="btn-send" :disabled="sending" @click="send">发送</button>
          <button v-if="sending" class="btn-stop" @click="stop">停</button>
        </div>

        <!-- Resize handle -->
        <div
          class="resize-handle"
          @mousedown="onResizeStart"
          @touchstart.prevent="onResizeStart"
        ></div>
      </div>
    </Transition>

    <!-- Floating button -->
    <button
      v-show="!open"
      class="float-btn"
      @mousedown.stop="onDragStart"
      @touchstart.stop.prevent="onDragStart"
      @click="toggleOpen"
    >
      <svg class="robot-icon-svg" viewBox="0 0 64 64" fill="none">
        <!-- 外轮廓 - 六边形 -->
        <path d="M32 4 L54 17 L54 43 L32 56 L10 43 L10 17 Z" stroke="white" stroke-width="2.5" fill="none" opacity="0.5"/>
        <!-- 内轮廓 -->
        <path d="M32 12 L48 22 L48 40 L32 50 L16 40 L16 22 Z" stroke="white" stroke-width="2" fill="none" opacity="0.8"/>
        <!-- 顶部信号线 -->
        <line x1="32" y1="2" x2="32" y2="12" stroke="white" stroke-width="2" stroke-linecap="round" opacity="0.7"/>
        <circle cx="32" cy="2" r="2.5" fill="white" opacity="0.9"/>
        <!-- 左信号线 -->
        <line x1="6" y1="20" x2="16" y2="22" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
        <circle cx="6" cy="20" r="1.5" fill="white" opacity="0.5"/>
        <!-- 右信号线 -->
        <line x1="58" y1="20" x2="48" y2="22" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
        <circle cx="58" cy="20" r="1.5" fill="white" opacity="0.5"/>
        <!-- 左眼 - 菱形 -->
        <path d="M24 28 L28 24 L32 28 L28 32 Z" fill="white" opacity="0.9"/>
        <!-- 右眼 - 菱形 -->
        <path d="M32 28 L36 24 L40 28 L36 32 Z" fill="white" opacity="0.9"/>
        <!-- 嘴巴 - 科技线条 -->
        <line x1="24" y1="39" x2="40" y2="39" stroke="white" stroke-width="2" stroke-linecap="round" opacity="0.7"/>
        <line x1="27" y1="42" x2="37" y2="42" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
        <!-- 底部连接线 -->
        <line x1="32" y1="56" x2="32" y2="60" stroke="white" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
        <circle cx="32" cy="61" r="1.5" fill="white" opacity="0.6"/>
      </svg>
    </button>
  </div>
</template>

<style scoped>
/* ── root ── */
.widget-root {
  position: fixed;
  bottom: 0;
  right: 0;
  z-index: 99999;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial,
    "PingFang SC", "Microsoft YaHei", sans-serif;
  transition: transform 0.3s ease;
}
.widget-root.dragging {
  transition: none;
}

/* ── float button ── */
.float-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #0a1628 0%, #1a2744 100%);
  box-shadow:
    0 0 20px rgba(0, 180, 255, 0.3),
    0 0 40px rgba(0, 180, 255, 0.1),
    inset 0 0 15px rgba(0, 180, 255, 0.1);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, box-shadow 0.2s;
  user-select: none;
  position: absolute;
  bottom: 0;
  right: 0;
}
.float-btn:hover {
  transform: scale(1.08);
  box-shadow:
    0 0 30px rgba(0, 180, 255, 0.5),
    0 0 60px rgba(0, 180, 255, 0.15),
    inset 0 0 20px rgba(0, 180, 255, 0.15);
}
.robot-icon-svg {
  width: 34px;
  height: 34px;
}

/* ── chat window ── */
.chat-window {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(16, 20, 48, 0.92);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(100, 126, 234, 0.2);
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.chat-window.left {
  right: auto;
  left: 8px;
}

/* ── resize handle ── */
.resize-handle {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  cursor: nwse-resize;
}
.resize-handle::after {
  content: '';
  position: absolute;
  bottom: 6px;
  right: 6px;
  width: 10px;
  height: 10px;
  border-right: 2px solid rgba(224, 230, 240, 0.3);
  border-bottom: 2px solid rgba(224, 230, 240, 0.3);
}
.resize-handle:hover::after {
  border-color: rgba(100, 126, 234, 0.6);
}

/* ── header ── */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  cursor: grab;
  user-select: none;
  flex-shrink: 0;
}
.chat-header:active {
  cursor: grabbing;
}
.chat-title {
  font-weight: 600;
  font-size: 15px;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.model-select {
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  font-size: 12px;
  cursor: pointer;
  outline: none;
}
.model-select option {
  color: #333;
  background: #fff;
}
.btn-close {
  background: none;
  border: none;
  color: #fff;
  font-size: 22px;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
  opacity: 0.8;
}
.btn-close:hover {
  opacity: 1;
}

/* ── messages ── */
.msg-area {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: transparent;
}
.empty-hint {
  text-align: center;
  color: rgba(224, 230, 240, 0.35);
  margin-top: 60px;
  font-size: 15px;
}
.msg {
  max-width: 85%;
}
.msg.user {
  align-self: flex-end;
}
.msg.user .msg-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 14px 14px 4px 14px;
}
.msg.assistant {
  align-self: flex-start;
}
.msg.assistant .msg-content {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(100, 126, 234, 0.2);
  border-radius: 14px 14px 14px 4px;
  color: #e0e6f0;
}
.msg-content {
  padding: 10px 14px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}
.status-line {
  text-align: center;
  color: rgba(224, 230, 240, 0.4);
  font-size: 12px;
}

/* ── input area ── */
.input-area {
  display: flex;
  gap: 6px;
  padding: 10px 12px;
  border-top: 1px solid rgba(100, 126, 234, 0.15);
  flex-shrink: 0;
  background: rgba(0, 0, 0, 0.2);
}
.input-area input {
  flex: 1;
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid rgba(100, 126, 234, 0.25);
  border-radius: 10px;
  outline: none;
  background: rgba(255, 255, 255, 0.06);
  color: #e0e6f0;
  transition: border-color 0.2s;
}
.input-area input::placeholder {
  color: rgba(224, 230, 240, 0.3);
}
.input-area input:focus {
  border-color: #667eea;
}
.btn-send,
.btn-stop {
  padding: 10px 16px;
  font-size: 13px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  white-space: nowrap;
}
.btn-send {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}
.btn-send:hover {
  opacity: 0.9;
}
.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-stop {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(224, 230, 240, 0.6);
}
.btn-stop:hover {
  background: rgba(255, 255, 255, 0.15);
}

/* ── transitions ── */
.pop-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pop-leave-active {
  transition: all 0.2s ease-in;
}
.pop-enter-from {
  opacity: 0;
  transform: scale(0.7) translateY(20px);
}
.pop-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(10px);
}
</style>
