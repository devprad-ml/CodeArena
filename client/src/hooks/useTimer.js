import { useEffect, useCallback } from 'react'
import { useArenaStore } from '@/store/arenaStore'

export function useTimer(initialSeconds = 1800) {
  const { timerSeconds, timerRunning, setTimerSeconds, setTimerRunning } = useArenaStore()

  useEffect(() => {
    if (!timerRunning || timerSeconds <= 0) return
    const interval = setInterval(() => {
      setTimerSeconds(timerSeconds - 1)
    }, 1000)
    return () => clearInterval(interval)
  }, [timerRunning, timerSeconds, setTimerSeconds])

  const start = useCallback(() => {
    setTimerSeconds(initialSeconds)
    setTimerRunning(true)
  }, [initialSeconds, setTimerSeconds, setTimerRunning])

  const pause = useCallback(() => setTimerRunning(false), [setTimerRunning])
  const resume = useCallback(() => setTimerRunning(true), [setTimerRunning])
  const reset = useCallback(() => {
    setTimerRunning(false)
    setTimerSeconds(initialSeconds)
  }, [initialSeconds, setTimerRunning, setTimerSeconds])

  return { seconds: timerSeconds, running: timerRunning, start, pause, resume, reset }
}
