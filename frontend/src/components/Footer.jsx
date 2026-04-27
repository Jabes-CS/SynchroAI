export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-bold text-white mb-2">SynchroAI</h3>
            <p className="text-sm">
              Orquestrando voluntariado inteligente para situações de crise.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-2">Tecnologia</h4>
            <ul className="text-sm space-y-1">
              <li>IBM watsonx Orchestrate</li>
              <li>FastAPI + PostgreSQL</li>
              <li>React + Tailwind CSS</li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-2">Equipe</h4>
            <ul className="text-sm space-y-1">
              <li>Jabes Candido da Silva</li>
              <li>Nickolas Bragato</li>
              <li className="text-xs text-gray-500 pt-1">UNASP — 2026</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-6 pt-4 text-center text-xs text-gray-500">
          Feito com 💙 durante o Hackathon IA Descomplicada — UNASP + IBM 2026
        </div>
      </div>
    </footer>
  )
}