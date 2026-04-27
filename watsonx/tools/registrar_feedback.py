"""
registrar_feedback.py — Tool que registra feedback de voluntários após missão.

Usada pelo agente Bem-estar para coletar impressões e experiências de voluntários.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="registrar_feedback",
    description=(
        "Registra feedback de um voluntário após participar de uma missão. "
        "Coleta impressões, sugestões e experiência. "
        "Usada pelo agente Bem-estar para melhorar o programa."
    ),
)
def registrar_feedback(
    volunteer_id: int,
    need_id: int,
    texto: str,
    nota_experiencia: float = None,
) -> dict:
    """
    Registra feedback de um voluntário.

    Args:
        volunteer_id: ID do voluntário.
        need_id: ID da necessidade/missão.
        texto: Texto do feedback.
        nota_experiencia: Nota de 1-5 sobre a experiência (opcional).

    Returns:
        Dicionário com confirmação do feedback registrado.
    """
    try:
        payload = {
            "volunteer_id": volunteer_id,
            "need_id": need_id,
            "texto": texto,
        }

        if nota_experiencia is not None:
            payload["nota_experiencia"] = nota_experiencia

        response = requests.post(
            f"{API_BASE_URL}/feedbacks/",
            json=payload,
            timeout=60,
        )

        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "feedback_id": result.get("id"),
            "volunteer_id": volunteer_id,
            "need_id": need_id,
            "message": "Feedback registrado com sucesso! Obrigado pela sua participação.",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao registrar feedback: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
