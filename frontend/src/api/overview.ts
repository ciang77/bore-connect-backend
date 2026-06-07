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

export interface AlarmItem {
  id: number
  time: string
  level: 'info' | 'warning' | 'error'
  subsystem: string
  msg: string
}

export function fetchAlarms(): Promise<{ code: number; data: AlarmItem[] }> {
  return api.get('/api/overview/alarms').then((res) => res.data)
}

// ── 实时报警开关 ──
export function fetchAlertStatus(): Promise<{ code: number; data: { enabled: boolean } }> {
  return api.get('/api/alert/status').then((res) => res.data)
}

export function toggleAlert(enabled: boolean): Promise<{ code: number; data: { enabled: boolean }; msg: string }> {
  return api.post('/api/alert/toggle', { enabled }).then((res) => res.data)
}
