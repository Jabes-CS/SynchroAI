import { Link } from 'react-router-dom'
import {
  Heart,
  Users,
  Target,
  Award,
  Shield,
  ArrowRight,
  AlertTriangle,
  CheckCircle2,
} from 'lucide-react'

export default function Home() {
  return (
    <div>
      {/* HERO — primeira tela */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28">
          <div className="text-center max-w-3xl mx-auto">
            <span className="inline-block px-4 py-1 bg-blue-500/30 backdrop-blur text-blue-100 text-sm font-medium rounded-full mb-6">
              🏆 Hackathon UNASP + IBM 2026
            </span>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              Orquestrando voluntariado em
              <span className="block text-yellow-300">situações de crise</span>
            </h1>
            <p className="text-xl text-blue-100 mb-10 leading-relaxed">
              SynchroAI conecta voluntários e instituições com inteligência artificial,
              priorizando urgência, habilidades e bem-estar para maximizar o impacto social.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/cadastro"
                className="inline-flex items-center justify-center gap-2 px-8 py-3 bg-white text-blue-700 font-semibold rounded-lg hover:bg-blue-50 transition shadow-lg"
              >
                Quero ser voluntário
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/tasks"
                className="inline-flex items-center justify-center gap-2 px-8 py-3 bg-blue-500/30 backdrop-blur border border-white/30 text-white font-semibold rounded-lg hover:bg-blue-500/40 transition"
              >
                Ver necessidades abertas
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* PROBLEMA — RS 2024 */}
      <section className="bg-red-50 py-16">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-red-100 text-red-700 text-sm font-medium rounded-full mb-4">
              <AlertTriangle className="w-4 h-4" />
              O problema é real
            </div>
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Enchentes do Rio Grande do Sul, 2024
            </h2>
            <p className="text-lg text-gray-700 max-w-2xl mx-auto">
              Milhares de pessoas se voluntariaram. A coordenação foi caótica.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="text-3xl font-bold text-red-600 mb-2">200+</div>
              <p className="text-sm text-gray-600">
                Médicos cadastrados que não chegaram ao destino certo por falta de coordenação.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="text-3xl font-bold text-red-600 mb-2">73%</div>
              <p className="text-sm text-gray-600">
                Voluntários relataram não saber em qual tarefa seriam mais úteis.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="text-3xl font-bold text-red-600 mb-2">∞</div>
              <p className="text-sm text-gray-600">
                Doações de roupas sobrando enquanto faltavam itens essenciais como água potável.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* SOLUÇÃO — 4 agentes */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 text-sm font-medium rounded-full mb-4">
              <CheckCircle2 className="w-4 h-4" />
              A nossa solução
            </div>
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              4 Agentes de IA trabalhando em conjunto
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Cada agente é especialista em uma parte crítica do voluntariado, orquestrados pelo IBM watsonx Orchestrate.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <AgentCard
              icon={<Users className="w-7 h-7" />}
              color="blue"
              name="Perfilador"
              description="Coleta habilidades, disponibilidade e contexto de cada voluntário."
            />
            <AgentCard
              icon={<Target className="w-7 h-7" />}
              color="green"
              name="Pareador"
              description="Casa voluntários com necessidades, priorizando urgência e proximidade."
            />
            <AgentCard
              icon={<Heart className="w-7 h-7" />}
              color="pink"
              name="Bem-estar"
              description="Previne burnout através de revezamento entre voluntários compatíveis."
            />
            <AgentCard
              icon={<Award className="w-7 h-7" />}
              color="yellow"
              name="Pontuação"
              description="Reconhece o trabalho realizado com pontos e bônus de bem-estar."
            />
          </div>
        </div>
      </section>

      {/* CTA FINAL */}
      <section className="bg-gradient-to-br from-gray-900 to-blue-900 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Shield className="w-12 h-12 mx-auto text-blue-400 mb-4" />
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Pronto para fazer parte?
          </h2>
          <p className="text-lg text-blue-100 mb-8 max-w-2xl mx-auto">
            Cadastre-se em menos de 2 minutos e seja conectado a quem mais precisa do seu apoio.
          </p>
          <Link
            to="/cadastro"
            className="inline-flex items-center gap-2 px-8 py-3 bg-yellow-400 hover:bg-yellow-300 text-gray-900 font-bold rounded-lg transition shadow-lg"
          >
            Cadastrar agora
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  )
}

/**
 * Componente auxiliar para o card de cada agente.
 */
function AgentCard({ icon, color, name, description }) {
  const colors = {
    blue: 'bg-blue-100 text-blue-700',
    green: 'bg-green-100 text-green-700',
    pink: 'bg-pink-100 text-pink-700',
    yellow: 'bg-yellow-100 text-yellow-700',
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition">
      <div className={`w-14 h-14 rounded-xl ${colors[color]} flex items-center justify-center mb-4`}>
        {icon}
      </div>
      <h3 className="text-lg font-bold text-gray-900 mb-2">Agente {name}</h3>
      <p className="text-sm text-gray-600 leading-relaxed">{description}</p>
    </div>
  )
}