import { getCurrentInstance, onUnmounted, watch, type Ref } from 'vue'

/**
 * 通用 SSE (Server-Sent Events) composable
 *
 * - 自动 JSON 解析
 * - 响应式 URL 切换（关闭旧连接 + 打开新连接）
 * - 组件卸载时自动关闭
 * - EventSource 内置断线重连
 *
 * **重要**：必须在 setup() 同步阶段调用，不要在 onMounted 的 await 之后调用！
 * 如果不在 setup 上下文中，将跳过自动清理，调用方需手动 close()。
 */
export function useEventSource<T>(
  url: Ref<string> | string,
  onData: (data: T) => void,
  onError?: (event: Event) => void,
): { close: () => void } {
  let es: EventSource | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null

  function connect(targetUrl: string) {
    if (es) {
      es.close()
      es = null
    }
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }

    es = new EventSource(targetUrl)

    es.onmessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data) as T
        onData(data)
      } catch {
        // 忽略解析失败的数据
      }
    }

    es.onerror = (event: Event) => {
      // 关闭当前连接，准备手动重连
      if (es) {
        es.close()
        es = null
      }
      onError?.(event)
      // EventSource 有内置重连，但长时间断开后可能停止重试
      // 添加手动重连兜底：5 秒后重试
      reconnectTimer = setTimeout(() => {
        if (!es) {
          connect(targetUrl)
        }
      }, 5000)
    }
  }

  function close() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    if (es) {
      es.close()
      es = null
    }
  }

  if (typeof url === 'string') {
    connect(url)
  } else {
    watch(
      url,
      (newUrl) => {
        if (newUrl) connect(newUrl)
      },
      { immediate: true },
    )
  }

  // 仅在 setup 同步阶段注册生命周期钩子
  if (getCurrentInstance()) {
    onUnmounted(() => close())
  }

  return { close }
}
