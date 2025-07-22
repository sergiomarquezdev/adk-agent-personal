# 🤖 Asistente Personal de Sergio Márquez

Un sistema de **inteligencia artificial multi-agente** que actúa como Sergio Márquez, desarrollador IA/ML. El sistema incluye especialistas para consultar su CV dinámico y buscar en su blog, con una interfaz web moderna incluida.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-orange.svg)](https://ai.google.dev/)
[![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-purple.svg)](https://ai.google.dev/gemini/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 🚀 Características

- **🎭 Sistema Multi-Agente**: Arquitectura con agentes especializados para diferentes tareas
- **📊 CV Dinámico**: Carga optimizada desde archivo local `nginx/cv.json`
- **📝 Búsqueda en Blog**: Integración con Google Search para `blog.sergiomarquez.dev`
- **🎨 Frontend Moderno**: Interfaz web elegante con soporte Markdown completo
- **⚡ FastAPI + ADK**: Backend robusto con Google Agent Development Kit
- **🧪 Tests Completos**: Suite de tests con pytest (100% passing)
- **🐳 Docker Ready**: Contenedor optimizado para despliegue
- **📱 API REST**: Endpoints documentados con OpenAPI/Swagger

## 🏗️ Arquitectura Multi-Agente

```
┌─────────────────────────────────────────────────────────┐
│                Personal_Orchestrator                    │
│          (Coordinador Ejecutivo)                       │
└─────────────────┬───────────────────┬───────────────────┘
                  │                   │
         ┌────────▼────────┐ ┌───────▼────────┐
         │   CV_Expert     │ │  Blog_Expert   │
         │ (Especialista   │ │ (Archivista    │
         │  en CV)         │ │  Digital)      │
         └─────────────────┘ └────────────────┘
```

### Agentes Especializados

- **🎯 Personal_Orchestrator**: Analiza consultas y delega al especialista adecuado
- **👨‍💼 CV_Expert**: Responde sobre experiencia, habilidades y trayectoria profesional
- **📚 Blog_Expert**: Busca artículos específicos usando Google Search

## 🏗️ Estructura del Proyecto

```
adk-agent-personal/
├── assistant/               # Módulo principal del asistente
│   ├── __init__.py         # Definición del paquete
│   ├── agents.py           # Arquitectura multi-agente (ADK)
│   ├── services.py         # Lógica de negocio e invocación
│   └── tools.py            # Herramientas (CV y blog search)
├── tests/                  # Suite de tests completa
│   ├── conftest.py         # Fixtures y configuración pytest
│   ├── test_agents.py      # Tests de agentes
│   ├── test_main.py        # Tests de API FastAPI
│   ├── test_services.py    # Tests de servicios
│   ├── test_tools.py       # Tests de herramientas
│   ├── test_integration.py # Tests de integración
│   ├── TESTING_GUIDE.md    # Guía de testing
│   └── TEST_RESULTS.md     # Resultados de tests
├── nginx/                  # Frontend y configuración web
│   ├── index.html          # Interfaz web moderna
│   ├── nginx.conf          # Configuración Nginx
│   ├── docker-compose.yml  # Stack completo
│   └── update.sh           # Script de despliegue
├── main.py                 # Servidor FastAPI
├── requirements.txt        # Dependencias Python
├── pytest.ini            # Configuración pytest
└── Dockerfile             # Contenedor Docker
```

## 🛠️ Tecnologías

- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **IA/ML**: Google ADK (Agent Development Kit), Gemini 1.5 Flash
- **Frontend**: HTML5, CSS3, JavaScript con sistema de rendering robusto
- **Rendering**: DOMParser + sanitización automática + detección de contenido
- **Búsqueda**: Google Search API (googlesearch-python)
- **Testing**: Pytest, pytest-asyncio, pytest-mock, httpx
- **Containerización**: Docker, Docker Compose
- **Proxy**: Nginx (para producción)

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

5. **Acceder a la aplicación**
   - **Frontend**: http://localhost:8000/nginx/
   - **API Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/api/health

### Instalación con Docker

```bash
# Stack completo (Backend + Frontend + Nginx)
cd nginx
docker-compose up -d

# Solo backend
docker build -t adk-agent-personal .
docker run -p 8000:8000 --env-file .env adk-agent-personal
```

## 🚀 Uso

### Interfaz Web

La interfaz web está disponible en `/nginx/index.html` con características modernas:

- **🎨 Diseño elegante**: UI/UX optimizada para conversaciones
- **🤖 Rendering robusto**: Sistema adaptativo que maneja HTML, Markdown y texto automáticamente
- **🔒 Seguridad avanzada**: DOMParser + sanitización previenen vulnerabilidades XSS
- **💬 Chat fluido**: Experiencia conversacional natural sin errores de renderizado
- **📱 Responsive**: Adaptado para móviles y escritorio
- **⚡ Tiempo real**: Indicadores de typing y loading

### API REST

```bash
# Consulta sobre experiencia profesional
curl -X POST "http://localhost:8000/api/invoke" \
     -H "Content-Type: application/json" \
     -d '{"message": "Háblame de tu experiencia en IA/ML"}'

# Búsqueda en blog
curl -X POST "http://localhost:8000/api/invoke" \
     -H "Content-Type: application/json" \
     -d '{"message": "¿Has escrito sobre Docker?"}'
```

### Ejemplo de Respuesta

```json
{
  "response": "<h2>🤖 Mi Experiencia en IA/ML</h2><p>Como <strong>Desarrollador IA/ML</strong> he trabajado con:</p><ul><li><code>Python</code> para machine learning</li><li><strong>TensorFlow</strong> y <strong>PyTorch</strong></li><li><strong>Google Cloud AI</strong> y ADK</li><li>Automatización con <strong>FastAPI</strong></li></ul>",
  "session_id": "user_abc123..."
}
```

> **Nota**: El sistema de rendering robusto detecta automáticamente si la respuesta es HTML, Markdown o texto plano, y la renderiza de forma segura usando DOMParser + sanitización.

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con verbose y coverage
pytest -v --tb=short

# Tests específicos
pytest tests/test_agents.py
pytest tests/test_integration.py

# Solo tests de unidad
pytest -m unit
```

### Resultados Actuales

- ✅ **57/57 tests pasando** (100%)
- 🧪 **5 módulos testeados** completamente
- 📊 **Cobertura completa** de funcionalidades críticas

Ver `tests/TEST_RESULTS.md` para detalles completos.

## 🔧 Configuración

### Variables de Entorno

| Variable         | Descripción                 | Requerido | Default |
| ---------------- | --------------------------- | --------- | ------- |
| `GOOGLE_API_KEY` | API key de Google AI Studio | ✅        | -       |
| `PORT`           | Puerto del servidor         | ❌        | 8000    |

### Personalización de Agentes

Los prompts de los agentes están optimizados para HTML en `assistant/agents.py`:

```python
# CV_Expert - Estructurado con HTML
- Usa `<h2>Encabezado</h2>` para secciones principales
- `<strong>texto</strong>` para resaltar tecnologías y empresas
- `<em>cursiva</em>` para fechas y ubicaciones
- `<code>tecnología</code>` para herramientas específicas

# Blog_Expert - Visual con HTML
- `<h2>📝 Artículos encontrados sobre [tema]</h2>`
- `<ul><li><strong>[Título]</strong> - <a href="[URL]">[URL]</a></li></ul>`

# Personal_Orchestrator - Conversacional con HTML
- Mantén fluidez natural
- `<strong>texto</strong>` para énfasis importantes
- `<p>párrafo</p>` para bloques de texto
```

### Sistema de Rendering Robusto

El frontend incluye un sistema avanzado de rendering (`enhanced_rendering.js`) que:

- **🔍 Detecta automáticamente** el tipo de contenido (HTML/Markdown/Texto)
- **🛡️ Sanitiza** todo el HTML para prevenir XSS
- **🔄 Fallback inteligente** garantiza que el contenido siempre se muestre
- **⚡ DOMParser** reemplaza `innerHTML` para mayor seguridad y robustez

## 🎯 Funcionalidades

### Consultas sobre CV

El **CV_Expert** puede responder sobre:

- **👤 Información Personal**: Nombre, contacto, resumen profesional
- **💼 Experiencia Laboral**: Roles, responsabilidades, tecnologías usadas
- **🎓 Educación**: Formación académica y certificaciones
- **🛠️ Habilidades**: Técnicas organizadas por categorías
- **📁 Proyectos**: Desarrollos personales y profesionales

### Búsqueda en Blog

El **Blog_Expert** busca en `blog.sergiomarquez.dev`:

- **🔍 Google Search**: Usando operador `site:blog.sergiomarquez.dev`
- **📝 Resultados estructurados**: Títulos y URLs organizados
- **⚡ Búsqueda real**: Sin fallbacks, resultados actualizados

### Ejemplos de Consultas

```
# Experiencia profesional
"¿Cuál es tu experiencia en Python?"
"Háblame de tus proyectos de IA"
"¿Qué tecnologías dominas?"

# Búsqueda en blog
"¿Has escrito sobre Docker?"
"Artículos sobre machine learning"
"Posts sobre FastAPI"
```

## 🔄 Desarrollo

### Arquitectura del Sistema de Rendering

El proyecto utiliza un sistema de rendering robusto que garantiza la correcta visualización del contenido:

```
Agente → Contenido → ContentRenderer → Detección Automática → Renderer Específico → DOM
                           ↓                      ↓                    ↓
                    HTML/Markdown/Texto     HTMLRenderer        DOMParser + Sanitización
                                          MarkdownRenderer      Conversión + HTMLRenderer
                                           TextRenderer        textContent seguro
```

### Agregar Nuevos Agentes

1. **Definir agente** en `assistant/agents.py`
2. **Crear herramientas** en `assistant/tools.py`
3. **Integrar** en `Personal_Orchestrator.sub_agents`
4. **Escribir tests** en `tests/`
5. **Configurar respuesta HTML** siguiendo las guías de formato

### Ejemplo de Nuevo Agente

```python
weather_agent = Agent(
    name="Weather_Expert",
    description="Especialista en información meteorológica",
    model="gemini-1.5-flash",
    instruction="...",
    tools=[get_weather_info],
)
```

### Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/NewAgent`)
3. Implementar con tests
4. Commit cambios (`git commit -m 'Add Weather Agent'`)
5. Push y crear Pull Request

## 🐛 Troubleshooting

### Problemas Comunes

**❌ Error de API Key**

```bash
# Verificar configuración
echo $GOOGLE_API_KEY
# Debe mostrar tu API key
```

**❌ Tests fallando**

```bash
# Reinstalar dependencias de testing
pip install pytest pytest-asyncio pytest-mock httpx
pytest --tb=short
```

**❌ Frontend no carga**

```bash
# Verificar servidor está corriendo
curl http://localhost:8000/api/health
# Debe devolver {"status": "OK"}
```

### Logs y Debugging

```bash
# Logs detallados
python main.py --log-level debug

# Verificar imports
python -c "from assistant import agents, services, tools; print('✅ Imports OK')"

# Test rápido de API
curl http://localhost:8000/api/health
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Sergio Márquez**

- 💼 LinkedIn: [Sergio Márquez](https://linkedin.com/in/sergiomarquez)
- 🐙 GitHub: [@sergiomarquez](https://github.com/sergiomarquez)
- 📄 CV: [cv.sergiomarquez.dev](https://cv.sergiomarquez.dev)
- 📝 Blog: [blog.sergiomarquez.dev](https://blog.sergiomarquez.dev)

## 🙏 Agradecimientos

- [Google ADK](https://ai.google.dev/) por el framework de agentes
- [Gemini 1.5 Flash](https://ai.google.dev/gemini/) por el modelo de IA
- [FastAPI](https://fastapi.tiangolo.com/) por el framework web
- [Pytest](https://pytest.org/) por el framework de testing
- [Marked.js](https://marked.js.org/) por el renderizado Markdown

---

⭐ **Si este proyecto te resulta útil, ¡dale una estrella en GitHub!**
