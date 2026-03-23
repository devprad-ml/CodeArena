export default function ConsoleOutput({ output = '', error = '', isRunning = false }) {
  const hasError = !!error
  const isEmpty = !output && !error && !isRunning

  return (
    <div className="h-full flex flex-col bg-gray-950 font-mono text-xs">
      <div className="px-3 py-1.5 border-b border-gray-800 flex items-center gap-2">
        <span className="text-gray-500 text-xs uppercase tracking-wider">Console</span>
        {isRunning && (
          <span className="text-yellow-400 text-xs animate-pulse">● Running...</span>
        )}
        {!isRunning && output && (
          <span className="text-green-400 text-xs">● Done</span>
        )}
        {!isRunning && hasError && (
          <span className="text-red-400 text-xs">● Error</span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        {isEmpty && (
          <p className="text-gray-700">Run your code to see output here.</p>
        )}
        {output && (
          <pre className="text-gray-200 whitespace-pre-wrap">{output}</pre>
        )}
        {hasError && (
          <pre className="text-red-400 whitespace-pre-wrap">{error}</pre>
        )}
      </div>
    </div>
  )
}
