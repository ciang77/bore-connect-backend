<script setup lang="ts">
import { ref, nextTick, onUnmounted, watch } from 'vue'
import clawdThinkingGif from './clawd-thinking.gif'

const open = ref(false)
const model = ref('qwen')
const input = ref('')
const sending = ref(false)
const status = ref('')
const messages = ref<{ role: 'user' | 'assistant'; content: string }[]>([])

let controller: AbortController | null = null

const widgetRoot = ref<HTMLElement | null>(null)
const widgetPos = ref({ x: 0, y: 0 })
const isDragging = ref(false)
const hasDragged = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const dragOffset = ref({ x: 0, y: 0 })
const snapSide = ref<'left' | 'right'>('right')
const dragThreshold = 8
const edgeMargin = 20
const floatButtonSize = { w: 256, h: 256 }
const chatInset = 8
let dragPointerId: number | null = null

const chatSize = ref({ w: 400, h: 560 })
const isResizing = ref(false)
const resizeStart = ref({ x: 0, y: 0 })
const resizeOffset = ref({ w: 0, h: 0 })
let resizePointerId: number | null = null

const models = [
  { value: 'qwen', label: 'Qwen 3.6' },
  { value: 'deepseek', label: 'DeepSeek V4' },
]

function getPoint(e: PointerEvent | MouseEvent | TouchEvent) {
  return 'touches' in e ? e.touches[0] : e
}

function getActiveBounds() {
  return open.value
    ? { width: chatSize.value.w, height: chatSize.value.h, inset: chatInset }
    : { width: floatButtonSize.w, height: floatButtonSize.h, inset: 0 }
}

function clampWidgetPos(nextX: number, nextY: number) {
  const bounds = getActiveBounds()
  const minX = edgeMargin + bounds.width + bounds.inset - window.innerWidth
  const maxX = bounds.inset - edgeMargin
  const minY = edgeMargin + bounds.height + bounds.inset - window.innerHeight
  const maxY = bounds.inset - edgeMargin

  return {
    x: Math.min(maxX, Math.max(minX, nextX)),
    y: Math.min(maxY, Math.max(minY, nextY)),
  }
}

function bindDragListeners() {
  window.addEventListener('pointermove', onDragMove)
  window.addEventListener('pointerup', onDragEnd, { capture: true })
  window.addEventListener('pointercancel', onDragEnd, { capture: true })
  window.addEventListener('blur', onDragEnd)
}

function unbindDragListeners() {
  window.removeEventListener('pointermove', onDragMove)
  window.removeEventListener('pointerup', onDragEnd, { capture: true })
  window.removeEventListener('pointercancel', onDragEnd, { capture: true })
  window.removeEventListener('blur', onDragEnd)
}

// ── drag logic ──
function onDragStart(e: PointerEvent) {
  if (e.button !== 0 && e.pointerType !== 'touch') return
  dragPointerId = e.pointerId
  isDragging.value = false
  hasDragged.value = false
  const p = getPoint(e)
  dragStart.value = { x: p.clientX, y: p.clientY }
  dragOffset.value = { x: widgetPos.value.x, y: widgetPos.value.y }
  bindDragListeners()
  ;(e.currentTarget as HTMLElement | null)?.setPointerCapture?.(e.pointerId)
}

function onDragMove(e: PointerEvent) {
  if (dragPointerId !== null && e.pointerId !== dragPointerId) return
  const p = getPoint(e)
  const dx = p.clientX - dragStart.value.x
  const dy = p.clientY - dragStart.value.y
  if (!isDragging.value && Math.abs(dx) < dragThreshold && Math.abs(dy) < dragThreshold) return

  e.preventDefault()
  isDragging.value = true
  hasDragged.value = true
  widgetPos.value = clampWidgetPos(dragOffset.value.x + dx, dragOffset.value.y + dy)
}

function onDragEnd() {
  dragPointerId = null
  unbindDragListeners()
  if (!isDragging.value && !hasDragged.value) return

  isDragging.value = false
  // 延迟重置 hasDragged，让 click 事件能读到拖拽状态
  setTimeout(() => {
    hasDragged.value = false
  }, 0)
}

// ── snap to nearest edge ──
function snapToEdge() {
  const viewportCenter = window.innerWidth / 2
  const widgetRight = window.innerWidth + widgetPos.value.x
  if (widgetRight < viewportCenter) {
    snapSide.value = 'left'
    widgetPos.value = clampWidgetPos(floatButtonSize.w + edgeMargin - window.innerWidth, widgetPos.value.y)
  } else {
    snapSide.value = 'right'
    widgetPos.value = clampWidgetPos(-edgeMargin, widgetPos.value.y)
  }
}

function initPosition() {
  widgetPos.value = clampWidgetPos(-edgeMargin, -edgeMargin)
  snapSide.value = 'right'
}
initPosition()

function bindResizeListeners() {
  window.addEventListener('pointermove', onResizeMove)
  window.addEventListener('pointerup', onResizeEnd, { capture: true })
  window.addEventListener('pointercancel', onResizeEnd, { capture: true })
  window.addEventListener('blur', onResizeEnd)
}

function unbindResizeListeners() {
  window.removeEventListener('pointermove', onResizeMove)
  window.removeEventListener('pointerup', onResizeEnd, { capture: true })
  window.removeEventListener('pointercancel', onResizeEnd, { capture: true })
  window.removeEventListener('blur', onResizeEnd)
}

// ── resize logic ──
function onResizeStart(e: PointerEvent) {
  if (e.button !== 0 && e.pointerType !== 'touch') return
  resizePointerId = e.pointerId
  isResizing.value = true
  const p = getPoint(e)
  resizeStart.value = { x: p.clientX, y: p.clientY }
  resizeOffset.value = { w: chatSize.value.w, h: chatSize.value.h }
  bindResizeListeners()
  e.preventDefault()
  ;(e.currentTarget as HTMLElement | null)?.setPointerCapture?.(e.pointerId)
}

function onResizeMove(e: PointerEvent) {
  if (!isResizing.value) return
  if (resizePointerId !== null && e.pointerId !== resizePointerId) return
  const p = getPoint(e)
  const dx = p.clientX - resizeStart.value.x
  const dy = p.clientY - resizeStart.value.y
  chatSize.value = {
    w: Math.max(300, Math.min(800, resizeOffset.value.w + dx)),
    h: Math.max(400, Math.min(window.innerHeight - 80, resizeOffset.value.h + dy)),
  }
  widgetPos.value = clampWidgetPos(widgetPos.value.x, widgetPos.value.y)
}

function onResizeEnd() {
  resizePointerId = null
  isResizing.value = false
  unbindResizeListeners()
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

function toggleOpen(e: MouseEvent) {
  if (hasDragged.value) return
  e.stopPropagation()
  open.value = !open.value
  if (open.value) scrollBottom()
}

watch(open, (val) => {
  if (val) {
    document.addEventListener('click', onClickOutside)
    widgetPos.value = clampWidgetPos(widgetPos.value.x, widgetPos.value.y)
  } else {
    document.removeEventListener('click', onClickOutside)
    snapToEdge()
  }
})

function onClickOutside(e: MouseEvent) {
  const target = e.target as Node | null
  if (target && widgetRoot.value?.contains(target)) return
  open.value = false
}

// esc to close
function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && open.value) open.value = false
}
window.addEventListener('keydown', onKeydown)

onUnmounted(() => {
  abort()
  window.removeEventListener('keydown', onKeydown)
  document.removeEventListener('click', onClickOutside)
  unbindDragListeners()
  unbindResizeListeners()
})
</script>

<template>
  <div
    ref="widgetRoot"
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
        @click.stop
      >
        <!-- Header (drag handle) -->
        <div class="chat-header" @pointerdown.prevent="onDragStart">
          <div class="chat-title-wrap">
            <span class="chat-title">AI 助手</span>
          </div>
          <div class="header-actions">
            <div class="model-select-wrap">
              <span class="model-label">MODEL</span>
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
            </div>
            <button class="btn-close" @pointerdown.stop @click="open = false" title="关闭 (Esc)">&times;</button>
          </div>
        </div>

        <!-- Messages -->
        <div id="msg-area" class="msg-area">
          <div v-if="messages.length === 0" class="empty-hint">
            <div class="empty-title">智能助手已就绪</div>
            <div class="empty-copy">输入设备、工艺或知识问题，开始一段对话。</div>
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
          @pointerdown.prevent="onResizeStart"
        ></div>
      </div>
    </Transition>

    <!-- Floating button -->
    <button
      v-show="!open"
      class="float-btn"
      @pointerdown.stop.prevent="onDragStart"
      @click="toggleOpen"
    >
      <img :src="clawdThinkingGif" alt="AI Assistant" class="robot-icon" draggable="false" />
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
  width: 256px;
  height: 256px;
  border-radius: 18px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
  user-select: none;
  position: absolute;
  bottom: 0;
  right: 0;
  overflow: hidden;
  padding: 0;
  touch-action: none;
}
.float-btn:hover {
  transform: scale(1.06) translateY(-2px);
}
.robot-icon {
  width: 240px;
  height: 240px;
  border-radius: 16px;
  object-fit: cover;
}

/* ── chat window ── */
.chat-window {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.06);
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
  touch-action: none;
}
.resize-handle::after {
  content: '';
  position: absolute;
  bottom: 6px;
  right: 6px;
  width: 10px;
  height: 10px;
  border-right: 2px solid #ccc;
  border-bottom: 2px solid #ccc;
}
.resize-handle:hover::after {
  border-color: #4a90d9;
}

/* ── header ── */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
  color: #fff;
  cursor: grab;
  user-select: none;
  flex-shrink: 0;
  touch-action: none;
}
.chat-header:active {
  cursor: grabbing;
}
.chat-title-wrap {
  display: flex;
  align-items: center;
}
.chat-title {
  font-weight: 700;
  font-size: 16px;
  letter-spacing: 0.5px;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.model-select-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}
.model-label {
  font-size: 10px;
  letter-spacing: 1px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 600;
}
.model-select {
  min-width: 110px;
  padding: 6px 24px 6px 8px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  font-size: 12px;
  cursor: pointer;
  outline: none;
  appearance: none;
}
.model-select option {
  color: #333;
  background: #fff;
}
.btn-close {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: background 0.2s;
}
.btn-close:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* ── messages ── */
.msg-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #f8f9fb;
}
.empty-hint {
  text-align: center;
  color: #999;
  margin-top: 60px;
  padding: 18px;
}
.empty-title {
  font-size: 16px;
  font-weight: 600;
  color: #555;
  margin-bottom: 6px;
}
.empty-copy {
  font-size: 13px;
  line-height: 1.7;
  color: #aaa;
}
.msg {
  max-width: 85%;
}
.msg.user {
  align-self: flex-end;
}
.msg.user .msg-content {
  background: linear-gradient(135deg, #4a90d9 0%, #5ba0e8 100%);
  color: #fff;
  border-radius: 16px 16px 4px 16px;
  box-shadow: 0 2px 8px rgba(74, 144, 217, 0.2);
}
.msg.assistant {
  align-self: flex-start;
}
.msg.assistant .msg-content {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 16px 16px 16px 4px;
  color: #333;
}
.msg-content {
  padding: 12px 14px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}
.status-line {
  text-align: center;
  color: #aaa;
  font-size: 12px;
}

/* ── input area ── */
.input-area {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid #eee;
  flex-shrink: 0;
  background: #fff;
}
.input-area input {
  flex: 1;
  padding: 10px 14px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 10px;
  outline: none;
  background: #f5f6f8;
  color: #333;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.input-area input::placeholder {
  color: #bbb;
}
.input-area input:focus {
  border-color: #4a90d9;
  box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.1);
}
.btn-send,
.btn-stop {
  padding: 10px 18px;
  font-size: 13px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  white-space: nowrap;
}
.btn-send {
  background: #4a90d9;
  color: #fff;
  transition: background 0.2s;
}
.btn-send:hover {
  background: #357abd;
}
.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-stop {
  background: #f0f0f0;
  color: #888;
  border: 1px solid #ddd;
}
.btn-stop:hover {
  background: #e5e5e5;
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
