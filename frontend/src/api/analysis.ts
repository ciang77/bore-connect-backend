import api from './index'

export interface MotorCurrentItem {
  id: string
  current: number
  minCurrent: number
  maxCurrent: number
}

export function fetchMotorCurrents(): Promise<{ code: number; data: MotorCurrentItem[] }> {
  return api.get('/api/analysis/motor-currents').then((res) => res.data)
}
