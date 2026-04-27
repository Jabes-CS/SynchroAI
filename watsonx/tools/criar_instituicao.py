"""
criar_instituicao.py — Tool que cadastra uma nova instituição no SynchroAI.

Usada pelo agente Necessidades quando a instituição informada ainda não existe.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="criar_instituicao",
    description=(
        "Cadastra uma nova instituição no SynchroAI. Recebe nome, email, "
        "telefone, tipo (ngo, government, religious, health, crisis, other), "
        "cidade, estado e endereço. Retorna a instituição criada com ID."
    ),
)
def criar_instituicao(
    name: str,
    email: str,
    type: str = "ngo",
    city: str = "",
    state: str = "",
    address: str = "",
    phone: str = "",
) -> dict:
    """
    Cria uma nova instituição no SynchroAI.

    Args:
        name: Nome da instituição. Ex: "Defesa Civil de Porto Alegre".
        email: Email único de contato.
        type: Tipo. Valores: ngo, government, religious, health, crisis, other.
        city: Cidade. Ex: "Porto Alegre".
        state: Sigla do estado com 2 letras. Ex: "RS".
        address: Endereço completo.
        phone: Telefone de contato.

    Returns:
        Dicionário com os dados da instituição criada, ou erro.
    """
    payload = {
        "name": name,
        "email": email,
        "type": type,
    }

    if city:
        payload["city"] = city
    if state:
        payload["state"] = state
    if address:
        payload["address"] = address
    if phone:
        payload["phone"] = phone

    try:
        response = requests.post(
            f"{API_BASE_URL}/institutions/",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        institution = response.json()

        return {
            "success": True,
            "institution_id": institution["id"],
            "name": institution["name"],
            "email": institution["email"],
            "type": institution["type"],
            "city": institution.get("city", ""),
            "state": institution.get("state", ""),
            "message": (
                f"Instituicao '{institution['name']}' cadastrada com sucesso! "
                f"ID: {institution['id']}. Agora pode cadastrar necessidades."
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
                    f"O email '{email}' ja esta cadastrado. "
                    "Use 'buscar_instituicoes' para encontrar a institucao existente."
                ),
            }

        return {
            "success": False,
            "error": "erro_api",
            "message": f"Erro ao cadastrar instituicao: {detail}",
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": "erro_conexao",
            "message": f"Erro de conexao com a API: {str(e)}",
        }