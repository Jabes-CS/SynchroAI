"""
gerar_matches.py — Tool que gera matches em lote (sistema).

Tool adicional para uso interno do sistema quando novas necessidades/voluntários são criados.
Combina a lógica de pareamento automaticamente sem necessidade de intervenção do agente.
"""

import requests
from typing import List, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


def calcular_score_simples(vol_skills: List[str], need_skills: List[str],
                          vol_city: str, need_city: str,
                          vol_state: str, need_state: str) -> float:
    """Calcula score simples de compatibilidade."""
    score = 0.0
    
    if not need_skills:
        return 50.0
    
    v_skills_lower = [s.lower() for s in vol_skills]
    req_skills_lower = [s.lower() for s in need_skills]
    
    matches = sum(1 for skill in req_skills_lower if skill in v_skills_lower)
    match_pct = matches / len(req_skills_lower)
    
    if match_pct >= 1.0:
        score += 35
    elif match_pct >= 0.5:
        score += 25
    else:
        score += max(0, match_pct * 15)
    
    if vol_city and need_city and vol_city.lower() == need_city.lower():
        score += 20
    elif vol_state and need_state and vol_state.lower() == need_state.lower():
        score += 10
    
    return min(100.0, max(0.0, score))


@tool(
    name="gerar_matches",
    description=(
        "Gera matches em lote entre voluntários e necessidades. "
        "Função auxiliar do sistema para pareamento automático quando novas "
        "necessidades ou voluntários são criados. "
        "Calcula scores e cria matches automaticamente para score >= 60."
    ),
)
def gerar_matches(
    city: Optional[str] = None,
    urgency: Optional[str] = None,
    min_score: float = 60.0,
) -> dict:
    """
    Gera matches em lote entre voluntários e necessidades.

    Args:
        city: Cidade para filtrar (opcional).
        urgency: Urgência mínima - "low", "medium", "high", "critical" (opcional).
        min_score: Score mínimo para criar match (padrão: 60.0).

    Returns:
        Dicionário com estatísticas dos matches criados.
    """
    try:
        # 1. Busca necessidades abertas
        needs_response = requests.get(f"{API_BASE_URL}/needs/", timeout=60)
        needs_response.raise_for_status()
        all_needs = needs_response.json()

        # Filtra necessidades
        filtered_needs = []
        urgency_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        
        for n in all_needs:
            if n.get("status") != "open":
                continue
            if city and n.get("city", "").lower() != city.lower():
                continue
            if urgency and urgency_order.get(n.get("urgency", "low"), 0) < urgency_order.get(urgency.lower(), 0):
                continue
            filtered_needs.append(n)

        # 2. Busca voluntários
        vol_response = requests.get(f"{API_BASE_URL}/volunteers/", timeout=60)
        vol_response.raise_for_status()
        all_volunteers = vol_response.json()

        filtered_volunteers = []
        for v in all_volunteers:
            if not v.get("is_active", True):
                continue
            if city and v.get("city", "").lower() != city.lower():
                continue
            filtered_volunteers.append(v)

        # 3. Gera matches
        matches_created = []
        matches_skipped = []

        for need in filtered_needs:
            need_skills = need.get("required_skills", [])
            volunteers_needed = need.get("volunteers_needed", 1)
            matched_count = 0

            for vol in filtered_volunteers:
                if matched_count >= volunteers_needed:
                    break

                vol_skills = vol.get("skills", [])
                score = calcular_score_simples(
                    vol_skills, need_skills,
                    vol.get("city", ""), need.get("city", ""),
                    vol.get("state", ""), need.get("state", "")
                )

                if score >= min_score:
                    try:
                        match_response = requests.post(
                            f"{API_BASE_URL}/matches/",
                            json={
                                "volunteer_id": vol["id"],
                                "need_id": need["id"],
                                "score": score,
                            },
                            timeout=60,
                        )
                        match_response.raise_for_status()
                        match = match_response.json()

                        matches_created.append({
                            "match_id": match["id"],
                            "volunteer_id": vol["id"],
                            "need_id": need["id"],
                            "score": score,
                        })
                        matched_count += 1

                    except Exception as e:
                        matches_skipped.append({
                            "volunteer_id": vol["id"],
                            "need_id": need["id"],
                            "error": str(e),
                        })
                else:
                    matches_skipped.append({
                        "volunteer_id": vol["id"],
                        "need_id": need["id"],
                        "score": score,
                        "reason": f"Score {score} abaixo do mínimo {min_score}",
                    })

        return {
            "success": True,
            "total_needs": len(filtered_needs),
            "total_volunteers": len(filtered_volunteers),
            "matches_created": len(matches_created),
            "matches_skipped": len(matches_skipped),
            "matches": matches_created,
            "message": f"Lote processado: {len(matches_created)} matches criados.",
        }

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro ao gerar matches: {str(e)}"}
