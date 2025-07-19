import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import requests

# Cache para el CV descargado
_cv_cache: Optional[Dict[str, Any]] = None
_cache_timestamp: Optional[datetime] = None
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
