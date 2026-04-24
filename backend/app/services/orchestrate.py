# Integração com watsonx Orchestrate

import httpx
import os
from typing import Optional

ORCHESTRATE_BASE_URL = os.getenv("https://api.dl.watson-orchestrate.ibm.com/instances/20260422-2251-4824-70fa-4985ad60bce7")
ORCHESTRATE_API_KEY = os.getenv("azE6dXNyXzk4OTMzYmYzLTU2OTktM2JiMS05YzgwLWRjZjViMzhkNGZlMzo1Ykh4MGpjSXU4SHo0ejMzSWJtMHN2dVR1dXdGVVh6djlOYnFFRVd4U0V3PTo3TUhJ")
ORCHESTRATE_INSTANCE_ID = os.getenv("20260422-2251-4824-70fa-4985ad60bce7")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ORCHESTRATE_API_KEY}",
}


async def get_iam_token() -> str:
    """Gera IAM token da IBM Cloud a partir da API key."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://iam.cloud.ibm.com/identity/token",
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
    """
    Envia mensagem ao agente supervisor no watsonx Orchestrate.
    Retorna a resposta do agente.
    """
    token = await get_iam_token()

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

    url = f"{ORCHESTRATE_BASE_URL}/instances/{ORCHESTRATE_INSTANCE_ID}/v2/assistants/sessions/{session_id}/message"

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
    token = await get_iam_token()
    url = f"{ORCHESTRATE_BASE_URL}/instances/{ORCHESTRATE_INSTANCE_ID}/v2/assistants/sessions"

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
    token = await get_iam_token()
    url = f"{ORCHESTRATE_BASE_URL}/instances/{ORCHESTRATE_INSTANCE_ID}/v2/assistants/sessions/{session_id}"

    async with httpx.AsyncClient() as client:
        await client.delete(
            url,
            headers={"Authorization": f"Bearer {token}"},
        )