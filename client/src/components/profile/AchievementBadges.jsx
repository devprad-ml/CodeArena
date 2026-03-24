// Achievements are defined here as a frontend constant.
// The backend awards them; we just display locked/unlocked state.
const ACHIEVEMENTS = [
  // Fighter
  { id: 'first_blood',    label: 'First Blood',      desc: 'Solve your first problem',         icon: '⚔️',  path: 'fighter' },
  { id: 'hat_trick',      label: 'Hat Trick',        desc: 'Solve 3 problems in a row',         icon: '🎯',  path: 'fighter' },
  { id: 'speed_demon',    label: 'Speed Demon',      desc: 'Solve a hard problem under 10 min', icon: '⚡',  path: 'fighter' },
  { id: 'perfectionist',  label: 'Perfectionist',    desc: 'First-try on 10 problems',          icon: '💎',  path: 'fighter' },
  { id: 'grinder',        label: 'Grinder',          desc: 'Solve 50 problems total',           icon: '🔥',  path: 'fighter' },
  { id: 'graph_master',   label: 'Graph Master',     desc: 'Complete all graph problems',        icon: '🕸️',  path: 'fighter' },
  { id: 'dp_wizard',      label: 'DP Wizard',        desc: 'Solve 10 DP problems',              icon: '🧙',  path: 'fighter' },
  { id: 'legend_born',    label: 'Legend Born',      desc: 'Achieve LEGEND rank',               icon: '👑',  path: 'fighter' },

  // Sentinel
  { id: 'architect',      label: 'Architect',        desc: 'Complete your first system design', icon: '🏛️',  path: 'sentinel' },
  { id: 'load_balancer',  label: 'Load Balancer',    desc: 'Score 90%+ on 5 designs',           icon: '⚖️',  path: 'sentinel' },
  { id: 'fault_tolerant', label: 'Fault Tolerant',   desc: 'Zero hint usage on 5 problems',     icon: '🛡️',  path: 'sentinel' },
  { id: 'scalable',       label: 'Scalable',         desc: 'Complete 10 HLD problems',          icon: '📈',  path: 'sentinel' },
  { id: 'oracle_born',    label: 'Oracle Born',      desc: 'Achieve ORACLE rank',               icon: '🔮',  path: 'sentinel' },

  // General
  { id: 'streak_7',       label: 'Week Warrior',     desc: '7-day streak',                      icon: '📅',  path: 'general' },
  { id: 'streak_30',      label: 'Month Master',     desc: '30-day streak',                     icon: '🗓️',  path: 'general' },
  { id: 'dual_path',      label: 'Dual Threat',      desc: 'Earn 100 pts on both paths',        icon: '✨',  path: 'general' },
]

export default function AchievementBadges({ earnedIds = [] }) {
  const earned = new Set(earnedIds)

  const sections = [
    { label: '⚔️ Fighter', filter: 'fighter' },
    { label: '🛡️ Sentinel', filter: 'sentinel' },
    { label: '✨ General', filter: 'general' },
  ]

  return (
    <div className="space-y-6">
      {sections.map(({ label, filter }) => {
        const achievements = ACHIEVEMENTS.filter((a) => a.path === filter)
        return (
          <div key={filter}>
            <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">{label}</h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {achievements.map((a) => {
                const unlocked = earned.has(a.id)
                return (
                  <div
                    key={a.id}
                    className={`flex flex-col items-center text-center p-3 rounded-xl border transition-all ${
                      unlocked
                        ? 'border-yellow-700/50 bg-yellow-900/10'
                        : 'border-gray-800 bg-gray-900/50 opacity-40 grayscale'
                    }`}
                    title={a.desc}
                  >
                    <span className="text-2xl mb-1">{a.icon}</span>
                    <span className={`text-xs font-semibold ${unlocked ? 'text-yellow-300' : 'text-gray-500'}`}>
                      {a.label}
                    </span>
                    <span className="text-xs text-gray-600 mt-0.5 leading-tight">{a.desc}</span>
                  </div>
                )
              })}
            </div>
          </div>
        )
      })}
    </div>
  )
}
