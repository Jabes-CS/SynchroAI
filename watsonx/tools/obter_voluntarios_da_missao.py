"""
obter_voluntarios_da_missao.py — Tool que obtém voluntários que atuaram em uma necessidade.

Usada pelo agente Pontuação para listar voluntários que devem ser avaliados.
"""

import requests
from typing import List
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="obter_voluntarios_da_missao",
    description=(
        "Obtém lista de voluntários que atuaram em uma necessidade específica. "
        "Retorna dados básicos (ID, nome, email) para avaliação de pontuação. "
        "Usada pelo agente Pontuação após conclusão de uma missão."
    ),
)
def obter_voluntarios_da_missao(need_id: int) -> dict:
    """
    Obtém voluntários que atuaram em uma necessidade.

    Args:
        need_id: ID da necessidade.

    Returns:
        Dicionário com lista de voluntários da missão.
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/needs/{need_id}/volunteers",
            timeout=60,
        )

        if response.status_code == 404:
            return {
                "success": False,
                "message": f"Necessidade {need_id} não encontrada.",
            }

        response.raise_for_status()
        result = response.json()

        volunteers = result.get("volunteers", [])

        return {
            "success": True,
            "need_id": need_id,
            "need_title": result.get("need_title"),
            "total_volunteers": len(volunteers),
            "volunteers": [
                {
                    "volunteer_id": v["id"],
                    "name": v["name"],
                    "email": v["email"],
                    "skills": v.get("skills", []),
                }
                for v in volunteers
            ],
            "message": f"Encontrei {len(volunteers)} voluntário(s) para avaliar.",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao obter voluntários: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
