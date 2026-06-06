import api from './index'

export interface DeviceStatus {
  name: string
  model: string
  status: 'online' | 'warning' | 'stopped'
  runtime: string
  temperature: string
  vibration: string
  pressure: string
  spindleSpeed: string
  servoCurrent: string
}

export interface TrendData {
  labels: string[]
  servoCurrent: number[]
  vibration: number[]
  temperature: number[]
}

export interface SubsystemMetric {
  label: string
  value: string
  unit: string
}

export interface SubsystemInfo {
  name: string
  nameEn: string
  status: 'normal' | 'warning' | 'fault'
  healthScore: number
  metrics: SubsystemMetric[]
}

export function fetchDeviceStatus(): Promise<{ code: number; data: DeviceStatus }> {
  return api.get('/api/overview/device-status').then((res) => res.data)
}

export function fetchTrendData(range: '24h' | '7d'): Promise<{ code: number; data: TrendData }> {
  return api.get('/api/overview/trend-data', { params: { range } }).then((res) => res.data)
}

export function fetchSubsystems(): Promise<{ code: number; data: SubsystemInfo[] }> {
  return api.get('/api/overview/subsystems').then((res) => res.data)
}
