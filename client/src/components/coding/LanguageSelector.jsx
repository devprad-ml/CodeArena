import { SUPPORTED_LANGUAGES } from '@/utils/constants'
import { useArenaStore } from '@/store/arenaStore'

export default function LanguageSelector() {
  const { language, setLanguage } = useArenaStore()

  return (
    <select
      value={language}
      onChange={(e) => setLanguage(e.target.value)}
      className="bg-gray-800 border border-gray-700 text-gray-200 text-sm rounded-lg px-3 py-1.5 focus:outline-none focus:border-gray-500 cursor-pointer"
    >
      {SUPPORTED_LANGUAGES.map((lang) => (
        <option key={lang.id} value={lang.id}>
          {lang.label}
        </option>
      ))}
    </select>
  )
}
