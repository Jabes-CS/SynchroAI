"""
main.py — Ponto de entrada da API SynchroAI.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

from app.routes import (
    volunteers_router,
    institutions_router,
    needs_router,
    matches_router,
    alertas_router,
    feedbacks_router,
    interesses_router,
    chat_router,
)
from app.services.orchestrate import get_orchestrate_token, ORCHESTRATE_BASE_URL

app = FastAPI(
    title="SynchroAI API",
    description="Orquestrando voluntariado inteligente para situações de crise.",
    version="0.1.0",
)



WATSONX_API_KEY = os.getenv("WATSONX_API_KEY") or os.getenv("WO_API_KEY")

# CORS — em produção, libera todos os origins (vamos restringir depois)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    # Em produção, permite todas as origens (pra ngrok, vercel, IBM, etc)
    allow_origins = ["*"]
else:
    # Em dev, só localhost
    allow_origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=False,  # False quando allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(volunteers_router)
app.include_router(institutions_router)
app.include_router(needs_router)
app.include_router(matches_router)
app.include_router(alertas_router)
app.include_router(feedbacks_router)
app.include_router(interesses_router)
app.include_router(chat_router)




@app.get("/api/profile")
async def get_profile():
    token = await get_orchestrate_token()
    url = f"{ORCHESTRATE_BASE_URL}/mfe_home_archer/api/v1/profiles/me"
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "project": "SynchroAI",
        "version": "0.1.0",
        "environment": ENVIRONMENT,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}