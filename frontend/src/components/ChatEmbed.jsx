import { useEffect } from 'react'

/**
 * ChatEmbed — Carrega o widget oficial do IBM watsonx Orchestrate.
 *
 * IMPORTANTE: o widget renderiza dentro de #wxo-chat (uma div separada
 * do #root onde o React vive), pra não sobrescrever a aplicação.
 */
export default function ChatEmbed() {
  useEffect(() => {
    // Evita carregamento duplicado (StrictMode chama useEffect 2x em dev)
    if (document.getElementById('wxo-loader-script')) {
      return
    }

    // Configuração do widget IBM — APONTA pra #wxo-chat, NÃO #root
    window.wxOConfiguration = {
      orchestrationID:
        '20260422-2251-1570-00f3-3cdb8b5547d2_20260422-2251-4824-70fa-4985ad60bce7',
      hostURL: 'https://dl.watson-orchestrate.ibm.com',
      rootElementID: 'wxo-chat', // ← mudou de 'root' pra 'wxo-chat'
      chatOptions: {
        agentId: 'abe3f124-1559-404e-9fcd-586480f12366',
      },
    }

    const script = document.createElement('script')
    script.id = 'wxo-loader-script'
    script.src = `${window.wxOConfiguration.hostURL}/wxochat/wxoLoader.js?embed=true`
    script.async = true

    script.addEventListener('load', () => {
      if (window.wxoLoader && typeof window.wxoLoader.init === 'function') {
        window.wxoLoader.init()
      }
    })

    document.head.appendChild(script)
  }, [])

  return null
}