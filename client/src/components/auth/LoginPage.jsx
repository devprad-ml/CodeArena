import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import OAuthButtons from './OAuthButtons'

export default function LoginPage() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard')
  }, [isAuthenticated, navigate])

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center px-4">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-fighter-bg via-gray-950 to-sentinel-bg opacity-60" />

      <div className="relative z-10 w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-10">
          <h1 className="font-display font-bold text-5xl tracking-widest mb-2">
            <span className="text-fighter-primary">CODE</span>
            <span className="text-white">ARENA</span>
          </h1>
          <p className="text-gray-400 text-sm mt-2">
            Choose your path. Prove your mastery.
          </p>
        </div>

        {/* Card */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 shadow-2xl">
          <h2 className="text-center text-white font-semibold text-lg mb-6">
            Enter the Arena
          </h2>
          <OAuthButtons />
          <p className="text-center text-gray-600 text-xs mt-6">
            By signing in, you agree to battle with honor.
          </p>
        </div>
      </div>
    </div>
  )
}
