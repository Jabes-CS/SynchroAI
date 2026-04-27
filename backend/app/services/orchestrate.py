# Integração com watsonx Orchestrate

import os
from typing import Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

ORCHESTRATE_BASE_URL = os.getenv("WO_DEVELOPER_EDITION_SOURCE")
ORCHESTRATE_API_KEY = os.getenv("WO_API_KEY")
ORCHESTRATE_INSTANCE_ID = os.getenv("WO_INSTANCE")
WO_AUTH_TYPE = os.getenv("WO_AUTH_TYPE", "mcsp").lower()

MCSP_TOKEN_URL = "https://iam.platform.saas.ibm.com/siusermgr/api/1.0/apikeys/token"
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"


async def get_orchestrate_token() -> str:
    """
    Gera um JWT válido para o watsonx Orchestrate.
    - mcsp  → IBM Cloud SaaS (Developer Edition)
    - iam   → IBM Cloud clássico (CPD / on-prem)
    """
    if not ORCHESTRATE_API_KEY:
        raise RuntimeError("WO_API_KEY não configurada no .env")

    async with httpx.AsyncClient(timeout=15.0) as client:
        if WO_AUTH_TYPE == "mcsp":
            response = await client.post(
                MCSP_TOKEN_URL,
                headers={"Content-Type": "application/json"},
                json={"apikey": ORCHESTRATE_API_KEY},
            )
            response.raise_for_status()
            return response.json()["token"]

        response = await client.post(
            IAM_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": ORCHESTRATE_API_KEY,
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]


async def send_message_to_agent(
    session_id: str,
    message: str,
    agent_name: str = "SynchroAI_Orquestrador",
    volunteer_id: Optional[str] = None,
) -> dict:
    """Envia mensagem ao agente supervisor no watsonx Orchestrate."""
    token = await get_orchestrate_token()

    payload = {
        "input": {
            "text": message,
            "session_id": session_id,
        },
        "context": {
            "skills": {
                "main skill": {
                    "user_defined": {
                        "volunteer_id": volunteer_id,
                    }
                }
            }
        },
    }

    url = f"{ORCHESTRATE_BASE_URL}/v2/assistants/sessions/{session_id}/message"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def create_session() -> str:
    """Cria uma nova sessão de conversa no watsonx Orchestrate."""
    token = await get_orchestrate_token()
    url = f"{ORCHESTRATE_BASE_URL}/v2/assistants/sessions"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json={},
        )
        response.raise_for_status()
        return response.json()["session_id"]


async def delete_session(session_id: str) -> None:
    """Encerra uma sessão de conversa."""
    token = await get_orchestrate_token()
    url = f"{ORCHESTRATE_BASE_URL}/v2/assistants/sessions/{session_id}"

    async with httpx.AsyncClient() as client:
        await client.delete(
            url,
            headers={"Authorization": f"Bearer {token}"},
        )
