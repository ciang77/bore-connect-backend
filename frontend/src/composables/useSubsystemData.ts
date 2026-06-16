import { ref, onMounted, type Ref } from 'vue'
import { fetchSubsystems, type SubsystemInfo } from '../api/overview'
import { useEventSource } from './useEventSource'

export function useSubsystemData(): {
  subsystems: Ref<SubsystemInfo[]>
  loading: Ref<boolean>
} {
  const subsystems = ref<SubsystemInfo[]>([])
  const loading = ref(true)

  async function load() {
    try {
      const res = await fetchSubsystems()
      if (res.code === 0 && res.data) {
        subsystems.value = res.data
      }
    } finally {
      loading.value = false
    }
  }

  // SSE 必须在 setup 同步阶段注册，不能放在 onMounted 的 await 之后
  useEventSource<SubsystemInfo[]>(
    '/api/overview/subsystems/stream',
    (data) => {
      subsystems.value = data
    },
  )

  onMounted(async () => {
    // 首次加载走 REST 快速获取
    await load()
  })

  return { subsystems, loading }
}
