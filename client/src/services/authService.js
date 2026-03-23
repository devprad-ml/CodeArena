import api from './api'

export const authService = {
  async getMe() {
    const { data } = await api.get('/users/me')
    return data
  },

  async logout() {
    await api.post('/auth/logout')
    localStorage.removeItem('access_token')
  },

  getOAuthUrl(provider) {
    return `/api/v1/auth/${provider}`
  },
}
