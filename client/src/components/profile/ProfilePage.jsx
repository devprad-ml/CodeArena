import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/store/authStore'
import { useArenaStore } from '@/store/arenaStore'
import { authService } from '@/services/authService'
import { getRankForPoints } from '@/utils/helpers'
import { PATHS } from '@/utils/constants'
import RankLadder from './RankLadder'
import SubmissionHistory from './SubmissionHistory'
import AchievementBadges from './AchievementBadges'
import LoadingSpinner from '@/components/shared/LoadingSpinner'

const TABS = ['Overview', 'Rank Ladder', 'Submissions', 'Achievements']

export default function ProfilePage() {
  const { token } = useAuthStore()
  const { activePath } = useArenaStore()
  const [activeTab, setActiveTab] = useState('Overview')
  const isFighter = activePath === PATHS.FIGHTER

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
  const fighterRank = getRankForPoints(fighterPoints, PATHS.FIGHTER)
  const sentinelRank = getRankForPoints(sentinelPoints, PATHS.SENTINEL)
  const stats = user?.stats ?? {}
  const achievements = user?.achievements ?? []

  const accentColor = isFighter ? fighterRank.color : sentinelRank.color
  const tabActiveClass = isFighter
    ? 'border-fighter-primary text-white'
    : 'border-sentinel-primary text-white'

  return (
    <div className="min-h-screen bg-gray-950 pt-20 pb-12 px-4">
      <div className="max-w-4xl mx-auto">

        {/* Profile header */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-6 flex items-center gap-5">
          {user?.avatar_url ? (
            <img
              src={user.avatar_url}
              alt="avatar"
              className="w-16 h-16 rounded-full border-2"
              style={{ borderColor: accentColor }}
            />
          ) : (
            <div
              className="w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold border-2"
              style={{ borderColor: accentColor, backgroundColor: `${accentColor}20` }}
            >
              {user?.username?.[0]?.toUpperCase() ?? '?'}
            </div>
          )}

          <div className="flex-1 min-w-0">
            <h1 className="text-white font-display font-bold text-2xl">{user?.username ?? 'Anonymous'}</h1>
            <p className="text-gray-500 text-sm mt-0.5">{user?.email ?? ''}</p>
            <div className="flex items-center gap-4 mt-2">
              <span className="text-xs" style={{ color: fighterRank.color }}>
                ⚔️ {fighterRank.name}
              </span>
              <span className="text-xs" style={{ color: sentinelRank.color }}>
                🛡️ {sentinelRank.name}
              </span>
              {stats.current_streak > 0 && (
                <span className="text-xs text-orange-400">
                  🔥 {stats.current_streak}d streak
                </span>
              )}
            </div>
          </div>

          {/* Quick stats */}
          <div className="hidden sm:flex gap-6 text-center">
            {[
              { label: 'Solved', value: stats.total_solved ?? 0 },
              { label: 'Fighter', value: fighterPoints + ' pts' },
              { label: 'Sentinel', value: sentinelPoints + ' pts' },
            ].map(({ label, value }) => (
              <div key={label}>
                <p className="text-white font-bold text-lg">{value}</p>
                <p className="text-gray-500 text-xs">{label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-800 mb-6">
          {TABS.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab
                  ? tabActiveClass
                  : 'border-transparent text-gray-500 hover:text-gray-300'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {activeTab === 'Overview' && (
          <div className="space-y-6">
            {/* Stat cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[
                { label: 'Total Solved',      value: stats.total_solved ?? 0 },
                { label: 'First-Try Rate',     value: stats.first_try_rate ? `${Math.round(stats.first_try_rate * 100)}%` : '—' },
                { label: 'Current Streak',     value: `${stats.current_streak ?? 0}d` },
                { label: 'Total Submissions',  value: stats.total_submissions ?? 0 },
              ].map(({ label, value }) => (
                <div key={label} className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
                  <p className="text-2xl font-bold text-white">{value}</p>
                  <p className="text-xs text-gray-500 mt-1">{label}</p>
                </div>
              ))}
            </div>

            {/* Category breakdown (if available) */}
            {stats.categories && Object.keys(stats.categories).length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <h3 className="text-sm font-semibold text-gray-300 mb-4">Category Breakdown</h3>
                <div className="space-y-2">
                  {Object.entries(stats.categories).map(([cat, count]) => (
                    <div key={cat} className="flex items-center gap-3">
                      <span className="text-xs text-gray-400 w-28 truncate capitalize">{cat}</span>
                      <div className="flex-1 bg-gray-800 rounded-full h-1.5">
                        <div
                          className="h-1.5 rounded-full"
                          style={{
                            width: `${Math.min(100, (count / (stats.total_solved || 1)) * 100)}%`,
                            backgroundColor: accentColor,
                          }}
                        />
                      </div>
                      <span className="text-xs text-gray-500 w-6 text-right">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'Rank Ladder' && (
          <RankLadder fighterPoints={fighterPoints} sentinelPoints={sentinelPoints} />
        )}

        {activeTab === 'Submissions' && <SubmissionHistory />}

        {activeTab === 'Achievements' && (
          <AchievementBadges earnedIds={achievements} />
        )}
      </div>
    </div>
  )
}
