import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { submissionService } from '@/services/submissionService'
import { useArenaStore } from '@/store/arenaStore'
import { PATHS } from '@/utils/constants'
import LoadingSpinner from '@/components/shared/LoadingSpinner'

const STATUS_STYLES = {
  accepted:    { label: 'Accepted',    cls: 'text-green-400 bg-green-900/30' },
  wrong_answer:{ label: 'Wrong',       cls: 'text-red-400 bg-red-900/30' },
  time_limit:  { label: 'TLE',         cls: 'text-yellow-400 bg-yellow-900/30' },
  error:       { label: 'Error',       cls: 'text-orange-400 bg-orange-900/30' },
}

const PAGE_SIZE = 10

export default function SubmissionHistory() {
  const { activePath } = useArenaStore()
  const [page, setPage] = useState(0)
  const isFighter = activePath === PATHS.FIGHTER

  const { data: submissions = [], isLoading } = useQuery({
    queryKey: ['submissions-me', activePath],
    queryFn: () => submissionService.getMySubmissions(activePath),
  })

  const paged = submissions.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE)
  const totalPages = Math.ceil(submissions.length / PAGE_SIZE)

  if (isLoading) {
    return (
      <div className="flex justify-center py-8">
        <LoadingSpinner color={activePath} />
      </div>
    )
  }

  if (submissions.length === 0) {
    return (
      <p className="text-gray-600 text-sm text-center py-8">
        No submissions yet. Enter the arena!
      </p>
    )
  }

  return (
    <div>
      <div className="overflow-x-auto rounded-xl border border-gray-800">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800 bg-gray-900">
              <th className="text-left px-4 py-3 text-xs text-gray-500 font-semibold uppercase tracking-wider">Problem</th>
              <th className="text-left px-4 py-3 text-xs text-gray-500 font-semibold uppercase tracking-wider">Status</th>
              <th className="text-left px-4 py-3 text-xs text-gray-500 font-semibold uppercase tracking-wider">Language</th>
              <th className="text-right px-4 py-3 text-xs text-gray-500 font-semibold uppercase tracking-wider">Points</th>
              <th className="text-right px-4 py-3 text-xs text-gray-500 font-semibold uppercase tracking-wider">Date</th>
            </tr>
          </thead>
          <tbody>
            {paged.map((sub, i) => {
              const statusInfo = STATUS_STYLES[sub.status] ?? { label: sub.status, cls: 'text-gray-400 bg-gray-800' }
              const delta = sub.points_delta ?? 0

              return (
                <tr
                  key={sub._id ?? i}
                  className="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors"
                >
                  <td className="px-4 py-3 text-gray-200 font-medium truncate max-w-xs">
                    {sub.problem_title ?? sub.problem_id}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-xs px-2 py-0.5 rounded font-semibold ${statusInfo.cls}`}>
                      {statusInfo.label}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-400 text-xs font-mono capitalize">
                    {sub.language}
                  </td>
                  <td className={`px-4 py-3 text-right font-mono font-bold text-sm ${
                    delta > 0 ? 'text-green-400' : delta < 0 ? 'text-red-400' : 'text-gray-500'
                  }`}>
                    {delta > 0 ? '+' : ''}{delta}
                  </td>
                  <td className="px-4 py-3 text-right text-gray-600 text-xs">
                    {sub.created_at
                      ? new Date(sub.created_at).toLocaleDateString()
                      : '—'}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-3 mt-4">
          <button
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="text-xs text-gray-400 hover:text-white disabled:opacity-30 px-3 py-1 border border-gray-700 rounded-lg transition-colors"
          >
            ← Prev
          </button>
          <span className="text-xs text-gray-500">{page + 1} / {totalPages}</span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={page === totalPages - 1}
            className="text-xs text-gray-400 hover:text-white disabled:opacity-30 px-3 py-1 border border-gray-700 rounded-lg transition-colors"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  )
}
