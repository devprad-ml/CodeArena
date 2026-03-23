export default function StatsOverview({ stats = {} }) {
  const items = [
    { label: 'Problems Solved', value: stats.total_solved ?? 0 },
    { label: 'Current Streak', value: `${stats.current_streak ?? 0}d` },
    { label: 'First-Try Rate', value: stats.first_try_rate ? `${Math.round(stats.first_try_rate * 100)}%` : '—' },
    { label: 'Total Submissions', value: stats.total_submissions ?? 0 },
  ]

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
      {items.map(({ label, value }) => (
        <div key={label} className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-white">{value}</p>
          <p className="text-xs text-gray-500 mt-1">{label}</p>
        </div>
      ))}
    </div>
  )
}
