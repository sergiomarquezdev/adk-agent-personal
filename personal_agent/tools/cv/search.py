from typing import Any, Dict

from .extractors import (
    get_certificates,
    get_education,
    get_personal_info,
    get_projects,
    get_skills,
    get_work_experience,
)


def search_cv_info(query: str) -> Dict[str, Any]:
    """
    Busca información específica en el CV basada en una consulta.

    Args:
        query: Consulta de búsqueda (ej: "experiencia", "habilidades", "proyectos")

    Returns:
        Dict con información encontrada
    """
    query_lower = query.lower()

    if any(
        word in query_lower for word in ["experiencia", "trabajo", "work", "laboral"]
    ):
        return {"type": "work_experience", "data": get_work_experience()}

    elif any(word in query_lower for word in ["educación", "education", "estudios"]):
        return {"type": "education", "data": get_education()}

    elif any(
        word in query_lower
        for word in ["habilidades", "skills", "tecnologías", "technologies"]
    ):
        return {"type": "skills", "data": get_skills()}

    elif any(word in query_lower for word in ["proyectos", "projects"]):
        return {"type": "projects", "data": get_projects()}

    elif any(word in query_lower for word in ["certificados", "certificates"]):
        return {"type": "certificates", "data": get_certificates()}

    elif any(word in query_lower for word in ["personal", "info", "básica", "basic"]):
        return {"type": "personal_info", "data": get_personal_info()}

    else:
        return {
            "type": "general",
            "data": {
                "personal_info": get_personal_info(),
                "work_experience": get_work_experience(),
                "skills": get_skills(),
            },
        }
