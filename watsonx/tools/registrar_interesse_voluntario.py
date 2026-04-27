"""
registrar_interesse_voluntario.py — Tool que registra interesse de um voluntário em uma necessidade.

Usada pelo agente Perfilador após o colaborador Pareador sugerir matches.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="registrar_interesse_voluntario",
    description=(
        "Registra o interesse de um voluntário em uma necessidade específica. "
        "Após interesse mútuo ser confirmado, a plataforma revela os contatos "
        "entre voluntário e instituição para iniciarem a ação."
    ),
)
def registrar_interesse_voluntario(
    volunteer_id: int,
    need_id: int,
) -> dict:
    """
    Registra interesse de um voluntário em uma necessidade.

    Args:
        volunteer_id: ID do voluntário.
        need_id: ID da necessidade.

    Returns:
        Dicionário com status do interesse registrado.
    """
    try:
        payload = {
            "volunteer_id": volunteer_id,
            "need_id": need_id,
        }

        response = requests.post(
            f"{API_BASE_URL}/volunteers/register-interest",
            json=payload,
            timeout=60,
        )

        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "volunteer_id": volunteer_id,
            "need_id": need_id,
            "interest_registered": True,
            "message": (
                "Seu interesse foi registrado! A instituição receberá uma notificação. "
                "Se houver interesse mútuo, vocês poderão se contactar em breve."
            ),
            "status": result.get("status", "pending"),
            "mutual_interest": result.get("mutual_interest", False),
            "institution_contact": result.get("institution_contact"),
            "volunteer_contact": result.get("volunteer_contact"),
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)

        # Trata alguns erros específicos
        if "already" in detail.lower():
            return {
                "success": False,
                "error": "Você já registrou interesse nesta necessidade.",
            }

        return {"success": False, "error": f"Erro ao registrar interesse: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
