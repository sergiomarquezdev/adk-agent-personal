# tools.py
# Herramientas que los agentes especialistas pueden utilizar.

import json
import os

import requests
from googlesearch import search


def search_blog_posts(query: str) -> str:
    """
    Busca artículos en el blog de Sergio usando Google Search con el operador site:.

    Args:
        query: El tema que el usuario quiere buscar en el blog.

    Returns:
        Una cadena con los artículos encontrados o un mensaje indicando que no se encontraron.
    """
    print(f"--- Ejecutando herramienta: search_blog_posts con query: '{query}' ---")

    # Construir la query de búsqueda con el operador site:
    google_query = f"site:blog.sergiomarquez.dev {query}"
    print(f"Buscando en Google: {google_query}")

    try:
        # Realizar búsqueda en Google (limitamos a 10 resultados)
        search_results = []
        for url in search(google_query, num_results=10, lang="es"):
            search_results.append(url)

        if not search_results:
            return f"Lo siento, pero no he encontrado ningún artículo sobre '{query}' en mi blog."

        # Formatear los resultados
        results_text = f"He encontrado {len(search_results)} artículo(s) sobre '{query}' en mi blog:\n\n"
        for i, url in enumerate(search_results, 1):
            # Extraer el título del artículo de la URL si es posible
            article_title = (
                url.replace("https://blog.sergiomarquez.dev/", "")
                .replace("-", " ")
                .title()
            )
            results_text += f"{i}. {article_title}\n   {url}\n\n"

        return results_text.strip()

    except Exception as e:
        print(f"Error al buscar en Google: {e}")
        return "Lo siento, pero no he podido buscar en mi blog en este momento. Por favor, intenta de nuevo más tarde."


def load_cv_data() -> str:
    """Descarga y devuelve el contenido del CV desde la página web de Sergio."""
    cv_url = "https://cv.sergiomarquez.dev/cv.json"

    try:
        print(f"Descargando CV desde: {cv_url}")
        response = requests.get(cv_url, timeout=10)
        response.raise_for_status()  # Lanza excepción si hay error HTTP

        # Verificar que la respuesta sea JSON válido
        cv_data = response.json()
        return json.dumps(cv_data, indent=2, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el CV desde {cv_url}: {e}")
        # Fallback: intentar cargar desde archivo local si existe
        fallback_path = os.path.join(
            os.path.dirname(__file__), "..", "nginx", "cv.json"
        )
        try:
            with open(fallback_path, "r", encoding="utf-8") as f:
                print("Usando CV local como fallback")
                return json.dumps(json.load(f), indent=2, ensure_ascii=False)
        except FileNotFoundError:
            print("No se encontró archivo CV local. Usando CV básico como fallback.")
            # CV básico de emergencia
            return json.dumps(
                {
                    "name": "Sergio Márquez",
                    "title": "Desarrollador Full Stack",
                    "note": "CV no disponible temporalmente. Intenta de nuevo más tarde.",
                },
                indent=2,
                ensure_ascii=False,
            )

    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON del CV: {e}")
        return json.dumps(
            {"name": "Sergio Márquez", "error": "Error en formato del CV"},
            indent=2,
            ensure_ascii=False,
        )
