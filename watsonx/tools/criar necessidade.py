"""
criar_necessidade.py — Tool que cadastra uma nova necessidade no SynchroAI.

Usada pelo agente Necessidades pra registrar demandas de uma instituição.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="criar_necessidade",
    description=(
        "Cadastra uma nova necessidade (demanda de voluntários) no SynchroAI. "
        "Vinculada a uma instituição existente. Recebe título, descrição, "
        "skills necessárias, urgência (low, medium, high, critical), "
        "quantidade de voluntários e localização. Retorna a necessidade "
        "criada com ID."
    ),
)
def criar_necessidade(
    title: str,
    description: str,
    institution_id: int,
    required_skills: str = "",
    volunteers_needed: int = 1,
    urgency: str = "medium",
    city: str = "",
    state: str = "",
    address: str = "",
) -> dict:
    """
    Cria uma nova necessidade no SynchroAI.

    Args:
        title: Título curto da necessidade. Ex: "Enfermeiros para abrigo".
        description: Descrição detalhada (mínimo 10 caracteres).
        institution_id: ID da instituição que criou a necessidade.
        required_skills: Skills necessárias separadas por vírgula. Ex: "enfermagem, primeiros socorros".
        volunteers_needed: Quantos voluntários são necessários (mínimo 1).
        urgency: Nível. Valores: "low", "medium", "high", "critical".
        city: Cidade onde a ajuda é necessária.
        state: Sigla do estado com 2 letras. Ex: "RS".
        address: Endereço completo da ação.

    Returns:
        Dicionário com os dados da necessidade criada, ou erro.
    """
    skills_list = [s.strip() for s in required_skills.split(",") if s.strip()] if required_skills else []

    payload = {
        "title": title,
        "description": description,
        "institution_id": institution_id,
        "required_skills": skills_list,
        "volunteers_needed": volunteers_needed,
        "urgency": urgency,
    }

    if city:
        payload["city"] = city
    if state:
        payload["state"] = state
    if address:
        payload["address"] = address

    try:
        response = requests.post(
            f"{API_BASE_URL}/needs/",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        need = response.json()

        return {
            "success": True,
            "need_id": need["id"],
            "title": need["title"],
            "institution_id": need["institution_id"],
            "urgency": need["urgency"],
            "volunteers_needed": need["volunteers_needed"],
            "required_skills": need.get("required_skills", []),
            "city": need.get("city", ""),
            "state": need.get("state", ""),
            "status": need["status"],
            "message": (
                f"Necessidade '{need['title']}' cadastrada com sucesso! "
                f"ID: {need['id']}. Urgencia: {need['urgency']}. "
                f"Buscando {need['volunteers_needed']} voluntario(s)."
            ),
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)

        if e.response.status_code == 404:
            return {
                "success": False,
                "error": "instituicao_nao_encontrada",
                "message": (
                    f"Instituicao com ID {institution_id} nao encontrada. "
                    "Use 'buscar_instituicoes' ou 'criar_instituicao' antes."
                ),
            }

        return {
            "success": False,
            "error": "erro_api",
            "message": f"Erro ao cadastrar necessidade: {detail}",
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": "erro_conexao",
            "message": f"Erro de conexao com a API: {str(e)}",
        }