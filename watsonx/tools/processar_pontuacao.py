"""
processar_pontuacao.py — Tool que processa pontuação de voluntários após conclusão de missão.

Usada pelo agente Pontuação para calcular pontos, bônus e atribuir badges.
"""

import requests
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="processar_pontuacao",
    description=(
        "Processa pontuação de voluntários após conclusão de uma necessidade. "
        "Calcula pontos base, bônus por rapidez/horas, nota da instituição e badges. "
        "Retorna pontuação atualizada de cada voluntário."
    ),
)
def processar_pontuacao(
    need_id: int,
    avaliacoes: List[Dict[str, Any]],
) -> dict:
    """
    Processa pontuação e calcula recompensas.

    Args:
        need_id: ID da necessidade concluída.
        avaliacoes: Lista de dicionários com:
            - volunteer_id: int
            - nota: float (1-5, nota da instituição)
            - feedback: str (comentário textual)
            - horas_trabalhadas: float (opcional)

    Returns:
        Dicionário com pontuação processada e recompensas.
    """
    try:
        # Valida avaliacoes
        if not avaliacoes:
            return {
                "success": False,
                "error": "Nenhuma avaliação foi fornecida.",
            }

        payload = {
            "need_id": need_id,
            "avaliacoes": avaliacoes,
        }

        response = requests.post(
            f"{API_BASE_URL}/rewards/processar",
            json=payload,
            timeout=60,
        )

        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "need_id": need_id,
            "processado": result.get("processado", True),
            "total_voluntarios_avaliados": len(avaliacoes),
            "recompensas": result.get("recompensas", []),
            "badges_atribuidos": result.get("badges", []),
            "message": (
                f"Pontuação processada! {len(result.get('recompensas', []))} voluntário(s) recebeu recompensas."
            ),
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao processar pontuação: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
