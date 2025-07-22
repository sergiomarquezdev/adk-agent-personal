# tools.py
# Herramientas que los agentes especialistas pueden utilizar.

import json
import os

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
    """Carga y devuelve el contenido del CV desde el archivo local."""
    # Calcular la raíz del proyecto de forma robusta
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cv_path = os.path.join(project_root, "nginx", "cv.json")

    try:
        print(f"📄 Cargando CV desde archivo local: {cv_path}")
        with open(cv_path, "r", encoding="utf-8") as f:
            cv_data = json.load(f)
            return json.dumps(cv_data, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo CV en {cv_path}.")
        return json.dumps(
            {
                "name": "Sergio Márquez",
                "title": "Desarrollador IA/ML",
                "note": "CV no disponible. Archivo no encontrado.",
            },
            indent=2,
            ensure_ascii=False,
        )
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON del CV: {e}")
        return json.dumps(
            {"name": "Sergio Márquez", "error": "Error en formato del CV"},
            indent=2,
            ensure_ascii=False,
        )
