import { FIGHTER_RANKS, SENTINEL_RANKS, PATHS } from '@/utils/constants'
import { getRankForPoints } from '@/utils/helpers'

function LadderPath({ ranks, points, path }) {
  const currentRank = getRankForPoints(points, path)
  const isFighter = path === PATHS.FIGHTER

  return (
    <div className="flex flex-col gap-1">
      {[...ranks].reverse().map((rank, i) => {
        const unlocked = points >= rank.points
        const isCurrent = rank.name === currentRank.name

        return (
          <div
            key={rank.name}
            className={`flex items-center gap-3 px-4 py-2.5 rounded-lg border transition-all ${
              isCurrent
                ? `border-opacity-60 bg-opacity-10`
                : unlocked
                ? 'border-gray-700 bg-gray-800/40'
                : 'border-gray-800 bg-gray-900/30 opacity-40'
            }`}
            style={
              isCurrent
                ? { borderColor: rank.color, backgroundColor: `${rank.color}15` }
                : {}
            }
          >
            {/* Dot indicator */}
            <div
              className={`w-2.5 h-2.5 rounded-full shrink-0 ${!unlocked ? 'bg-gray-700' : ''}`}
              style={unlocked ? { backgroundColor: rank.color } : {}}
            />

            {/* Rank name */}
            <div className="flex-1 min-w-0">
              <span
                className={`font-semibold text-sm ${!unlocked ? 'text-gray-600' : ''}`}
                style={unlocked ? { color: rank.color } : {}}
              >
                {rank.name}
                {rank.supreme && ' ★'}
              </span>
              <span className="text-xs text-gray-600 ml-2">{rank.points} pts</span>
            </div>

            {/* Status */}
            <div className="shrink-0 text-xs">
              {isCurrent && (
                <span
                  className="px-2 py-0.5 rounded font-semibold"
                  style={{ color: rank.color, backgroundColor: `${rank.color}20` }}
                >
                  Current
                </span>
              )}
              {!isCurrent && unlocked && (
                <span className="text-gray-500">✓</span>
              )}
              {!unlocked && (
                <span className="text-gray-700">🔒</span>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default function RankLadder({ fighterPoints = 0, sentinelPoints = 0 }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
      <div>
        <h3 className="text-xs font-semibold text-fighter-primary uppercase tracking-wider mb-3 flex items-center gap-2">
          ⚔️ Fighter Path
        </h3>
        <LadderPath ranks={FIGHTER_RANKS} points={fighterPoints} path={PATHS.FIGHTER} />
      </div>
      <div>
        <h3 className="text-xs font-semibold text-sentinel-primary uppercase tracking-wider mb-3 flex items-center gap-2">
          🛡️ Sentinel Path
        </h3>
        <LadderPath ranks={SENTINEL_RANKS} points={sentinelPoints} path={PATHS.SENTINEL} />
      </div>
    </div>
  )
}
