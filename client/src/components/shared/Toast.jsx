import { useEffect, useState } from 'react'

export default function Toast({ message, type = 'info', onClose, duration = 3000 }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false)
      onClose?.()
    }, duration)
    return () => clearTimeout(timer)
  }, [duration, onClose])

  if (!visible) return null

  const styles = {
    success: 'bg-green-900 border-green-500 text-green-200',
    error: 'bg-red-900 border-red-500 text-red-200',
    info: 'bg-gray-800 border-gray-600 text-gray-200',
    warning: 'bg-yellow-900 border-yellow-500 text-yellow-200',
  }

  return (
    <div className={`fixed top-16 right-4 z-50 border rounded-lg px-4 py-3 text-sm animate-fade-in shadow-lg ${styles[type]}`}>
      {message}
    </div>
  )
}
