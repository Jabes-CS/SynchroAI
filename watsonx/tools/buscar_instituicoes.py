"""
buscar_instituicoes.py — Tool que busca instituições cadastradas no SynchroAI.

Usada pelo agente Necessidades pra verificar se a instituição já existe
antes de criar uma nova.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="buscar_instituicoes",
    description=(
        "Busca instituições cadastradas no SynchroAI. Pode filtrar por nome "
        "(busca parcial) ou cidade. Retorna lista com id, nome, tipo, cidade "
        "e estado de cada instituição encontrada."
    ),
)
def buscar_instituicoes(
    name: str = "",
    city: str = "",
) -> list:
    """
    Busca instituições cadastradas no SynchroAI.

    Args:
        name: Parte do nome da instituição. Ex: "Defesa Civil".
        city: Cidade. Ex: "Porto Alegre".

    Returns:
        Lista de instituições que correspondem aos filtros.
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/institutions/",
            timeout=60,
        )
        response.raise_for_status()
        all_institutions = response.json()

        result = []
        for inst in all_institutions:
            if not inst.get("is_active", True):
                continue

            if name and name.lower() not in inst.get("name", "").lower():
                continue

            if city and inst.get("city", "").lower() != city.lower():
                continue

            result.append({
                "id": inst["id"],
                "name": inst["name"],
                "email": inst["email"],
                "type": inst["type"],
                "city": inst.get("city"),
                "state": inst.get("state"),
                "is_verified": inst.get("is_verified", False),
            })

        return result

    except requests.RequestException as e:
        return [{"error": f"Erro ao buscar instituicoes: {str(e)}"}]