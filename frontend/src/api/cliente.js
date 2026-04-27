import axios from 'axios'


// Em produção, lê da variável VITE_API_URL.
// Em desenvolvimento, usa localhost.

const API_URL = import.meta.env.VITE_API_URL || 'https://synchroai-api.onrender.com';

export async function getProfile() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/profile`);
    if (!response.ok) {
      throw new Error(`Erro ${response.status}: ${await response.text()}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Falha ao buscar perfil:', error);
    throw error;
  }
}


const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[API Error]', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export default api