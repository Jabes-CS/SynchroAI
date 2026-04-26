"""
listar_necessidades.py — Tool que lista necessidades abertas.

Usada pelo agente Pareador para identificar onde os voluntários
podem ajudar agora.
"""

import requests
from typing import List, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "http://localhost:8000"


@tool(
    name="listar_necessidades",
    description=(
        "Lista as necessidades abertas no SynchroAI, com filtros opcionais "
        "de cidade e nível de urgência. Retorna título, descrição, skills "
        "necessárias, urgência e quantos voluntários ainda faltam."
    ),
)
def listar_necessidades(
    city: Optional[str] = None,
    urgency: Optional[str] = None,
    only_open: bool = True,
) -> List[dict]:
    """
    Lista necessidades cadastradas pelas instituições.

    Args:
        city: Cidade da necessidade (ex: "Porto Alegre").
        urgency: Nível de urgência. Valores: "low", "medium", "high", "critical".
        only_open: Se True (padrão), retorna apenas necessidades em aberto.

    Returns:
        Lista de necessidades que correspondem aos filtros.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/needs/", timeout=10)
        response.raise_for_status()
        all_needs = response.json()

        result = []
        for n in all_needs:
            # Filtro: somente abertas
            if only_open and n.get("status") != "open":
                continue

            # Filtro: cidade
            if city and n.get("city", "").lower() != city.lower():
                continue

            # Filtro: urgência
            if urgency and n.get("urgency", "").lower() != urgency.lower():
                continue

            result.append({
                "id": n["id"],
                "title": n["title"],
                "description": n["description"],
                "institution_id": n["institution_id"],
                "required_skills": n.get("required_skills", []),
                "volunteers_needed": n.get("volunteers_needed", 1),
                "urgency": n.get("urgency"),
                "status": n.get("status"),
                "city": n.get("city"),
                "state": n.get("state"),
                "address": n.get("address"),
            })

        return result

    except requests.RequestException as e:
        return [{"error": f"Erro ao listar necessidades: {str(e)}"}]