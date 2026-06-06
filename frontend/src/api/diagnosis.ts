import api from './index'

export interface StatusVariable {
  label: string
  value: number
}

export interface SubsystemStatusData {
  name: string
  variables: StatusVariable[]
}

export function fetchDiagnosisStatus(): Promise<{ code: number; data: SubsystemStatusData[] }> {
  return api.get('/api/diagnosis/status').then((res) => res.data)
}
