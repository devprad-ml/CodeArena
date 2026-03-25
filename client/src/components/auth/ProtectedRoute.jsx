import { useEffect } from 'react'
import { Navigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/store/authStore'
import { authService } from '@/services/authService'
import LoadingSpinner from '@/components/shared/LoadingSpinner'

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, token, setAuth, logout } = useAuthStore()

  const { data: user, isLoading, isError } = useQuery({
    queryKey: ['me'],
    queryFn: authService.getMe,
    enabled: !!token && !isAuthenticated,
    retry: false,
  })

  useEffect(() => {
    if (user) setAuth(user, token)
  }, [user])

  useEffect(() => {
    if (isError) logout()
  }, [isError])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!isAuthenticated) return <Navigate to="/login" replace />

  return children
}
