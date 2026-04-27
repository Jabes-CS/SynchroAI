"""
atualizar_necessidade.py — Tool que atualiza uma necessidade (demanda) existente.

Usada pelo agente Necessidades para permitir edição de necessidades.
"""

import requests
from typing import Optional, List
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="atualizar_necessidade",
    description=(
        "Atualiza dados de uma necessidade existente no SynchroAI. "
        "Pode atualizar título, descrição, skills, urgência, localização, etc. "
        "Recebe apenas os campos que devem ser alterados."
    ),
)
def atualizar_necessidade(
    need_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    required_skills: Optional[List[str]] = None,
    urgency: Optional[str] = None,
    volunteers_needed: Optional[int] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    address: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    """
    Atualiza dados de uma necessidade.

    Args:
        need_id: ID da necessidade.
        title: Novo título (opcional).
        description: Nova descrição (opcional).
        required_skills: Novas skills como lista (opcional).
        urgency: Nova urgência (low, medium, high, critical).
        volunteers_needed: Novo número de voluntários (opcional).
        city: Nova cidade (opcional).
        state: Novo estado (opcional).
        address: Novo endereço (opcional).
        status: Novo status (open, closed, completed, cancelled).

    Returns:
        Dicionário com dados atualizados da necessidade, ou erro.
    """
    try:
        # Monta payload com apenas os campos que foram fornecidos
        payload = {}

        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if required_skills is not None:
            payload["required_skills"] = [s.lower() for s in required_skills]
        if urgency is not None:
            payload["urgency"] = urgency.lower()
        if volunteers_needed is not None:
            payload["volunteers_needed"] = volunteers_needed
        if city is not None:
            payload["city"] = city
        if state is not None:
            payload["state"] = state
        if address is not None:
            payload["address"] = address
        if status is not None:
            payload["status"] = status.lower()

        response = requests.patch(
            f"{API_BASE_URL}/needs/{need_id}",
            json=payload,
            timeout=60,
        )

        if response.status_code == 404:
            return {
                "success": False,
                "message": f"Necessidade com ID {need_id} não encontrada.",
            }

        response.raise_for_status()
        updated_need = response.json()

        return {
            "success": True,
            "need_id": updated_need["id"],
            "title": updated_need["title"],
            "description": updated_need.get("description"),
            "required_skills": updated_need.get("required_skills", []),
            "urgency": updated_need.get("urgency"),
            "volunteers_needed": updated_need.get("volunteers_needed"),
            "city": updated_need.get("city"),
            "state": updated_need.get("state"),
            "status": updated_need.get("status"),
            "message": f"Necessidade '{updated_need['title']}' atualizada com sucesso!",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao atualizar: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
