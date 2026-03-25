import { useEffect } from 'react'
import { formatDuration } from '@/utils/helpers'
import { useArenaStore } from '@/store/arenaStore'

export default function Timer({ onExpire }) {
  const { timerSeconds, timerRunning } = useArenaStore()

  useEffect(() => {
    if (timerRunning && timerSeconds <= 0 && onExpire) onExpire()
  }, [timerSeconds, timerRunning])

  const getColor = () => {
    if (timerSeconds > 600) return 'text-green-400'
    if (timerSeconds > 180) return 'text-yellow-400'
    return 'text-red-500 animate-pulse'
  }

  return (
    <div className={`font-mono text-lg font-bold tabular-nums ${getColor()}`}>
      {formatDuration(timerSeconds)}
    </div>
  )
}
