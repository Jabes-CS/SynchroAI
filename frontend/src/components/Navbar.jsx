import { Heart } from 'lucide-react'

export default function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center h-16">
          <div className="flex items-center gap-2">
            <Heart className="w-7 h-7 text-blue-600" fill="currentColor" />
            <span className="text-xl font-bold text-gray-900">
              Synchro<span className="text-blue-600">AI</span>
            </span>
          </div>

          <div className="ml-auto hidden md:flex items-center gap-2 text-sm text-gray-500">
            <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full font-medium">
              Hackathon UNASP + IBM 2026
            </span>
          </div>
        </div>
      </div>
    </nav>
  )
}