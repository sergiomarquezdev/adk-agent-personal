"""
Módulo de herramientas para manejo de CV.
"""

from .cache import get_cv_data
from .extractors import (
    get_certificates,
    get_education,
    get_personal_info,
    get_projects,
    get_skills,
    get_work_experience,
)

# Las funciones que se expondrán como herramientas para el agente
cv_tools = [
    get_personal_info,
    get_work_experience,
    get_education,
    get_skills,
    get_projects,
    get_certificates,
]

__all__ = [
    "get_cv_data",  # Se mantiene por si es usado internamente en otros sitios
    "cv_tools",
]
