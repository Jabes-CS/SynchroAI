"""
buscar_voluntarios.py — Tool que busca voluntários compatíveis com critérios.

Esta tool é usada principalmente pelo agente Pareador para encontrar
candidatos a uma necessidade específica.
"""

import requests
from typing import List, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool


# URL base da nossa API FastAPI
API_BASE_URL = "http://localhost:8000"


@tool(
    name="buscar_voluntarios",
    description=(
        "Busca voluntários cadastrados no SynchroAI, com filtros opcionais "
        "de habilidades e cidade. Retorna lista de voluntários compatíveis "
        "com nome, email, skills, cidade e pontos."
    ),
)
def buscar_voluntarios(
    skills: Optional[List[str]] = None,
    city: Optional[str] = None,
    only_active: bool = True,
) -> List[dict]:
    """
    Busca voluntários cadastrados no SynchroAI.

    Args:
        skills: Lista de habilidades necessárias (ex: ["enfermagem"]).
                Retorna voluntários que tenham PELO MENOS UMA das skills.
        city: Nome da cidade (ex: "Porto Alegre").
        only_active: Se True (padrão), retorna apenas voluntários ativos.

    Returns:
        Lista de dicionários com dados dos voluntários encontrados.
    """
    try:
        # Faz a chamada à API FastAPI
        response = requests.get(f"{API_BASE_URL}/volunteers/", timeout=10)
        response.raise_for_status()
        all_volunteers = response.json()

        # Filtra os resultados conforme os critérios
        result = []
        for v in all_volunteers:
            # Filtro: somente ativos
            if only_active and not v.get("is_active", True):
                continue

            # Filtro: cidade
            if city and v.get("city", "").lower() != city.lower():
                continue

            # Filtro: skills (pelo menos uma habilidade em comum)
            if skills:
                v_skills = [s.lower() for s in v.get("skills", [])]
                requested = [s.lower() for s in skills]
                if not any(s in v_skills for s in requested):
                    continue

            # Adiciona ao resultado em formato simplificado
            result.append({
                "id": v["id"],
                "name": v["name"],
                "email": v["email"],
                "type": v["type"],
                "skills": v.get("skills", []),
                "city": v.get("city"),
                "state": v.get("state"),
                "points": v.get("points", 0),
            })

        return result

    except requests.RequestException as e:
        return [{"error": f"Erro ao buscar voluntários: {str(e)}"}]