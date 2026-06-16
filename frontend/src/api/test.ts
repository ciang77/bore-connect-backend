import api from './index'

export interface LatestValue {
  value: number
  time: string
}

export interface RealtimeData {
  labels: string[]
  actPosition: number[]
  setPosition: number[]
  speed: number[]
  latestTime: string | null
  latestValues: Record<string, LatestValue>
}

export function fetchRealtimeData(range: '24h' | '7d'): Promise<{ code: number; data: RealtimeData }> {
  return api.get('/api/test/realtime-data', { params: { range } }).then((res) => res.data)
}
