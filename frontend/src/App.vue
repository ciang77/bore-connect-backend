<script setup lang="ts">
import { ref, nextTick, onUnmounted } from 'vue'

const open = ref(false)
const model = ref('qwen')
const input = ref('')
const sending = ref(false)
const status = ref('')
const messages = ref<{ role: 'user' | 'assistant'; content: string }[]>([])

let controller: AbortController | null = null

const widgetPos = ref({ x: 0, y: 0 })
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const dragOffset = ref({ x: 0, y: 0 })

const models = [
  { value: 'qwen', label: '千问 (Qwen)' },
  { value: 'deepseek', label: 'DeepSeek' },
]

// ── drag logic ──
function onDragStart(e: MouseEvent | TouchEvent) {
  isDragging.value = true
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
  widgetPos.value = {
    x: dragOffset.value.x + p.clientX - dragStart.value.x,
    y: dragOffset.value.y + p.clientY - dragStart.value.y,
  }
}

function onDragEnd() {
  isDragging.value = false
  document.removeEventListener('mousemove', onDragMove)
  document.removeEventListener('mouseup', onDragEnd)
  document.removeEventListener('touchmove', onDragMove)
  document.removeEventListener('touchend', onDragEnd)
}

// ── init position ──
function initPosition() {
  widgetPos.value = { x: -20, y: -20 }
}
initPosition()

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
    const resp = await fetch('/chat/qa/stream', {
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
  open.value = !open.value
  if (open.value) scrollBottom()
}

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
})
</script>

<template>
  <div
    class="widget-root"
    :style="{ transform: `translate(${widgetPos.x}px, ${widgetPos.y}px)` }"
  >
    <!-- Chat Window -->
    <Transition name="pop">
      <div v-if="open" class="chat-window">
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
      </div>
    </Transition>

    <!-- Floating button -->
    <button
      v-show="!open"
      class="float-btn"
      @mousedown.stop="onDragStart"
      @touchstart.stop.prevent="onDragStart"
      @click.stop="toggleOpen"
    >
      <span class="robot-icon">🤖</span>
    </button>
  </div>
</template>

<style>
/* ── reset for embeddable widget ── */
body {
  margin: 0;
  min-height: 100vh;
  background: #f0f2f5;
}
</style>

<style scoped>
/* ── root ── */
.widget-root {
  position: fixed;
  bottom: 0;
  right: 0;
  z-index: 99999;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial,
    "PingFang SC", "Microsoft YaHei", sans-serif;
}

/* ── float button ── */
.float-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.45);
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
  box-shadow: 0 6px 24px rgba(102, 126, 234, 0.55);
}
.robot-icon {
  font-size: 30px;
  line-height: 1;
}

/* ── chat window ── */
.chat-window {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 400px;
  height: 560px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  overflow: hidden;
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
  background: #f8f9fb;
}
.empty-hint {
  text-align: center;
  color: #aaa;
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
  background: #fff;
  border: 1px solid #e8e8ec;
  border-radius: 14px 14px 14px 4px;
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
  color: #999;
  font-size: 12px;
}

/* ── input area ── */
.input-area {
  display: flex;
  gap: 6px;
  padding: 10px 12px;
  border-top: 1px solid #eee;
  flex-shrink: 0;
  background: #fff;
}
.input-area input {
  flex: 1;
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid #e0e0e4;
  border-radius: 10px;
  outline: none;
  transition: border-color 0.2s;
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
  background: #eee;
  color: #666;
}
.btn-stop:hover {
  background: #ddd;
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
