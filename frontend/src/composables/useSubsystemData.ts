import { ref, onMounted, onUnmounted, type Ref } from 'vue'
import { fetchSubsystems, type SubsystemInfo } from '../api/overview'

export function useSubsystemData(): {
  subsystems: Ref<SubsystemInfo[]>
  loading: Ref<boolean>
} {
  const subsystems = ref<SubsystemInfo[]>([])
  const loading = ref(true)
  let timer: ReturnType<typeof setInterval> | undefined

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

  onMounted(async () => {
    await load()
    timer = setInterval(load, 3000)
  })

  onUnmounted(() => {
    if (timer) clearInterval(timer)
  })

  return { subsystems, loading }
}
