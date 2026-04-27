"""
__init__.py — Registra todos os modelos.

Este arquivo faz duas coisas importantes:
  1. Importa todos os modelos para que o SQLAlchemy conheça eles
  2. Permite fazer imports limpos: "from app.models import Volunteer"
"""

from app.models.volunteer import Volunteer, VolunteerType
from app.models.institution import Institution, InstitutionType
from app.models.need import Need, NeedStatus, UrgencyLevel
from app.models.match import Match, MatchStatus
from app.models.task_history import TaskHistory
from app.models.reward import Reward, RewardType
from app.models.alert import Alert, AlertType
from app.models.feedback import Feedback
from app.models.interest import Interest, InterestType, InterestStatus

# Exporta tudo — facilita imports em outros arquivos
__all__ = [
    "Volunteer",
    "VolunteerType",
    "Institution",
    "InstitutionType",
    "Need",
    "NeedStatus",
    "UrgencyLevel",
    "Match",
    "MatchStatus",
    "TaskHistory",
    "Reward",
    "RewardType",
    "Alert",
    "AlertType",
    "Feedback",
    "Interest",
    "InterestType",
    "InterestStatus",
]