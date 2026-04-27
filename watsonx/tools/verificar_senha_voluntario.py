"""
verificar_senha_voluntario.py — Tool que verifica a senha de um voluntário.

Usada pelo agente Perfilador para autenticar voluntários existentes.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="verificar_senha_voluntario",
    description=(
        "Verifica se a senha de um voluntário está correta. "
        "Retorna sucesso se autenticado, ou erro se a senha for inválida. "
        "Usada para login de voluntários existentes."
    ),
)
def verificar_senha_voluntario(cpf: str, senha: str) -> dict:
    """
    Verifica a senha de um voluntário.

    Args:
        cpf: CPF do voluntário (formato: "12345678901" ou "123.456.789-01").
        senha: Senha em texto plano (será validada pela API).

    Returns:
        Dicionário com sucesso/falha da autenticação.
    """
    try:
        # Normaliza o CPF removendo pontuação
        cpf_clean = cpf.replace(".", "").replace("-", "").strip()

        payload = {
            "cpf": cpf_clean,
            "password": senha,
        }

        response = requests.post(
            f"{API_BASE_URL}/volunteers/verify-password",
            json=payload,
            timeout=60,
        )

        if response.status_code == 401:
            return {
                "success": False,
                "authenticated": False,
                "message": "Senha incorreta. Tente novamente.",
            }

        if response.status_code == 404:
            return {
                "success": False,
                "authenticated": False,
                "message": "CPF não encontrado no sistema.",
            }

        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "authenticated": True,
            "volunteer_id": result.get("volunteer_id"),
            "name": result.get("name"),
            "message": f"Bem-vindo, {result.get('name')}!",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro na autenticação: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
