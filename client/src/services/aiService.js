import api from './api'

export const aiService = {
  async getHint(problemId, code) {
    const { data } = await api.post('/ai/hint', { problem_id: problemId, code })
    return data
  },

  async getExplanation(submissionId) {
    const { data } = await api.post(`/ai/explain/${submissionId}`)
    return data
  },

  async evaluateSentinel(problemId, answer) {
    const { data } = await api.post('/ai/evaluate', { problem_id: problemId, answer })
    return data
  },
}
