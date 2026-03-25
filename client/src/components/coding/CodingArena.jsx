import { useEffect, useRef, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useArenaStore } from '@/store/arenaStore'
import { useAuthStore } from '@/store/authStore'
import { useTimer } from '@/hooks/useTimer'
import { problemService } from '@/services/problemService'
import { submissionService } from '@/services/submissionService'
import { PATHS, TIMER_OPTIONS, getWsUrl } from '@/utils/constants'
import { CODE_TEMPLATES } from '@/utils/codeTemplates'

import ProblemPanel from './ProblemPanel'
import CodeEditor from './CodeEditor'
import Timer from './Timer'
import LanguageSelector from './LanguageSelector'
import TestCases from './TestCases'
import ConsoleOutput from './ConsoleOutput'
import SubmissionResult from './SubmissionResult'
import LoadingSpinner from '@/components/shared/LoadingSpinner'

export default function CodingArena() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const {
    activePath, currentProblem, setCurrentProblem,
    language, code, setCode,
    submissionResult, setSubmissionResult,
    resetArena,
  } = useArenaStore()

  const isFighter = activePath === PATHS.FIGHTER
  const [bottomTab, setBottomTab] = useState('testcases') // 'testcases' | 'console'
  const [selectedMinutes, setSelectedMinutes] = useState(30)
  const [consoleOutput, setConsoleOutput] = useState({ output: '', error: '', isRunning: false })
  const [previousPoints, setPreviousPoints] = useState(0)
  const [testResults, setTestResults] = useState([])
  const [wsStatus, setWsStatus] = useState(null) // null | 'connecting' | 'running' | 'done' | 'error'
  const wsRef = useRef(null)

  const { seconds, running, start, pause, resume, reset } = useTimer(selectedMinutes * 60)

  // Clean up WebSocket on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
    }
  }, [])

  // Load a random problem when the arena mounts
  const { data: fetchedProblem, isError: problemError } = useQuery({
    queryKey: ['random-problem', activePath],
    queryFn: () => problemService.getRandomProblem(activePath, null),
    enabled: !currentProblem,
    staleTime: Infinity,
    retry: 1,
  })

  useEffect(() => {
    if (fetchedProblem && !currentProblem) {
      setCurrentProblem(fetchedProblem)
      setCode(CODE_TEMPLATES[language] ?? '')
    }
  }, [fetchedProblem])

  // Reset code template when language changes
  useEffect(() => {
    if (!code || Object.values(CODE_TEMPLATES).includes(code)) {
      setCode(CODE_TEMPLATES[language] ?? '')
    }
  }, [language])

  const connectSubmissionWs = (submissionId) => {
    // Close any existing connection
    if (wsRef.current) {
      wsRef.current.close()
    }

    setWsStatus('connecting')
    const ws = new WebSocket(getWsUrl(`/ws/submission/${submissionId}`))
    wsRef.current = ws

    ws.onopen = () => {
      setWsStatus('running')
    }

    ws.onmessage = (event) => {
      let payload
      try { payload = JSON.parse(event.data) } catch { return }

      if (payload.event === 'status') {
        setWsStatus('running')
        setConsoleOutput((prev) => ({ ...prev, isRunning: true }))
      } else if (payload.event === 'result') {
        setWsStatus('done')
        setConsoleOutput({
          output: payload.stdout ?? '',
          error: payload.stderr ?? '',
          isRunning: false,
        })
        setTestResults(payload.test_results ?? [])
        setSubmissionResult(payload)
        queryClient.invalidateQueries({ queryKey: ['me'] })
        ws.close()
        wsRef.current = null
      } else if (payload.event === 'error') {
        setWsStatus('error')
        setConsoleOutput({ output: '', error: payload.message ?? 'Execution error', isRunning: false })
        ws.close()
        wsRef.current = null
      }
    }

    ws.onerror = () => {
      setWsStatus('error')
      setConsoleOutput({ output: '', error: 'Connection lost. Please try again.', isRunning: false })
      wsRef.current = null
    }
  }

  // Submit mutation — POST creates the submission, then WS streams the result
  const submitMutation = useMutation({
    mutationFn: () => submissionService.submit(currentProblem._id, code, language),
    onMutate: () => {
      const pts = activePath === PATHS.FIGHTER
        ? user?.fighter_progress?.points ?? 0
        : user?.sentinel_progress?.points ?? 0
      setPreviousPoints(pts)
      setConsoleOutput({ output: '', error: '', isRunning: true })
      setBottomTab('console')
    },
    onSuccess: (data) => {
      // data.id is the submission ID — open WS to stream real-time status
      if (data?.id) {
        connectSubmissionWs(data.id)
      } else {
        // Fallback: server returned a completed result directly
        setConsoleOutput({ output: data.stdout ?? '', error: data.stderr ?? '', isRunning: false })
        setTestResults(data.test_results ?? [])
        setSubmissionResult(data)
        queryClient.invalidateQueries({ queryKey: ['me'] })
      }
    },
    onError: (err) => {
      setConsoleOutput({ output: '', error: err.message, isRunning: false })
    },
  })

  const handleNextProblem = () => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    setWsStatus(null)
    resetArena()
    setTestResults([])
    setConsoleOutput({ output: '', error: '', isRunning: false })
    queryClient.invalidateQueries({ queryKey: ['random-problem', activePath] })
  }

  if (problemError) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center flex-col gap-3">
        <p className="text-red-400 text-sm">Failed to load problem. Check the console.</p>
        <button onClick={() => window.location.reload()} className="text-xs text-gray-400 underline">Retry</button>
      </div>
    )
  }

  if (!currentProblem) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <LoadingSpinner size="lg" color={activePath} />
      </div>
    )
  }

  const accentClass = isFighter ? 'border-fighter-primary' : 'border-sentinel-primary'
  const btnClass = isFighter
    ? 'bg-fighter-primary hover:bg-red-700'
    : 'bg-sentinel-primary hover:bg-blue-700'

  return (
    <div className="h-screen bg-gray-950 flex flex-col pt-14 overflow-hidden">
      {/* Top bar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800 bg-gray-900 shrink-0">
        {/* Left: path badge + problem title */}
        <div className="flex items-center gap-3 min-w-0">
          <span className={`text-xs font-semibold uppercase tracking-wider px-2 py-0.5 rounded border ${
            isFighter ? 'text-fighter-primary border-fighter-border' : 'text-sentinel-primary border-sentinel-border'
          }`}>
            {activePath}
          </span>
          <span className="text-gray-300 text-sm font-medium truncate">
            {currentProblem?.title ?? 'Loading...'}
          </span>
        </div>

        {/* Center: timer controls */}
        <div className="flex items-center gap-3">
          <select
            value={selectedMinutes}
            onChange={(e) => {
              setSelectedMinutes(Number(e.target.value))
              reset()
            }}
            className="bg-gray-800 border border-gray-700 text-gray-300 text-xs rounded px-2 py-1 focus:outline-none"
            disabled={running}
          >
            {TIMER_OPTIONS.map((m) => (
              <option key={m} value={m}>{m} min</option>
            ))}
          </select>
          {!running ? (
            <button
              onClick={seconds > 0 ? resume : start}
              className="text-xs text-green-400 hover:text-green-300 border border-green-800 px-2 py-1 rounded transition-colors"
            >
              {seconds > 0 ? 'Resume' : 'Start'}
            </button>
          ) : (
            <button
              onClick={pause}
              className="text-xs text-yellow-400 hover:text-yellow-300 border border-yellow-800 px-2 py-1 rounded transition-colors"
            >
              Pause
            </button>
          )}
          <Timer onExpire={() => pause()} />
        </div>

        {/* Right: language + actions */}
        <div className="flex items-center gap-2">
          <LanguageSelector />
          <button
            onClick={handleNextProblem}
            className="text-xs text-gray-400 hover:text-white border border-gray-700 px-3 py-1.5 rounded-lg transition-colors"
          >
            Skip (−2)
          </button>
          <button
            onClick={() => submitMutation.mutate()}
            disabled={submitMutation.isPending || wsStatus === 'connecting' || wsStatus === 'running' || !code.trim()}
            className={`text-xs text-white px-4 py-1.5 rounded-lg font-semibold transition-colors disabled:opacity-50 ${btnClass}`}
          >
            {submitMutation.isPending || wsStatus === 'connecting'
              ? 'Submitting...'
              : wsStatus === 'running'
              ? 'Running...'
              : 'Submit'}
          </button>
        </div>
      </div>

      {/* Main split: problem | editor */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: problem panel */}
        <div className={`w-2/5 border-r border-gray-800 overflow-hidden flex flex-col`}>
          <ProblemPanel />
        </div>

        {/* Right: editor + bottom panel */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Editor — takes up ~65% of right side */}
          <div className="flex-1 overflow-hidden">
            <CodeEditor />
          </div>

          {/* Bottom panel — test cases / console */}
          <div className="h-48 border-t border-gray-800 flex flex-col shrink-0">
            <div className="flex border-b border-gray-800 bg-gray-900 shrink-0">
              {['testcases', 'console'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setBottomTab(tab)}
                  className={`px-4 py-2 text-xs capitalize transition-colors ${
                    bottomTab === tab
                      ? `text-white border-b-2 ${isFighter ? 'border-fighter-primary' : 'border-sentinel-primary'}`
                      : 'text-gray-500 hover:text-gray-300'
                  }`}
                >
                  {tab === 'testcases' ? 'Test Cases' : 'Console'}
                </button>
              ))}
            </div>
            <div className="flex-1 overflow-hidden">
              {bottomTab === 'testcases' ? (
                <TestCases
                  testCases={currentProblem?.test_cases ?? []}
                  results={testResults}
                />
              ) : (
                <ConsoleOutput {...consoleOutput} />
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Submission result overlay */}
      {submissionResult && (
        <SubmissionResult
          result={submissionResult}
          previousPoints={previousPoints}
          currentPoints={
            (activePath === PATHS.FIGHTER
              ? user?.fighter_progress?.points
              : user?.sentinel_progress?.points) ?? 0
          }
          path={activePath}
          onClose={() => {
            setSubmissionResult(null)
            handleNextProblem()
          }}
        />
      )}
    </div>
  )
}
