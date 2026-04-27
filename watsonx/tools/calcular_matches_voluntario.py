"""
calcular_matches_voluntario.py — Tool que calcula matches entre um voluntário e necessidades.

Usada pelo agente Pareador para sugerir necessidades compatíveis com um voluntário.
Calcula score automaticamente baseado em skills, localização e urgência.
"""

import requests
from typing import List
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


def calcular_score(volunteer_skills: List[str], need_skills: List[str], 
                   vol_city: str, need_city: str, vol_state: str, need_state: str,
                   urgency: str) -> float:
    """
    Calcula score de compatibilidade entre voluntário e necessidade.
    
    Critérios:
    - +35: todas as skills (100% match)
    - +25: maioria das skills (>50%)
    - +20: cidade match
    - +10: estado match (sem cidade)
    - +10: urgência CRITICAL/HIGH
    
    Retorna valor 0-100.
    """
    score = 0.0
    
    if not need_skills:
        score = 50.0
    else:
        v_skills_lower = [s.lower() for s in volunteer_skills]
        req_skills_lower = [s.lower() for s in need_skills]
        
        matches = sum(1 for skill in req_skills_lower if skill in v_skills_lower)
        match_pct = matches / len(req_skills_lower)
        
        if match_pct >= 1.0:
            score += 35
        elif match_pct >= 0.5:
            score += 25
        else:
            score += max(0, match_pct * 15)
    
    # Localização
    if vol_city and need_city and vol_city.lower() == need_city.lower():
        score += 20
    elif vol_state and need_state and vol_state.lower() == need_state.lower():
        score += 10
    
    # Urgência
    if urgency and urgency.lower() in ["critical", "high"]:
        score += 10
    
    return min(100.0, max(0.0, score))


@tool(
    name="calcular_matches_voluntario",
    description=(
        "Calcula matches entre um voluntário e necessidades abertas. "
        "Retorna lista de necessidades ordenadas por score de compatibilidade. "
        "Leva em conta skills, localização e urgência. "
        "Usada pelo Pareador quando acionado por um voluntário."
    ),
)
def calcular_matches_voluntario(
    volunteer_id: int,
) -> dict:
    """
    Calcula matches para um voluntário específico.

    Args:
        volunteer_id: ID do voluntário.

    Returns:
        Dicionário com lista de matches ordenados por score.
    """
    try:
        # 1. Busca dados do voluntário
        volunteer_response = requests.get(
            f"{API_BASE_URL}/volunteers/{volunteer_id}",
            timeout=60,
        )
        volunteer_response.raise_for_status()
        volunteer = volunteer_response.json()

        vol_skills = volunteer.get("skills", [])
        vol_city = volunteer.get("city", "")
        vol_state = volunteer.get("state", "")

        # 2. Busca necessidades abertas
        needs_response = requests.get(
            f"{API_BASE_URL}/needs/",
            timeout=60,
        )
        needs_response.raise_for_status()
        all_needs = needs_response.json()

        # 3. Filtra e calcula scores
        matches = []
        for need in all_needs:
            if need.get("status") != "open":
                continue

            need_skills = need.get("required_skills", [])
            need_city = need.get("city", "")
            need_state = need.get("state", "")
            urgency = need.get("urgency", "medium")

            score = calcular_score(
                vol_skills, need_skills,
                vol_city, need_city,
                vol_state, need_state,
                urgency
            )

            matches.append({
                "need_id": need["id"],
                "title": need["title"],
                "description": need["description"],
                "institution_id": need["institution_id"],
                "required_skills": need_skills,
                "volunteers_needed": need.get("volunteers_needed", 1),
                "urgency": urgency,
                "city": need_city,
                "state": need_state,
                "score": round(score, 1),
            })

        # 4. Ordena por score decrescente
        matches.sort(key=lambda x: x["score"], reverse=True)

        return {
            "success": True,
            "volunteer_id": volunteer_id,
            "volunteer_name": volunteer["name"],
            "volunteer_skills": vol_skills,
            "total_matches_found": len(matches),
            "matches": matches,
            "message": f"Encontrei {len(matches)} oportunidades compatíveis para você!",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao calcular matches: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
