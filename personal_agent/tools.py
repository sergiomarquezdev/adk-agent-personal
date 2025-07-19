import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests

# Cache para el CV descargado
_cv_cache = None
_cache_timestamp = None
_cache_duration = timedelta(hours=1)  # Cache por 1 hora


def download_cv_from_url(
    url: str = "https://cv.sergiomarquez.dev/cv.json",
) -> Optional[Dict[str, Any]]:
    """
    Descarga el CV desde la URL especificada.

    Args:
        url: URL del CV JSON (por defecto: https://cv.sergiomarquez.dev/cv.json)

    Returns:
        Dict con el contenido del CV o None si hay error
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error descargando CV: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parseando JSON del CV: {e}")
        return None


def get_cv_data(force_refresh: bool = False) -> Optional[Dict[str, Any]]:
    """
    Obtiene los datos del CV, usando cache si está disponible y no ha expirado.

    Args:
        force_refresh: Si True, fuerza la descarga sin usar cache

    Returns:
        Dict con el contenido del CV o None si hay error
    """
    global _cv_cache, _cache_timestamp

    # Verificar si tenemos cache válido
    if not force_refresh and _cv_cache is not None and _cache_timestamp is not None:
        if datetime.now() - _cache_timestamp < _cache_duration:
            return _cv_cache

    # Descargar nuevo CV
    cv_data = download_cv_from_url()
    if cv_data:
        _cv_cache = cv_data
        _cache_timestamp = datetime.now()
        return cv_data

    return None


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


def get_skills() -> Dict[str, List[Dict[str, Any]]]:
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
