from typing import Any, Dict, List

from .cache import get_cv_data


def get_personal_info() -> Dict[str, Any]:
    """
    Obtiene información personal básica del CV.

    Returns:
        Dict con información personal básica
    """
    cv_data = get_cv_data()
    if not cv_data:
        return {"error": "No se pudo obtener el CV"}

    basics = cv_data.get("basics", {})
    return {
        "name": basics.get("name", "No disponible"),
        "label": basics.get("label", "No disponible"),
        "email": basics.get("email", "No disponible"),
        "summary": basics.get("summary", "No disponible"),
        "location": basics.get("location", {}),
        "profiles": basics.get("profiles", []),
    }


def get_work_experience() -> List[Dict[str, Any]]:
    """
    Obtiene la experiencia laboral del CV.

    Returns:
        Lista con experiencia laboral
    """
    cv_data = get_cv_data()
    if not cv_data:
        return [{"error": "No se pudo obtener el CV"}]

    return cv_data.get("work", [])


def get_education() -> List[Dict[str, Any]]:
    """
    Obtiene la información educativa del CV.

    Returns:
        Lista con información educativa
    """
    cv_data = get_cv_data()
    if not cv_data:
        return [{"error": "No se pudo obtener el CV"}]

    return cv_data.get("education", [])


def get_skills() -> Dict[str, Any]:
    """
    Obtiene las habilidades del CV organizadas por categorías.

    Returns:
        Dict con habilidades organizadas por categorías
    """
    cv_data = get_cv_data()
    if not cv_data:
        return {"error": "No se pudo obtener el CV"}

    return {
        "highlighted": cv_data.get("highlightedSkills", []),
        "other": cv_data.get("otherSkills", []),
        "databases": cv_data.get("databasesSkills", []),
    }


def get_projects() -> List[Dict[str, Any]]:
    """
    Obtiene los proyectos del CV.

    Returns:
        Lista con proyectos
    """
    cv_data = get_cv_data()
    if not cv_data:
        return [{"error": "No se pudo obtener el CV"}]

    return cv_data.get("projects", [])


def get_certificates() -> List[Dict[str, Any]]:
    """
    Obtiene los certificados del CV.

    Returns:
        Lista con certificados
    """
    cv_data = get_cv_data()
    if not cv_data:
        return [{"error": "No se pudo obtener el CV"}]

    return cv_data.get("certificates", [])
