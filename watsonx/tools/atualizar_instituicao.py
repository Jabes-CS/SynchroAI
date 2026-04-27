"""
atualizar_instituicao.py — Tool que atualiza dados de uma instituição cadastrada.

Usada pelo agente Necessidades para permitir que instituições atualizem suas informações.
"""

import requests
from typing import Optional, List
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="atualizar_instituicao",
    description=(
        "Atualiza dados de uma instituição existente no SynchroAI. "
        "Pode atualizar email, telefone, cidade, tipo, endereço, etc. "
        "Recebe apenas os campos que devem ser alterados."
    ),
)
def atualizar_instituicao(
    institution_id: int,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    address: Optional[str] = None,
    type: Optional[str] = None,
    website: Optional[str] = None,
) -> dict:
    """
    Atualiza dados de uma instituição.

    Args:
        institution_id: ID da instituição.
        email: Novo email (opcional).
        phone: Novo telefone (opcional).
        city: Nova cidade (opcional).
        state: Novo estado/sigla (opcional).
        address: Novo endereço (opcional).
        type: Novo tipo (ngo, government, religious, health, crisis, other).
        website: Novo website (opcional).

    Returns:
        Dicionário com dados atualizados da instituição, ou erro.
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
        if address is not None:
            payload["address"] = address
        if type is not None:
            payload["type"] = type.lower()
        if website is not None:
            payload["website"] = website

        response = requests.patch(
            f"{API_BASE_URL}/institutions/{institution_id}",
            json=payload,
            timeout=60,
        )

        if response.status_code == 404:
            return {
                "success": False,
                "message": f"Instituição com ID {institution_id} não encontrada.",
            }

        response.raise_for_status()
        updated_institution = response.json()

        return {
            "success": True,
            "institution_id": updated_institution["id"],
            "name": updated_institution["name"],
            "email": updated_institution.get("email"),
            "phone": updated_institution.get("phone"),
            "city": updated_institution.get("city"),
            "state": updated_institution.get("state"),
            "address": updated_institution.get("address"),
            "type": updated_institution.get("type"),
            "website": updated_institution.get("website"),
            "message": f"Dados de {updated_institution['name']} atualizados com sucesso!",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao atualizar: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
