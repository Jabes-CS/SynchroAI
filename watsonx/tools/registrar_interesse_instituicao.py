"""
registrar_interesse_instituicao.py — Tool que registra interesse de uma instituição em um voluntário.

Usada pelo agente Necessidades após o colaborador Pareador sugerir voluntários.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="registrar_interesse_instituicao",
    description=(
        "Registra o interesse de uma instituição em um voluntário para uma necessidade. "
        "Após interesse mútuo ser confirmado, a plataforma revela os contatos "
        "entre voluntário e instituição para iniciarem a ação."
    ),
)
def registrar_interesse_instituicao(
    need_id: int,
    volunteer_id: int,
) -> dict:
    """
    Registra interesse de uma instituição em um voluntário.

    Args:
        need_id: ID da necessidade.
        volunteer_id: ID do voluntário.

    Returns:
        Dicionário com status do interesse registrado.
    """
    try:
        payload = {
            "volunteer_id": volunteer_id,
            "need_id": need_id,
            "type": "instituicao_para_voluntario",
        }

        response = requests.post(
            f"{API_BASE_URL}/interesses/",
            json=payload,
            timeout=60,
        )

        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "need_id": need_id,
            "volunteer_id": volunteer_id,
            "interest_registered": True,
            "message": (
                "Seu interesse foi registrado! O voluntário receberá uma notificação. "
                "Se houver interesse mútuo, vocês poderão se contactar em breve."
            ),
            "status": result.get("status", "pending"),
            "mutual_interest": result.get("mutual_interest", False),
            "volunteer_contact": result.get("volunteer_contact"),
            "institution_contact": result.get("institution_contact"),
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
                "error": "Você já registrou interesse neste voluntário para esta necessidade.",
            }

        return {"success": False, "error": f"Erro ao registrar interesse: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
