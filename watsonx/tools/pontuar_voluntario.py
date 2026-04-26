"""
pontuar_voluntario.py — Tool que adiciona pontos a um voluntário.

Usada pelo agente Pontuação para gamificar a participação.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="pontuar_voluntario",
    description=(
        "Adiciona pontos a um voluntário pelo trabalho realizado. "
        "Os pontos podem ser usados para resgatar bônus de bem-estar e lazer. "
        "Retorna o novo total de pontos do voluntário."
    ),
)
def pontuar_voluntario(
    volunteer_id: int,
    points: int,
    reason: str = "Atividade concluída",
) -> dict:
    """
    Adiciona pontos a um voluntário.

    Args:
        volunteer_id: ID do voluntário.
        points: Quantidade de pontos a adicionar (positivo).
        reason: Motivo da pontuação (para histórico).

    Returns:
        Dicionário com o total de pontos atualizado, ou erro.
    """
    try:
        # 1. Busca o voluntário pra pegar pontos atuais
        response = requests.get(
            f"{API_BASE_URL}/volunteers/{volunteer_id}",
            timeout=10,
        )
        response.raise_for_status()
        volunteer = response.json()

        current_points = volunteer.get("points", 0)
        new_points = current_points + points

        return {
            "success": True,
            "volunteer_id": volunteer_id,
            "volunteer_name": volunteer["name"],
            "previous_points": current_points,
            "added_points": points,
            "new_total": new_points,
            "reason": reason,
            "message": (
                f"{volunteer['name']} ganhou {points} pontos por '{reason}'. "
                f"Total agora: {new_points} pontos."
            ),
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": detail}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}