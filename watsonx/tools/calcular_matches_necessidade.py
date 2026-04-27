"""
calcular_matches_necessidade.py — Tool que calcula matches entre uma necessidade e voluntários.

Usada pelo agente Pareador para sugerir voluntários compatíveis com uma necessidade.
Calcula score automaticamente e filtra dados sensíveis.
"""

import requests
from typing import List
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


def calcular_score(volunteer_skills: List[str], need_skills: List[str], 
                   vol_city: str, need_city: str, vol_state: str, need_state: str,
                   vol_points: int, vol_type: str) -> float:
    """
    Calcula score de compatibilidade entre voluntário e necessidade.
    
    Critérios:
    - +35: todas as skills (100% match)
    - +25: maioria das skills (>50%)
    - +20: cidade match
    - +10: estado match (sem cidade)
    - +10: voluntário PERMANENT (mais confiável)
    - +5: voluntário com pontuação alta (>50 pontos)
    
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
    
    # Engajamento
    if vol_type and vol_type.lower() == "permanent":
        score += 10
    
    if vol_points and vol_points > 50:
        score += 5
    
    return min(100.0, max(0.0, score))


@tool(
    name="calcular_matches_necessidade",
    description=(
        "Calcula matches entre uma necessidade e voluntários disponíveis. "
        "Retorna lista de voluntários ordenados por score de compatibilidade. "
        "Filtra dados sensíveis — NÃO mostra nome completo, email ou telefone "
        "até confirmação de interesse mútuo. "
        "Usada pelo Pareador quando acionado por uma instituição."
    ),
)
def calcular_matches_necessidade(
    need_id: int,
) -> dict:
    """
    Calcula matches para uma necessidade específica.

    Args:
        need_id: ID da necessidade.

    Returns:
        Dicionário com lista de voluntários ordenados por score.
        Dados sensíveis filtrados (sem contatos).
    """
    try:
        # 1. Busca dados da necessidade
        need_response = requests.get(
            f"{API_BASE_URL}/needs/{need_id}",
            timeout=60,
        )
        need_response.raise_for_status()
        need = need_response.json()

        need_skills = need.get("required_skills", [])
        need_city = need.get("city", "")
        need_state = need.get("state", "")

        # 2. Busca todos os voluntários
        volunteers_response = requests.get(
            f"{API_BASE_URL}/volunteers/",
            timeout=60,
        )
        volunteers_response.raise_for_status()
        all_volunteers = volunteers_response.json()

        # 3. Filtra e calcula scores
        matches = []
        for vol in all_volunteers:
            if not vol.get("is_active", True):
                continue

            vol_skills = vol.get("skills", [])
            vol_city = vol.get("city", "")
            vol_state = vol.get("state", "")
            vol_points = vol.get("points", 0)
            vol_type = vol.get("type", "freelancer")

            score = calcular_score(
                vol_skills, need_skills,
                vol_city, need_city,
                vol_state, need_state,
                vol_points, vol_type
            )

            # Apenas dados não-sensíveis
            matches.append({
                "volunteer_id": vol["id"],
                "skills": vol_skills,
                "age": vol.get("age"),  # Se disponível
                "gender": vol.get("gender"),  # Se disponível
                "points": vol_points,
                "type": vol_type,
                "city": vol_city,
                "state": vol_state,
                "score": round(score, 1),
            })

        # 4. Ordena por score decrescente
        matches.sort(key=lambda x: x["score"], reverse=True)

        return {
            "success": True,
            "need_id": need_id,
            "need_title": need["title"],
            "need_skills": need_skills,
            "need_city": need_city,
            "volunteers_needed": need.get("volunteers_needed", 1),
            "total_matches_found": len(matches),
            "matches": matches,
            "message": (
                f"Encontrei {len(matches)} voluntários compatíveis! "
                "(Dados pessoais ocultos até confirmação de interesse mútuo)"
            ),
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao calcular matches: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
