import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="border-t border-gray-800 bg-gray-950 py-6 px-4 mt-auto">
      <div className="max-w-4xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-gray-600">
        <span className="font-display font-bold tracking-widest">
          <span className="text-fighter-primary">CODE</span>
          <span className="text-gray-500">ARENA</span>
        </span>
        <div className="flex gap-5">
          <Link to="/dashboard" className="hover:text-gray-400 transition-colors">Dashboard</Link>
          <Link to="/arena" className="hover:text-gray-400 transition-colors">Arena</Link>
          <Link to="/profile" className="hover:text-gray-400 transition-colors">Profile</Link>
        </div>
        <span>© {new Date().getFullYear()} CodeArena</span>
      </div>
    </footer>
  )
}
