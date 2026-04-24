"""
main.py — Ponto de entrada da API SynchroAI.

Inicializa o FastAPI, configura CORS, registra as rotas.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    volunteers_router,
    institutions_router,
    needs_router,
    matches_router,
)

# ============================================
# INSTÂNCIA FASTAPI
# ============================================
app = FastAPI(
    title="SynchroAI API",
    description="Orquestrando voluntariado inteligente para situações de crise.",
    version="0.1.0",
)

# ============================================
# CORS (para o frontend React conseguir acessar)
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Frontend Vite em desenvolvimento
        "http://localhost:3000",  # Caso use outra porta
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ROTAS
# ============================================
app.include_router(volunteers_router)
app.include_router(institutions_router)
app.include_router(needs_router)
app.include_router(matches_router)


# ============================================
# HEALTH CHECK
# ============================================
@app.get("/", tags=["Health"])
def root():
    """Endpoint de sanidade — confirma que a API está no ar."""
    return {
        "status": "online",
        "project": "SynchroAI",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Verificação de saúde da API."""
    return {"status": "healthy"}