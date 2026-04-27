export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
          <div>
            <span className="font-bold text-white">SynchroAI</span>
            <span className="mx-2">·</span>
            <span>Jabes Candido & Nickolas Bragato</span>
          </div>
          <div className="text-xs text-gray-500">
            UNASP + IBM Hackathon 2026 · Powered by watsonx Orchestrate
          </div>
        </div>
      </div>
    </footer>
  )
}