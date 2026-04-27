"""
criar_alerta.py — Tool que cria alertas/notificações para voluntários.

Usada pelo agente Bem-estar para registrar alertas de emergência/bem-estar.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="criar_alerta",
    description=(
        "Cria um alerta/notificação para um voluntário. "
        "Pode ser alerta de bem-estar, emergência, ou informação importante. "
        "Usada pelo agente Bem-estar para comunicação com voluntários."
    ),
)
def criar_alerta(
    volunteer_id: int,
    mensagem: str,
    tipo: str = "info",
) -> dict:
    """
    Cria um alerta para um voluntário.

    Args:
        volunteer_id: ID do voluntário.
        mensagem: Texto da mensagem/alerta.
        tipo: Tipo de alerta ("info", "warning", "emergency", "wellbeing").

    Returns:
        Dicionário com confirmação do alerta criado.
    """
    try:
        payload = {
            "volunteer_id": volunteer_id,
            "mensagem": mensagem,
            "tipo": tipo.lower(),
        }

        response = requests.post(
            f"{API_BASE_URL}/alertas/",
            json=payload,
            timeout=60,
        )

        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "alert_id": result.get("id"),
            "volunteer_id": volunteer_id,
            "tipo": tipo,
            "message": f"Alerta '{tipo}' registrado para o voluntário.",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao criar alerta: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
