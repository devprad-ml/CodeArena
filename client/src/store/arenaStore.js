import { create } from 'zustand'
import { PATHS } from '@/utils/constants'

export const useArenaStore = create((set) => ({
  activePath: PATHS.FIGHTER,
  currentProblem: null,
  timerSeconds: 0,
  timerRunning: false,
  language: 'python',
  code: '',
  submissionResult: null,

  setActivePath: (path) => set({ activePath: path }),
  setCurrentProblem: (problem) => set({ currentProblem: problem }),
  setLanguage: (language) => set({ language }),
  setCode: (code) => set({ code }),
  setSubmissionResult: (result) => set({ submissionResult: result }),
  setTimerSeconds: (seconds) => set({ timerSeconds: seconds }),
  setTimerRunning: (running) => set({ timerRunning: running }),
  resetArena: () => set({ currentProblem: null, code: '', submissionResult: null, timerSeconds: 0, timerRunning: false }),
}))
