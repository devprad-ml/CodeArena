import api from './api'

export const submissionService = {
  async submit(problemId, code, language) {
    const { data } = await api.post('/submissions', { problem_id: problemId, code, language })
    return data
  },

  async getSubmission(id) {
    const { data } = await api.get(`/submissions/${id}`)
    return data
  },

  async getMySubmissions(path) {
    const { data } = await api.get('/submissions/me', { params: { path } })
    return data
  },
}
