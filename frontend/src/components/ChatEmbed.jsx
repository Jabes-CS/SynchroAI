import { useEffect } from 'react'

const API_URL =
  import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV
    ? 'http://localhost:8000'
    : 'https://synchroai-api.onrender.com')

async function fetchAuthToken() {
  const res = await fetch(`${API_URL}/chat/token`)
  if (!res.ok) {
    throw new Error(`Falha ao obter token do chat: ${res.status}`)
  }
  const data = await res.json()
  return data.token
}

export default function ChatEmbed() {
  useEffect(() => {
    if (document.getElementById('wxo-loader-script')) {
      return
    }

    window.wxOConfiguration = {
      orchestrationID:
        '20260422-2251-1570-00f3-3cdb8b5547d2_20260422-2251-4824-70fa-4985ad60bce7',
      hostURL: 'https://dl.watson-orchestrate.ibm.com',
      rootElementID: 'wxo-chat',
      chatOptions: {
        agentId: 'abe3f124-1559-404e-9fcd-586480f12366',
      },
      onLoad: (instance) => {
        instance.on({
          type: 'authTokenNeeded',
          handler: async (event) => {
            try {
              event.authToken = await fetchAuthToken()
            } catch (err) {
              console.error('[ChatEmbed] authTokenNeeded falhou:', err)
            }
          },
        })
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
