import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { authService } from '@/services/authService'

export default function AuthCallback() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()

  useEffect(() => {
    const token = searchParams.get('token')
    if (!token) {
      navigate('/login')
      return
    }

    // Store token first so the API call is authenticated
    localStorage.setItem('access_token', token)

    authService.getMe()
      .then((user) => {
        setAuth(user, token)
        navigate('/dashboard', { replace: true })
      })
      .catch(() => {
        localStorage.removeItem('access_token')
        navigate('/login')
      })
  }, [])

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <p className="text-gray-400 text-sm animate-pulse">Entering the arena...</p>
    </div>
  )
}
