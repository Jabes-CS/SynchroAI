"""
schemas/__init__.py — Exporta todos os schemas.
"""

from app.schemas.volunteer import (
    VolunteerBase,
    VolunteerCreate,
    VolunteerUpdate,
    VolunteerRead,
)
from app.schemas.institution import (
    InstitutionBase,
    InstitutionCreate,
    InstitutionUpdate,
    InstitutionRead,
)
from app.schemas.need import (
    NeedBase,
    NeedCreate,
    NeedUpdate,
    NeedRead,
)
from app.schemas.match import (
    MatchBase,
    MatchCreate,
    MatchUpdate,
    MatchRead,
)

__all__ = [
    "VolunteerBase", "VolunteerCreate", "VolunteerUpdate", "VolunteerRead",
    "InstitutionBase", "InstitutionCreate", "InstitutionUpdate", "InstitutionRead",
    "NeedBase", "NeedCreate", "NeedUpdate", "NeedRead",
    "MatchBase", "MatchCreate", "MatchUpdate", "MatchRead",
]