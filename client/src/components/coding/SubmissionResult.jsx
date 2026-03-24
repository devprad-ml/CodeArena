import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useArenaStore } from '@/store/arenaStore'
import { getRankForPoints } from '@/utils/helpers'
import { PATHS } from '@/utils/constants'

export default function SubmissionResult({ result, previousPoints, currentPoints, path, onClose }) {
  const navigate = useNavigate()
  const [showRankUp, setShowRankUp] = useState(false)

  const prevRank = getRankForPoints(previousPoints, path)
  const newRank = getRankForPoints(currentPoints, path)
  const rankChanged = prevRank.name !== newRank.name
  const pointDelta = currentPoints - previousPoints
  const passed = result?.status === 'accepted'
  const isFighter = path === PATHS.FIGHTER

  useEffect(() => {
    if (rankChanged) {
      const t = setTimeout(() => setShowRankUp(true), 600)
      return () => clearTimeout(t)
    }
  }, [rankChanged])

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
      <div className="relative bg-gray-900 border border-gray-700 rounded-2xl p-8 w-full max-w-md mx-4 text-center shadow-2xl">

        {/* Status icon */}
        <div className="text-6xl mb-4">
          {passed ? '✅' : '❌'}
        </div>

        <h2 className={`font-display font-bold text-3xl mb-1 ${passed ? 'text-green-400' : 'text-red-400'}`}>
          {passed ? 'Accepted!' : 'Wrong Answer'}
        </h2>

        {result?.message && (
          <p className="text-gray-400 text-sm mb-4">{result.message}</p>
        )}

        {/* Points delta */}
        <div className={`inline-block px-4 py-2 rounded-lg font-mono font-bold text-xl mb-6 ${
          pointDelta >= 0 ? 'bg-green-900/40 text-green-300' : 'bg-red-900/40 text-red-300'
        }`}>
          {pointDelta >= 0 ? '+' : ''}{pointDelta} pts
        </div>

        {/* Test case summary */}
        {result?.test_results && (
          <div className="flex justify-center gap-4 mb-6 text-sm">
            <span className="text-green-400">
              ✓ {result.test_results.filter((t) => t.passed).length} passed
            </span>
            <span className="text-red-400">
              ✗ {result.test_results.filter((t) => !t.passed).length} failed
            </span>
          </div>
        )}

        {/* Rank-up banner */}
        {rankChanged && showRankUp && (
          <div
            className="mb-6 p-4 rounded-xl border animate-rank-up"
            style={{
              borderColor: newRank.color,
              backgroundColor: `${newRank.color}15`,
            }}
          >
            <p className="text-xs text-gray-400 mb-1 uppercase tracking-wider">Rank Up!</p>
            <p className="text-gray-400 text-sm line-through">{prevRank.name}</p>
            <p className="font-display font-bold text-2xl" style={{ color: newRank.color }}>
              {newRank.name}
            </p>
            {newRank.supreme && (
              <p className="text-xs mt-1" style={{ color: newRank.color }}>★ Supreme Rank ★</p>
            )}
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 py-2.5 rounded-lg border border-gray-700 text-gray-300 hover:text-white hover:border-gray-500 text-sm transition-colors"
          >
            Next Problem
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className={`flex-1 py-2.5 rounded-lg text-white text-sm font-semibold transition-colors ${
              isFighter
                ? 'bg-fighter-primary hover:bg-red-700'
                : 'bg-sentinel-primary hover:bg-blue-700'
            }`}
          >
            Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}
