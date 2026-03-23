import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import LoadingSpinner from '@/components/shared/LoadingSpinner'

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, token } = useAuthStore()

  // Still checking token
  if (token && !isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!isAuthenticated) return <Navigate to="/login" replace />

  return children
}
