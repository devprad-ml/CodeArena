import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { useArenaStore } from '@/store/arenaStore'
import { authService } from '@/services/authService'
import { PATHS } from '@/utils/constants'

export default function Navbar() {
  const navigate = useNavigate()
  const { user, isAuthenticated, logout } = useAuthStore()
  const { activePath } = useArenaStore()

  const isFighter = activePath === PATHS.FIGHTER

  const handleLogout = async () => {
    await authService.logout()
    logout()
    navigate('/login')
  }

  return (
    <nav className={`fixed top-0 w-full z-50 border-b backdrop-blur-sm ${
      isFighter
        ? 'bg-fighter-bg/90 border-fighter-border'
        : 'bg-sentinel-bg/90 border-sentinel-border'
    }`}>
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        <Link to="/" className="font-display font-bold text-xl tracking-wider">
          <span className={isFighter ? 'text-fighter-primary' : 'text-sentinel-primary'}>
            CODE
          </span>
          <span className="text-gray-100">ARENA</span>
        </Link>

        {isAuthenticated && (
          <div className="flex items-center gap-6">
            <Link to="/dashboard" className="text-sm text-gray-400 hover:text-white transition-colors">
              Dashboard
            </Link>
            <Link to="/arena" className="text-sm text-gray-400 hover:text-white transition-colors">
              Arena
            </Link>
            <Link to="/profile" className="text-sm text-gray-400 hover:text-white transition-colors">
              Profile
            </Link>
            <div className="flex items-center gap-3">
              {user?.avatar_url && (
                <img src={user.avatar_url} alt="avatar" className="w-7 h-7 rounded-full border border-gray-600" />
              )}
              <span className="text-sm text-gray-300">{user?.username}</span>
              <button
                onClick={handleLogout}
                className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
