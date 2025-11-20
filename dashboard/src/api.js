import axios from 'axios'

const API_BASE = '/api'

export async function fetchStats(days = 7) {
  const response = await axios.get(`${API_BASE}/predictions/stats?days=${days}`)
  return response.data
}

export async function fetchAccuracy(days = 30) {
  const response = await axios.get(`${API_BASE}/accuracy?days=${days}`)
  return response.data
}

export async function fetchRecentPredictions(days = 7, sport = null) {
  let url = `${API_BASE}/predictions/recent?days=${days}`
  if (sport) url += `&sport=${sport}`
  const response = await axios.get(url)
  return response.data
}

export async function fetchConsensusPicks(days = 7, minAgreement = 3) {
  const response = await axios.get(`${API_BASE}/consensus?days=${days}&min_agreement=${minAgreement}`)
  return response.data
}

export async function fetchPredictionDetail(id) {
  const response = await axios.get(`${API_BASE}/predictions/${id}`)
  return response.data
}

export async function updatePredictionResult(id, result) {
  const response = await axios.post(`${API_BASE}/predictions/${id}/result`, result)
  return response.data
}
