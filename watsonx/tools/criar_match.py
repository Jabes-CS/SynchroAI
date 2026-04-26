"""
criar_match.py — Tool que cria um pareamento voluntário ↔ necessidade.

Esta é a "ação principal" do agente Pareador.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="criar_match",
    description=(
        "Cria um pareamento (match) entre um voluntário e uma necessidade. "
        "O score deve ser de 0 a 100, indicando a qualidade do match. "
        "Retorna o match criado ou uma mensagem de erro."
    ),
)
def criar_match(
    volunteer_id: int,
    need_id: int,
    score: float = 75.0,
) -> dict:
    """
    Cria um match entre um voluntário e uma necessidade.

    Args:
        volunteer_id: ID do voluntário.
        need_id: ID da necessidade.
        score: Qualidade do match de 0 a 100 (padrão: 75.0).

    Returns:
        Dicionário com os dados do match criado, ou erro.
    """
    try:
        payload = {
            "volunteer_id": volunteer_id,
            "need_id": need_id,
            "score": score,
        }

        response = requests.post(
            f"{API_BASE_URL}/matches/",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        match = response.json()

        return {
            "success": True,
            "match_id": match["id"],
            "volunteer_id": match["volunteer_id"],
            "need_id": match["need_id"],
            "score": match["score"],
            "status": match["status"],
            "message": f"Match criado com sucesso! ID: {match['id']}, Score: {match['score']}",
        }

    except requests.HTTPError as e:
        # Tenta extrair detalhe do erro da API
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": detail}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}