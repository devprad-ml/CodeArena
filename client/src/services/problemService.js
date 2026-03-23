import api from './api'

export const problemService = {
  async getProblems(path, params = {}) {
    const { data } = await api.get(`/problems`, { params: { path, ...params } })
    return data
  },

  async getProblem(id) {
    const { data } = await api.get(`/problems/${id}`)
    return data
  },

  async getRandomProblem(path, difficulty) {
    const { data } = await api.get(`/problems/random`, { params: { path, difficulty } })
    return data
  },
}
