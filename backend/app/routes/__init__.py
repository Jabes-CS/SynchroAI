"""
routes/__init__.py — Exporta todos os routers.
"""

from app.routes.volunteers import router as volunteers_router
from app.routes.institutions import router as institutions_router
from app.routes.needs import router as needs_router
from app.routes.matches import router as matches_router

__all__ = [
    "volunteers_router",
    "institutions_router",
    "needs_router",
    "matches_router",
]