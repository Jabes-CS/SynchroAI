"""
atualizar_voluntario.py — Tool que atualiza dados de um voluntário cadastrado.

Usada pelo agente Perfilador para permitir que voluntários atualizem suas informações.
"""

import requests
from typing import List, Optional, Dict
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="atualizar_voluntario",
    description=(
        "Atualiza dados de um voluntário existente no SynchroAI. "
        "Pode atualizar email, telefone, cidade, habilidades, disponibilidade, etc. "
        "Recebe apenas os campos que devem ser alterados."
    ),
)
def atualizar_voluntario(
    volunteer_id: int,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    skills: Optional[List[str]] = None,
    availability: Optional[Dict[str, str]] = None,
    type: Optional[str] = None,
) -> dict:
    """
    Atualiza dados de um voluntário.

    Args:
        volunteer_id: ID do voluntário.
        email: Novo email (opcional).
        phone: Novo telefone (opcional).
        city: Nova cidade (opcional).
        state: Novo estado/sigla (opcional).
        skills: Novas habilidades como lista (opcional).
        availability: Disponibilidade como dicionário dia:horário (opcional).
        type: Tipo do voluntário: "permanent" ou "freelancer" (opcional).

    Returns:
        Dicionário com dados atualizados do voluntário, ou erro.
    """
    try:
        # Monta payload com apenas os campos que foram fornecidos
        payload = {}

        if email is not None:
            payload["email"] = email
        if phone is not None:
            payload["phone"] = phone
        if city is not None:
            payload["city"] = city
        if state is not None:
            payload["state"] = state
        if skills is not None:
            payload["skills"] = [s.lower() for s in skills]
        if availability is not None:
            payload["availability"] = availability
        if type is not None:
            payload["type"] = type.lower()

        response = requests.patch(
            f"{API_BASE_URL}/volunteers/{volunteer_id}",
            json=payload,
            timeout=60,
        )

        if response.status_code == 404:
            return {
                "success": False,
                "message": f"Voluntário com ID {volunteer_id} não encontrado.",
            }

        response.raise_for_status()
        updated_volunteer = response.json()

        return {
            "success": True,
            "volunteer_id": updated_volunteer["id"],
            "name": updated_volunteer["name"],
            "email": updated_volunteer.get("email"),
            "phone": updated_volunteer.get("phone"),
            "city": updated_volunteer.get("city"),
            "state": updated_volunteer.get("state"),
            "skills": updated_volunteer.get("skills", []),
            "type": updated_volunteer.get("type"),
            "availability": updated_volunteer.get("availability"),
            "message": f"Perfil de {updated_volunteer['name']} atualizado com sucesso!",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao atualizar: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
