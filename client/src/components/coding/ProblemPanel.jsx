import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useArenaStore } from '@/store/arenaStore'
import { aiService } from '@/services/aiService'
import { PATHS, SCORING } from '@/utils/constants'
import LoadingSpinner from '@/components/shared/LoadingSpinner'

const DIFFICULTY_COLORS = {
  Easy: 'text-green-400',
  'Easy-Medium': 'text-green-300',
  Medium: 'text-yellow-400',
  'Medium-Hard': 'text-orange-400',
  Hard: 'text-red-400',
  Expert: 'text-red-600',
}

export default function ProblemPanel() {
  const { currentProblem, code, activePath } = useArenaStore()
  const [hint, setHint] = useState(null)
  const isFighter = activePath === PATHS.FIGHTER

  const hintMutation = useMutation({
    mutationFn: () => aiService.getHint(currentProblem._id, code),
    onSuccess: (data) => setHint(data.hint),
  })

  if (!currentProblem) {
    return (
      <div className="h-full flex items-center justify-center text-gray-600">
        <p className="text-sm">No problem loaded.</p>
      </div>
    )
  }

  const { title, difficulty, category, description, examples = [], constraints = [] } = currentProblem

  return (
    <div className="h-full overflow-y-auto px-5 py-4 text-sm text-gray-300">
      {/* Header */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-1">
          <span className={`font-semibold ${DIFFICULTY_COLORS[difficulty] ?? 'text-gray-400'}`}>
            {difficulty}
          </span>
          {category && (
            <span className="text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded">{category}</span>
          )}
        </div>
        <h2 className="text-white font-semibold text-base leading-snug">{title}</h2>
      </div>

      {/* Description */}
      <div className="mb-5 leading-relaxed whitespace-pre-wrap text-gray-300">
        {description}
      </div>

      {/* Examples */}
      {examples.length > 0 && (
        <div className="mb-5">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Examples</h3>
          {examples.map((ex, i) => (
            <div key={i} className="mb-3 bg-gray-900 rounded-lg p-3 border border-gray-800">
              <p className="text-xs text-gray-400 mb-1">
                <span className="font-semibold text-gray-300">Input:</span> {ex.input}
              </p>
              <p className="text-xs text-gray-400 mb-1">
                <span className="font-semibold text-gray-300">Output:</span> {ex.output}
              </p>
              {ex.explanation && (
                <p className="text-xs text-gray-500 mt-1">
                  <span className="font-semibold">Explanation:</span> {ex.explanation}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Constraints */}
      {constraints.length > 0 && (
        <div className="mb-5">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Constraints</h3>
          <ul className="list-disc list-inside space-y-1">
            {constraints.map((c, i) => (
              <li key={i} className="text-xs text-gray-400 font-mono">{c}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Hint */}
      <div className="mt-auto pt-4 border-t border-gray-800">
        {hint ? (
          <div className="bg-yellow-900/30 border border-yellow-700/40 rounded-lg p-3">
            <p className="text-xs text-yellow-500 font-semibold mb-1">Hint ({SCORING.HINT_PENALTY} pts)</p>
            <p className="text-xs text-yellow-200">{hint}</p>
          </div>
        ) : (
          <button
            onClick={() => hintMutation.mutate()}
            disabled={hintMutation.isPending}
            className="flex items-center gap-2 text-xs text-yellow-500 hover:text-yellow-300 transition-colors disabled:opacity-50"
          >
            {hintMutation.isPending ? (
              <LoadingSpinner size="sm" color="white" />
            ) : (
              '💡'
            )}
            Get Hint ({SCORING.HINT_PENALTY} pts)
          </button>
        )}
      </div>
    </div>
  )
}
