import { createContext, useContext } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/store/authStore'
import { authService } from '@/services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const { token, setAuth, logout } = useAuthStore()

  const { data: user, isLoading } = useQuery({
    queryKey: ['me'],
    queryFn: authService.getMe,
    enabled: !!token,
    retry: false,
    onSuccess: (data) => setAuth(data, token),
    onError: () => logout(),
  })

  return (
    <AuthContext.Provider value={{ user, isLoading, token }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
