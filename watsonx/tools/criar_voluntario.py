"""
criar_voluntario.py — Tool que cadastra um novo voluntário no SynchroAI.

Usada pelo agente Perfilador após coletar todas as informações
necessárias do voluntário em conversa.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "http://localhost:8000"


@tool(
    name="criar_voluntario",
    description=(
        "Cadastra um novo voluntário no SynchroAI. Recebe nome, email, "
        "telefone, tipo (permanent ou freelancer), habilidades como "
        "string separada por vírgulas, cidade e estado. Retorna o "
        "voluntário criado com ID, ou erro se o email já existir."
    ),
)
def criar_voluntario(
    name: str,
    email: str,
    type: str = "freelancer",
    skills: str = "",
    city: str = "",
    state: str = "",
    phone: str = "",
    availability: str = "",
    open_to_rotation: bool = True,
) -> dict:
    """
    Cria um novo voluntário no SynchroAI.

    Args:
        name: Nome completo do voluntário.
        email: Email único do voluntário.
        type: Tipo de voluntário. Use "permanent" ou "freelancer".
        skills: Habilidades separadas por vírgula. Ex: "enfermagem, primeiros socorros, logística".
        city: Cidade do voluntário. Ex: "Porto Alegre".
        state: Sigla do estado com 2 letras. Ex: "RS".
        phone: Telefone do voluntário. Opcional.
        availability: Disponibilidade em texto livre. Ex: "seg e qua das 8h às 12h".
        open_to_rotation: Se aceita ser revezado em situações de burnout.

    Returns:
        Dicionário com os dados do voluntário criado, incluindo ID, ou erro.
    """
    # Converte skills de string para lista
    skills_list = [s.strip() for s in skills.split(",") if s.strip()] if skills else []

    # Monta dicionário de disponibilidade simples
    availability_dict = {"description": availability} if availability else {}

    payload = {
        "name": name,
        "email": email,
        "type": type,
        "skills": skills_list,
        "availability": availability_dict,
        "open_to_rotation": open_to_rotation,
    }

    if phone:
        payload["phone"] = phone
    if city:
        payload["city"] = city
    if state:
        payload["state"] = state

    try:
        response = requests.post(
            f"{API_BASE_URL}/volunteers/",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        volunteer = response.json()

        return {
            "success": True,
            "volunteer_id": volunteer["id"],
            "name": volunteer["name"],
            "email": volunteer["email"],
            "type": volunteer["type"],
            "city": volunteer.get("city", ""),
            "state": volunteer.get("state", ""),
            "skills": volunteer.get("skills", []),
            "points": volunteer.get("points", 0),
            "message": (
                f"Voluntario {volunteer['name']} cadastrado com sucesso! "
                f"ID: {volunteer['id']}. Ja pode receber convites para acoes."
            ),
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)

        if e.response.status_code == 400:
            return {
                "success": False,
                "error": "email_duplicado",
                "message": (
                    f"O email '{email}' ja esta cadastrado no SynchroAI. "
                    "Use um email diferente."
                ),
            }

        return {
            "success": False,
            "error": "erro_api",
            "message": f"Erro ao cadastrar: {detail}",
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": "erro_conexao",
            "message": f"Erro de conexao com a API: {str(e)}",
        }