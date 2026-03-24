import { useState } from 'react'

export default function TestCases({ testCases = [], results = [] }) {
  const [activeTab, setActiveTab] = useState(0)

  if (testCases.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-600 text-sm">
        No test cases available.
      </div>
    )
  }

  const getResultStatus = (i) => {
    if (!results[i]) return null
    return results[i].passed ? 'pass' : 'fail'
  }

  const statusStyle = {
    pass: 'text-green-400 border-green-700',
    fail: 'text-red-400 border-red-700',
  }

  return (
    <div className="flex flex-col h-full">
      {/* Tabs */}
      <div className="flex gap-1 px-3 pt-2 pb-1 border-b border-gray-800">
        {testCases.map((_, i) => {
          const status = getResultStatus(i)
          return (
            <button
              key={i}
              onClick={() => setActiveTab(i)}
              className={`px-3 py-1 text-xs rounded-md transition-colors border ${
                activeTab === i
                  ? status
                    ? `bg-gray-800 ${statusStyle[status]}`
                    : 'bg-gray-800 text-white border-gray-600'
                  : `text-gray-500 border-transparent hover:text-gray-300 ${
                      status ? statusStyle[status] : ''
                    }`
              }`}
            >
              Case {i + 1}
              {status === 'pass' && ' ✓'}
              {status === 'fail' && ' ✗'}
            </button>
          )
        })}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3 text-xs font-mono">
        <div>
          <p className="text-gray-500 mb-1">Input</p>
          <pre className="bg-gray-900 rounded p-2 text-gray-200 whitespace-pre-wrap">
            {testCases[activeTab]?.input ?? ''}
          </pre>
        </div>
        <div>
          <p className="text-gray-500 mb-1">Expected Output</p>
          <pre className="bg-gray-900 rounded p-2 text-gray-200 whitespace-pre-wrap">
            {testCases[activeTab]?.expected_output ?? ''}
          </pre>
        </div>
        {results[activeTab] && (
          <div>
            <p className="text-gray-500 mb-1">Your Output</p>
            <pre className={`bg-gray-900 rounded p-2 whitespace-pre-wrap ${
              results[activeTab].passed ? 'text-green-300' : 'text-red-300'
            }`}>
              {results[activeTab].actual_output ?? ''}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}
