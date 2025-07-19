"""
Archivo principal de herramientas del agente personal.
Este archivo mantiene compatibilidad hacia atrás mientras redirige a la nueva estructura modular.
"""

# Importar desde el nuevo módulo CV
from .tools.cv import search_cv_info

# Re-exportar para mantener compatibilidad
__all__ = ["search_cv_info"]
