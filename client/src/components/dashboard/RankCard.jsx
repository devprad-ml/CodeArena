import { getRankForPoints, getNextRank, getProgressPercent } from '@/utils/helpers'
import { PATHS } from '@/utils/constants'

export default function RankCard({ points = 0, path }) {
  const rank = getRankForPoints(points, path)
  const nextRank = getNextRank(points, path)
  const progress = getProgressPercent(points, path)
  const isFighter = path === PATHS.FIGHTER

  return (
    <div className={`rounded-xl p-5 border ${
      isFighter ? 'bg-fighter-surface border-fighter-border' : 'bg-sentinel-surface border-sentinel-border'
    }`}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
            {isFighter ? 'Fighter Rank' : 'Sentinel Rank'}
          </p>
          <h3
            className="font-display font-bold text-2xl"
            style={{ color: rank.color }}
          >
            {rank.name}
          </h3>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-white">{points}</p>
          <p className="text-xs text-gray-500">points</p>
        </div>
      </div>

      {nextRank && (
        <>
          <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span>{rank.name}</span>
            <span>{nextRank.name} ({nextRank.points} pts)</span>
          </div>
          <div className="w-full bg-gray-800 rounded-full h-2">
            <div
              className="h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%`, backgroundColor: rank.color }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-1 text-right">{progress}%</p>
        </>
      )}

      {!nextRank && (
        <p className="text-xs text-center mt-2" style={{ color: rank.color }}>
          ★ Supreme Rank Achieved ★
        </p>
      )}
    </div>
  )
}
