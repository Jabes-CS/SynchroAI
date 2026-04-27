"""
listar_necessidades_ativas.py — Tool que lista necessidades ativas de uma instituição.

Usada pelo agente Necessidades para exibir necessidades que a instituição pode editar ou gerenciar.
"""

import requests
from typing import Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="listar_necessidades_ativas",
    description=(
        "Lista as necessidades ativas de uma instituição específica. "
        "Retorna apenas necessidades em status 'open' ou 'active'. "
        "Útil para gerenciamento e edição de necessidades."
    ),
)
def listar_necessidades_ativas(
    institution_id: int,
    include_closed: bool = False,
) -> dict:
    """
    Lista necessidades ativas de uma instituição.

    Args:
        institution_id: ID da instituição.
        include_closed: Se True, inclui necessidades fechadas/concluídas.

    Returns:
        Dicionário com lista de necessidades da instituição.
    """
    try:
        # Busca todas as necessidades
        response = requests.get(
            f"{API_BASE_URL}/needs/",
            timeout=60,
        )
        response.raise_for_status()
        all_needs = response.json()

        # Filtra por instituição e status
        filtered_needs = []
        for need in all_needs:
            if need.get("institution_id") != institution_id:
                continue

            status = need.get("status", "open")
            
            # Se include_closed é False, ignora needs fechadas
            if not include_closed and status not in ["open", "active"]:
                continue

            filtered_needs.append({
                "need_id": need["id"],
                "title": need["title"],
                "description": need.get("description"),
                "required_skills": need.get("required_skills", []),
                "volunteers_needed": need.get("volunteers_needed", 1),
                "urgency": need.get("urgency"),
                "status": status,
                "city": need.get("city"),
                "state": need.get("state"),
                "created_at": need.get("created_at"),
            })

        # Ordena por urgência e data
        urgency_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        filtered_needs.sort(
            key=lambda x: (urgency_order.get(x.get("urgency", "low"), 4)),
        )

        return {
            "success": True,
            "institution_id": institution_id,
            "total_needs": len(filtered_needs),
            "needs": filtered_needs,
            "message": f"Total de {len(filtered_needs)} necessidade(s) encontrada(s).",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao listar necessidades: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
