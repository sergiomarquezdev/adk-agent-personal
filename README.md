# 🤖 Agente Personal de Sergio Márquez

Un agente de inteligencia artificial personal que actúa como Sergio Márquez, desarrollador IA/ML con experiencia en Python, FastAPI y automatización. El agente puede consultar información actualizada de su CV y responder preguntas sobre su experiencia profesional.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-orange.svg)](https://ai.google.dev/)
[![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-purple.svg)](https://ai.google.dev/gemini/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 🚀 Características

- **🤖 Agente Personalizado**: Actúa como Sergio Márquez con personalidad profesional pero cercana
- **📊 CV Dinámico**: Consulta información actualizada desde `https://cv.sergiomarquez.dev/cv.json`
- **🔍 Búsqueda Inteligente**: Analiza consultas en español e inglés para encontrar información relevante
- **⚡ Cache Optimizado**: Sistema de cache automático para mejorar el rendimiento
- **🏗️ Arquitectura Modular**: Herramientas organizadas en módulos especializados
- **🐳 Docker Ready**: Contenedor Docker optimizado para despliegue
- **🧪 Tests Completos**: Suite de tests automatizados y manuales
- **📱 API REST**: Endpoint RESTful para integración con aplicaciones

## 🏗️ Arquitectura

```
adk-agent-personal/
├── assistant/           # Módulo principal del agente
│   ├── agent.py             # Configuración del agente ADK
│   ├── tools.py             # Punto de entrada de herramientas (compatibilidad)
│   └── tools/               # Herramientas modulares
│       ├── cv/              # Herramientas del CV
│       │   ├── cache.py     # Gestión de cache y descarga
│       │   ├── extractors.py # Extracción de datos específicos
│       │   └── search.py    # Búsqueda inteligente
│       └── README.md        # Documentación de herramientas
├── main.py                  # Servidor FastAPI
├── requirements.txt         # Dependencias Python
├── Dockerfile              # Contenedor Docker
├── test/                   # Tests automatizados
```

## 🛠️ Tecnologías

- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **IA/ML**: Google ADK, Gemini 1.5 Flash
- **Cache**: Sistema de cache en memoria con expiración
- **Testing**: Pytest, requests
- **Containerización**: Docker
- **API**: RESTful con documentación automática

## 📦 Instalación

### Prerrequisitos

- Python 3.11 o superior
- Docker (opcional)
- Cuenta de Google AI Studio con API key

### Instalación Local

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/sergiomarquezdev/adk-agent-personal.git
   cd adk-agent-personal
   ```

2. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**

   ```bash
   # Crear archivo .env
   echo "GOOGLE_API_KEY=tu-api-key-aqui" > .env
   ```

4. **Ejecutar el servidor**
   ```bash
   python main.py
   ```

### Instalación con Docker

1. **Construir la imagen**

   ```bash
   docker build -t adk-agent-personal .
   ```

2. **Ejecutar el contenedor**
   ```bash
   docker run -p 8000:8000 --env-file .env adk-agent-personal
   ```

## 🚀 Uso

### API REST

El servidor expone un endpoint REST para interactuar con el agente:

```bash
# Ejemplo de uso con curl
curl -X POST "http://localhost:8000/api/invoke" \
     -H "Content-Type: application/json" \
     -d '{"message": "Háblame de tu experiencia laboral"}'
```

### Ejemplo de Respuesta

```json
{
  "response": "Perfecto. Según mi CV, he tenido dos roles principales en XXXXX:\n\nPrimero, desde mayo de 2025, trabajo como **Desarrollador IA/ML**..."
}
```

### Uso Programático

```python
import requests

def ask_agent(question: str) -> str:
    response = requests.post(
        "http://localhost:8000/api/invoke",
        json={"message": question}
    )
    return response.json()["response"]

# Ejemplo de uso
answer = ask_agent("¿Cuáles son tus habilidades en Python?")
print(answer)
```

## 🧪 Testing

### Tests Automatizados

```bash
# Ejecutar todos los tests
pytest test/test_api_pytest.py

# Ejecutar con verbose
pytest -v test/test_api_pytest.py
```

### Tests Manuales

```bash
# Test manual de la API
python test/test_api.py
```

### Verificación de Funcionamiento

```python
# Verificar importaciones
from assistant.tools import search_cv_info
from assistant.agent import root_agent

# Verificar funcionalidad básica
result = search_cv_info("experiencia")
assert result['type'] == 'work_experience'
```

## 🔧 Configuración

### Variables de Entorno

| Variable         | Descripción                         | Requerido |
| ---------------- | ----------------------------------- | --------- |
| `GOOGLE_API_KEY` | API key de Google AI Studio         | ✅        |
| `PORT`           | Puerto del servidor (default: 8000) | ❌        |

### Configuración del Agente

El agente está configurado en `assistant/agent.py` con:

- **Modelo**: Gemini 1.5 Flash
- **Personalidad**: Profesional pero cercana
- **Herramientas**: Búsqueda inteligente en CV
- **Reglas**: No política, religión ni temas controvertidos

## 📊 Funcionalidades del CV

El agente puede consultar y responder sobre:

- **👤 Información Personal**: Nombre, email, resumen, ubicación
- **💼 Experiencia Laboral**: Roles, responsabilidades, tecnologías
- **🎓 Educación**: Formación académica y certificaciones
- **🛠️ Habilidades**: Técnicas organizadas por categorías
- **📁 Proyectos**: Personales y profesionales
- **🏆 Certificaciones**: Acreditaciones y cursos

### Palabras Clave Soportadas

- **Experiencia**: `experiencia`, `trabajo`, `work`, `laboral`
- **Educación**: `educación`, `education`, `estudios`
- **Habilidades**: `habilidades`, `skills`, `tecnologías`
- **Proyectos**: `proyectos`, `projects`
- **Certificados**: `certificados`, `certificates`

## 🔄 Desarrollo

### Estructura Modular

Las herramientas están organizadas en módulos especializados:

```python
# Importación básica (compatibilidad)
from assistant.tools import search_cv_info

# Importación directa (recomendada)
from assistant.tools.cv import search_cv_info
```

### Agregar Nuevas Herramientas

1. Crear nuevo directorio en `assistant/tools/`
2. Implementar funciones necesarias
3. Actualizar `assistant/tools/__init__.py`
4. Agregar documentación
5. Crear tests

### Ejemplo de Nuevo Módulo

```
tools/
├── weather/
│   ├── __init__.py
│   ├── api_client.py
│   └── forecast.py
└── cv/ (existente)
```

## 🐛 Troubleshooting

### Problemas Comunes

**Error: "No se pudo encontrar 'invoke_agent_async'"**

- Verificar que `assistant/agent.py` existe
- Comprobar que la función está definida correctamente

**Error: "Library stubs not installed for 'requests'"**

- Instalar tipos: `pip install types-requests`
- O ignorar el warning (no afecta funcionalidad)

**Error de API Key**

- Verificar que `GOOGLE_API_KEY` está configurada
- Comprobar que la key es válida en Google AI Studio

### Logs y Debugging

```bash
# Ejecutar con logs detallados
python main.py --log-level debug

# Verificar conectividad
curl http://localhost:8000/docs
```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

### Guías de Contribución

- Seguir PEP 8 para estilo de código
- Agregar tests para nuevas funcionalidades
- Actualizar documentación según sea necesario
- Verificar que todos los tests pasen

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Sergio Márquez**

- LinkedIn: [Sergio Márquez](https://linkedin.com/in/sergiomarquez)
- GitHub: [@sergiomarquez](https://github.com/sergiomarquez)
- CV: [cv.sergiomarquez.dev](https://cv.sergiomarquez.dev)

## 🙏 Agradecimientos

- [Google ADK](https://ai.google.dev/) por el framework de agentes
- [Gemini](https://ai.google.dev/gemini/) por el modelo de IA
- [FastAPI](https://fastapi.tiangolo.com/) por el framework web
- [Pytest](https://pytest.org/) por el framework de testing

---

⭐ **Si este proyecto te resulta útil, ¡dale una estrella en GitHub!**
