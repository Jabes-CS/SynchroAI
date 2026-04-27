"""
buscar_voluntario_por_cpf.py — Tool que busca um voluntário pelo CPF.

Usada pelo agente Perfilador para verificar se um CPF já está cadastrado.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="buscar_voluntario_por_cpf",
    description=(
        "Busca um voluntário cadastrado no SynchroAI pelo CPF. "
        "Retorna os dados do voluntário se encontrado, ou uma mensagem se não existe. "
        "Útil para verificar se um CPF já está registrado antes de cadastrar."
    ),
)
def buscar_voluntario_por_cpf(cpf: str) -> dict:
    """
    Busca um voluntário pelo CPF.

    Args:
        cpf: CPF do voluntário (formato: "12345678901" ou "123.456.789-01").

    Returns:
        Dicionário com dados do voluntário se encontrado, ou mensagem de não encontrado.
    """
    try:
        # Normaliza o CPF removendo pontuação
        cpf_clean = cpf.replace(".", "").replace("-", "").strip()

        # Busca o voluntário pelo CPF
        response = requests.get(
            f"{API_BASE_URL}/volunteers/cpf/{cpf_clean}",
            timeout=60,
        )

        if response.status_code == 404:
            return {
                "success": False,
                "found": False,
                "message": f"CPF {cpf} não encontrado no sistema.",
            }

        response.raise_for_status()
        volunteer = response.json()

        return {
            "success": True,
            "found": True,
            "volunteer_id": volunteer["id"],
            "name": volunteer["name"],
            "email": volunteer["email"],
            "type": volunteer.get("type"),
            "city": volunteer.get("city"),
            "state": volunteer.get("state"),
            "skills": volunteer.get("skills", []),
            "points": volunteer.get("points", 0),
            "is_active": volunteer.get("is_active", True),
            "message": f"Voluntário encontrado: {volunteer['name']}",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao buscar CPF: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
