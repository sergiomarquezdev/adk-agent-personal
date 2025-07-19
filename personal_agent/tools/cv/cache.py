import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import requests

# --- New: Define a path for the local CV ---
_local_cv_path = "cv.json"

# Cache para el CV
_cv_cache: Optional[Dict[str, Any]] = None
_cache_timestamp: Optional[datetime] = None
_cache_duration = timedelta(hours=1)  # Cache por 1 hora


def _load_local_cv() -> Optional[Dict[str, Any]]:
    """
    Intenta cargar el CV desde un archivo local 'cv.json'.
    """
    if not os.path.exists(_local_cv_path):
        return None
    try:
        with open(_local_cv_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error leyendo CV local: {e}")
        return None


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
        print(f"DEBUG: Descargando CV desde {url}")
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
    Obtiene los datos del CV.
    Prioriza la carga desde un archivo local. Si no existe, lo descarga de una URL.
    Utiliza un sistema de cache para mejorar el rendimiento.

    Args:
        force_refresh: Si True, fuerza la recarga sin usar cache.

    Returns:
        Dict con el contenido del CV o None si hay error.
    """
    global _cv_cache, _cache_timestamp

    # 1. Comprobar cache
    if not force_refresh and _cv_cache is not None and _cache_timestamp is not None:
        if datetime.now() - _cache_timestamp < _cache_duration:
            print("DEBUG: Usando CV desde cache.")
            return _cv_cache

    # 2. Intentar cargar desde el archivo local
    print("DEBUG: Intentando cargar CV desde archivo local.")
    cv_data = _load_local_cv()

    # 3. Si no hay archivo local, descargar desde la URL (fallback)
    if cv_data is None:
        print("DEBUG: No se encontró CV local, descargando desde URL.")
        cv_data = download_cv_from_url()

    # 4. Si se obtuvieron datos (local o URL), actualizar cache
    if cv_data:
        print("DEBUG: CV cargado exitosamente, actualizando cache.")
        _cv_cache = cv_data
        _cache_timestamp = datetime.now()
        return cv_data

    # 5. Si todo falla, retornar None
    print("ERROR: No se pudo cargar el CV ni localmente ni desde la URL.")
    return None
