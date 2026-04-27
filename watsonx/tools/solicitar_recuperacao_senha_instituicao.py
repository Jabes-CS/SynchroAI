"""
solicitar_recuperacao_senha_instituicao.py — Tool para solicitar recuperação de senha de instituição.

Usada pelo agente Necessidades quando uma instituição esquece a senha.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="solicitar_recuperacao_senha_instituicao",
    description=(
        "Solicita recuperação de senha para uma instituição. "
        "Envia um email de recuperação com instruções. "
        "Usada quando a instituição esqueceu ou precisa resetar a senha."
    ),
)
def solicitar_recuperacao_senha_instituicao(email: str) -> dict:
    """
    Solicita recuperação de senha via email.

    Args:
        email: Email da instituição para receber link de recuperação.

    Returns:
        Dicionário com status da solicitação.
    """
    try:
        payload = {
            "email": email,
        }

        response = requests.post(
            f"{API_BASE_URL}/institutions/request-password-reset",
            json=payload,
            timeout=60,
        )

        if response.status_code == 404:
            return {
                "success": False,
                "message": f"Email {email} não encontrado no sistema.",
            }

        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "message": (
                f"Email de recuperação enviado para {email}. "
                "Verifique a caixa de entrada (e spam) nos próximos minutos. "
                "O link expira em 24 horas."
            ),
            "email_sent": result.get("email_sent", True),
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao solicitar recuperação: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
