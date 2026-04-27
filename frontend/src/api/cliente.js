/**
 * client.js — Cliente axios centralizado para falar com a API SynchroAI.
 *
 * Quando fizermos deploy, vamos só trocar a baseURL aqui pelo URL público
 * (ex: synchroai-api.onrender.com) e tudo continua funcionando.
 */

import axios from 'axios'

// Em desenvolvimento usa localhost. Em produção, ler de variável de ambiente.
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor — loga erros no console pra debug
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[API Error]', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export default api