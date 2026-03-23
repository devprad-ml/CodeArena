import { useArenaStore } from '@/store/arenaStore'
import { PATHS } from '@/utils/constants'

export default function PathSelector({ fighterPoints = 0, sentinelPoints = 0 }) {
  const { activePath, setActivePath } = useArenaStore()

  return (
    <div className="grid grid-cols-2 gap-4 mb-8">
      {/* Fighter Path */}
      <button
        onClick={() => setActivePath(PATHS.FIGHTER)}
        className={`relative p-6 rounded-xl border-2 text-left transition-all duration-300 ${
          activePath === PATHS.FIGHTER
            ? 'border-fighter-primary bg-fighter-surface glow-fighter'
            : 'border-gray-800 bg-gray-900 hover:border-fighter-border'
        }`}
      >
        <div className="text-3xl mb-2">⚔️</div>
        <h3 className="font-display font-bold text-xl text-fighter-primary mb-1">FIGHTER</h3>
        <p className="text-xs text-gray-400">Algorithmic challenges. Raw skill. Prove yourself.</p>
        <div className="mt-3 text-sm font-bold text-white">{fighterPoints} pts</div>
        {activePath === PATHS.FIGHTER && (
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full bg-fighter-primary animate-pulse" />
        )}
      </button>

      {/* Sentinel Path */}
      <button
        onClick={() => setActivePath(PATHS.SENTINEL)}
        className={`relative p-6 rounded-xl border-2 text-left transition-all duration-300 ${
          activePath === PATHS.SENTINEL
            ? 'border-sentinel-primary bg-sentinel-surface glow-sentinel'
            : 'border-gray-800 bg-gray-900 hover:border-sentinel-border'
        }`}
      >
        <div className="text-3xl mb-2">🛡️</div>
        <h3 className="font-display font-bold text-xl text-sentinel-primary mb-1">SENTINEL</h3>
        <p className="text-xs text-gray-400">System design. Strategic thinking. Build to last.</p>
        <div className="mt-3 text-sm font-bold text-white">{sentinelPoints} pts</div>
        {activePath === PATHS.SENTINEL && (
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full bg-sentinel-primary animate-pulse" />
        )}
      </button>
    </div>
  )
}
