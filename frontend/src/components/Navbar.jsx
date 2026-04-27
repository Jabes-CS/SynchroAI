import { Link, NavLink } from 'react-router-dom'
import { Heart, Users, LayoutDashboard, ListChecks, MessageCircle } from 'lucide-react'

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition ${
      isActive
        ? 'bg-blue-100 text-blue-700'
        : 'text-gray-700 hover:bg-gray-100'
    }`

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center gap-2">
            <Heart className="w-7 h-7 text-blue-600" fill="currentColor" />
            <span className="text-xl font-bold text-gray-900">
              Synchro<span className="text-blue-600">AI</span>
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-2">
            <NavLink to="/cadastro" className={linkClass}>
              <Users className="w-4 h-4" />
              Cadastro
            </NavLink>
            <NavLink to="/dashboard" className={linkClass}>
              <LayoutDashboard className="w-4 h-4" />
              Dashboard
            </NavLink>
            <NavLink to="/tasks" className={linkClass}>
              <ListChecks className="w-4 h-4" />
              Necessidades
            </NavLink>
          </div>

          <a
            href="https://dl.watson-orchestrate.ibm.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition shadow-sm"
          >
            <MessageCircle className="w-4 h-4" />
            Conversar com IA
          </a>
        </div>
      </div>
    </nav>
  )
}