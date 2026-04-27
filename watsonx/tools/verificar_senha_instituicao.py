"""
verificar_senha_instituicao.py — Tool que verifica a senha de uma instituição.

Usada pelo agente Necessidades para autenticar instituições existentes.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="verificar_senha_instituicao",
    description=(
        "Verifica se a senha de uma instituição está correta. "
        "Retorna sucesso se autenticada, ou erro se a senha for inválida. "
        "Usada para login de instituições existentes."
    ),
)
def verificar_senha_instituicao(cnpj: str, senha: str) -> dict:
    """
    Verifica a senha de uma instituição.

    Args:
        cnpj: CNPJ da instituição (formato: "12345678000190" ou "12.345.678/0001-90").
        senha: Senha em texto plano (será validada pela API).

    Returns:
        Dicionário com sucesso/falha da autenticação.
    """
    try:
        # Normaliza o CNPJ removendo pontuação
        cnpj_clean = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()

        payload = {
            "cnpj": cnpj_clean,
            "password": senha,
        }

        response = requests.post(
            f"{API_BASE_URL}/institutions/verify-password",
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
                "message": "CNPJ não encontrado no sistema.",
            }

        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "authenticated": True,
            "institution_id": result.get("institution_id"),
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
