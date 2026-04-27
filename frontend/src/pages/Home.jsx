import { useState } from 'react'
import {
  Heart,
  Users,
  Target,
  Award,
  Shield,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
  MessageCircle,
  ArrowDown,
} from 'lucide-react'

import ChatEmbed from '../components/ChatEmbed'

export default function Home() {
  const [showContext, setShowContext] = useState(false)

  return (
    <>
      {/* HERO compacto */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
          <div className="text-center">
            <span className="inline-block px-4 py-1 bg-blue-500/30 backdrop-blur text-blue-100 text-xs font-medium rounded-full mb-4">
              🏆 Hackathon UNASP + IBM 2026
            </span>
            <h1 className="text-3xl md:text-5xl font-bold mb-4 leading-tight">
              Voluntariado inteligente para
              <span className="block text-yellow-300 mt-1">situações de crise</span>
            </h1>
            <p className="text-lg text-blue-100 max-w-2xl mx-auto mb-6">
              Cadastre-se, encontre oportunidades de ajuda ou registre seu impacto.
              Tudo conversando com nossos agentes de IA.
            </p>

            {/* CTA — apontando para o botão flutuante */}
            <div className="inline-flex items-center gap-2 px-6 py-3 bg-yellow-400 text-gray-900 font-semibold rounded-full shadow-lg">
              <ArrowDown className="w-5 h-5 animate-bounce" />
              Clique no chat azul no canto da tela
              <MessageCircle className="w-5 h-5" />
            </div>

            <div className="mt-6">
              <button
                onClick={() => setShowContext(!showContext)}
                className="inline-flex items-center gap-2 text-sm text-blue-200 hover:text-white transition"
              >
                {showContext ? 'Ocultar contexto' : 'Por que esse projeto existe?'}
                {showContext ? (
                  <ChevronUp className="w-4 h-4" />
                ) : (
                  <ChevronDown className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Contexto expansível — RS 2024 */}
      {showContext && (
        <section className="bg-red-50 py-10 border-b border-red-100">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-start gap-3 mb-6">
              <AlertTriangle className="w-6 h-6 text-red-600 flex-shrink-0 mt-1" />
              <div>
                <h2 className="text-xl font-bold text-gray-900">
                  Enchentes do Rio Grande do Sul, 2024
                </h2>
                <p className="text-gray-700 mt-1">
                  Milhares de pessoas se voluntariaram. A coordenação foi caótica.
                </p>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-4">
              <StatCard value="200+" text="Médicos cadastrados que não chegaram ao destino certo." />
              <StatCard value="73%" text="Voluntários sem clareza de onde seriam mais úteis." />
              <StatCard value="∞" text="Doações desorganizadas — falta de água, sobra de roupas." />
            </div>
          </div>
        </section>
      )}

      {/* Os 4 agentes */}
      <section className="py-12 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-3">
              4 Agentes de IA trabalhando juntos
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Quando você abre o chat, fala primeiro com o Coordenador. Ele
              encaminha sua solicitação ao especialista certo.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <AgentCard
              icon={<Users className="w-6 h-6" />}
              color="blue"
              name="Perfilador"
              description="Coleta habilidades, disponibilidade e contexto."
            />
            <AgentCard
              icon={<Target className="w-6 h-6" />}
              color="green"
              name="Pareador"
              description="Casa voluntários e necessidades por urgência."
            />
            <AgentCard
              icon={<Heart className="w-6 h-6" />}
              color="pink"
              name="Bem-estar"
              description="Previne burnout através de revezamento."
            />
            <AgentCard
              icon={<Award className="w-6 h-6" />}
              color="yellow"
              name="Pontuação"
              description="Reconhece o trabalho com pontos e bônus."
            />
          </div>
        </div>
      </section>

      {/* Selo IBM */}
      <section className="bg-gradient-to-br from-gray-900 to-blue-900 text-white py-10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Shield className="w-10 h-10 mx-auto text-blue-400 mb-3" />
          <h2 className="text-xl md:text-2xl font-bold mb-2">
            Powered by IBM watsonx Orchestrate
          </h2>
          <p className="text-blue-100 text-sm max-w-2xl mx-auto">
            Múltiplos agentes de IA coordenados em tempo real, integrados ao
            backend do SynchroAI para cadastros e matches reais.
          </p>
        </div>
      </section>

      {/* Componente que injeta o widget IBM (não renderiza nada visível) */}
      <ChatEmbed />
    </>
  )
}

// ============================================
// COMPONENTES AUXILIARES
// ============================================

function StatCard({ value, text }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-red-100">
      <div className="text-2xl font-bold text-red-600 mb-1">{value}</div>
      <p className="text-xs text-gray-600">{text}</p>
    </div>
  )
}

function AgentCard({ icon, color, name, description }) {
  const colors = {
    blue: 'bg-blue-100 text-blue-700',
    green: 'bg-green-100 text-green-700',
    pink: 'bg-pink-100 text-pink-700',
    yellow: 'bg-yellow-100 text-yellow-700',
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md hover:border-blue-300 transition">
      <div className={`w-12 h-12 rounded-xl ${colors[color]} flex items-center justify-center mb-3`}>
        {icon}
      </div>
      <h3 className="font-bold text-gray-900 mb-1">Agente {name}</h3>
      <p className="text-sm text-gray-600 leading-relaxed">{description}</p>
    </div>
  )
}