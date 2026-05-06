import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000, // 60s — RAG + LLM can be slow
})

/**
 * Analyze a legal case description.
 * @param {string} name - User's name
 * @param {string} caseDescription - The case facts
 * @returns {Promise<AnalyzeResponse>}
 */
export async function analyzeCase(name, caseDescription) {
  const { data } = await api.post('/analyze', {
    name,
    case_description: caseDescription,
  })
  return data
}

/**
 * Fetch available IPC categories from backend.
 * @returns {Promise<{ categories: Category[] }>}
 */
export async function fetchCategories() {
  const { data } = await api.get('/ipc-categories')
  return data
}

/**
 * Health-check the backend.
 */
export async function healthCheck() {
  const { data } = await api.get('/health')
  return data
}
