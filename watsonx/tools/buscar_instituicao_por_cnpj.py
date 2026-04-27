"""
buscar_instituicao_por_cnpj.py — Tool que busca uma instituição pelo CNPJ.

Usada pelo agente Necessidades para verificar se uma instituição já está cadastrada.
"""

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


API_BASE_URL = "https://synchroai-api.onrender.com"


@tool(
    name="buscar_instituicao_por_cnpj",
    description=(
        "Busca uma instituição cadastrada no SynchroAI pelo CNPJ. "
        "Retorna os dados da instituição se encontrada, ou uma mensagem se não existe. "
        "Útil para verificar se um CNPJ já está registrado antes de cadastrar."
    ),
)
def buscar_instituicao_por_cnpj(cnpj: str) -> dict:
    """
    Busca uma instituição pelo CNPJ.

    Args:
        cnpj: CNPJ da instituição (formato: "12345678000190" ou "12.345.678/0001-90").

    Returns:
        Dicionário com dados da instituição se encontrada, ou mensagem de não encontrado.
    """
    try:
        # Normaliza o CNPJ removendo pontuação
        cnpj_clean = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()

        # Busca a instituição pelo CNPJ
        response = requests.get(
            f"{API_BASE_URL}/institutions/cnpj/{cnpj_clean}",
            timeout=60,
        )

        if response.status_code == 404:
            return {
                "success": False,
                "found": False,
                "message": f"CNPJ {cnpj} não encontrado no sistema.",
            }

        response.raise_for_status()
        institution = response.json()

        return {
            "success": True,
            "found": True,
            "institution_id": institution["id"],
            "name": institution["name"],
            "email": institution["email"],
            "phone": institution.get("phone"),
            "type": institution.get("type"),
            "city": institution.get("city"),
            "state": institution.get("state"),
            "is_active": institution.get("is_active", True),
            "message": f"Instituição encontrada: {institution['name']}",
        }

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return {"success": False, "error": f"Erro ao buscar CNPJ: {detail}"}

    except requests.RequestException as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
