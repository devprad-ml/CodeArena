import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { useArenaStore } from '@/store/arenaStore'
import { authService } from '@/services/authService'
import { PATHS } from '@/utils/constants'
import PathSelector from './PathSelector'
import RankCard from './RankCard'
import StatsOverview from './StatsOverview'
import LoadingSpinner from '@/components/shared/LoadingSpinner'

export default function Dashboard() {
  const navigate = useNavigate()
  const { token } = useAuthStore()
  const { activePath } = useArenaStore()

  const { data: user, isLoading } = useQuery({
    queryKey: ['me'],
    queryFn: authService.getMe,
    enabled: !!token,
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <LoadingSpinner size="lg" color={activePath} />
      </div>
    )
  }

  const fighterPoints = user?.fighter_progress?.points ?? 0
  const sentinelPoints = user?.sentinel_progress?.points ?? 0
  const activePoints = activePath === PATHS.FIGHTER ? fighterPoints : sentinelPoints

  return (
    <div className="min-h-screen bg-gray-950 pt-20 px-4 pb-8">
      <div className="max-w-4xl mx-auto">
        {/* Welcome */}
        <div className="mb-8">
          <h1 className="font-display text-3xl font-bold text-white">
            Welcome back, <span className={activePath === PATHS.FIGHTER ? 'text-fighter-primary' : 'text-sentinel-primary'}>
              {user?.username ?? 'Warrior'}
            </span>
          </h1>
          <p className="text-gray-400 mt-1">Your path to mastery continues.</p>
        </div>

        {/* Path Selector */}
        <PathSelector fighterPoints={fighterPoints} sentinelPoints={sentinelPoints} />

        {/* Rank Card */}
        <div className="mb-6">
          <RankCard points={activePoints} path={activePath} />
        </div>

        {/* Stats */}
        <div className="mb-8">
          <StatsOverview stats={user?.stats ?? {}} />
        </div>

        {/* Enter Arena CTA */}
        <button
          onClick={() => navigate('/arena')}
          className={`w-full py-4 rounded-xl font-display font-bold text-xl tracking-wider transition-all duration-300 ${
            activePath === PATHS.FIGHTER
              ? 'bg-fighter-primary hover:bg-red-700 text-white glow-fighter'
              : 'bg-sentinel-primary hover:bg-blue-700 text-white glow-sentinel'
          }`}
        >
          ENTER THE ARENA →
        </button>
      </div>
    </div>
  )
}
