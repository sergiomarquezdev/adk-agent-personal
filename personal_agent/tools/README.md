# Módulo de Herramientas del Agente Personal

Este directorio contiene las herramientas modulares del agente personal de Sergio Márquez, organizadas por funcionalidad para facilitar el mantenimiento y la escalabilidad.

## 🏗️ Estructura del Proyecto

```
personal_agent/
├── tools/
│   ├── __init__.py          # Exporta las funciones principales
│   ├── README.md            # Este archivo de documentación
│   └── cv/                  # Herramientas relacionadas con el CV
│       ├── __init__.py      # Exporta funciones del módulo CV
│       ├── cache.py         # Manejo de cache y descarga del CV
│       ├── extractors.py    # Funciones de extracción de datos del CV
│       └── search.py        # Función de búsqueda inteligente en el CV
└── tools.py                 # Archivo principal (compatibilidad hacia atrás)
```

## 📦 Módulos Disponibles

### CV (`cv/`)

Contiene todas las herramientas relacionadas con el manejo del CV de Sergio Márquez, incluyendo descarga, cache, extracción de datos y búsqueda inteligente.

#### `cache.py` - Gestión de Datos y Cache

**Funciones principales:**

- `download_cv_from_url(url: str) -> Optional[Dict[str, Any]]`: Descarga el CV desde la URL especificada con manejo de errores
- `get_cv_data(force_refresh: bool = False) -> Optional[Dict[str, Any]]`: Obtiene los datos del CV con cache automático de 1 hora

**Características:**

- Cache automático con expiración de 1 hora
- Manejo robusto de errores de red y JSON
- Timeout de 10 segundos para descargas
- URL por defecto: `https://cv.sergiomarquez.dev/cv.json`

#### `extractors.py` - Extracción de Datos Específicos

**Funciones de extracción:**

- `get_personal_info() -> Dict[str, Any]`: Información personal básica (nombre, email, resumen, ubicación, perfiles)
- `get_work_experience() -> List[Dict[str, Any]]`: Experiencia laboral completa
- `get_education() -> List[Dict[str, Any]]`: Información educativa y formación
- `get_skills() -> Dict[str, Any]`: Habilidades técnicas organizadas por categorías
- `get_projects() -> List[Dict[str, Any]]`: Proyectos personales y profesionales
- `get_certificates() -> List[Dict[str, Any]]`: Certificaciones y acreditaciones

**Organización de habilidades:**

- `highlighted`: Habilidades destacadas
- `other`: Otras habilidades técnicas
- `databases`: Habilidades en bases de datos

#### `search.py` - Búsqueda Inteligente

**Función principal:**

- `search_cv_info(query: str) -> Dict[str, Any]`: Función de búsqueda que analiza consultas en español e inglés y devuelve información relevante

**Palabras clave soportadas:**

- **Experiencia laboral**: `experiencia`, `trabajo`, `work`, `laboral`
- **Educación**: `educación`, `education`, `estudios`
- **Habilidades**: `habilidades`, `skills`, `tecnologías`, `technologies`
- **Proyectos**: `proyectos`, `projects`
- **Certificados**: `certificados`, `certificates`
- **Información personal**: `personal`, `info`, `básica`, `basic`

## 🚀 Uso Práctico

### Importación Básica

```python
# Importar la función principal de búsqueda
from personal_agent.tools import search_cv_info

# Buscar información específica
result = search_cv_info("experiencia laboral")
print(result['type'])  # 'work_experience'
print(result['data'])  # Lista de experiencias laborales
```

### Importación Directa de Módulos

```python
# Importar funciones específicas del módulo CV
from personal_agent.tools.cv import get_personal_info, get_skills

# Obtener información personal
personal_info = get_personal_info()
print(f"Nombre: {personal_info['name']}")

# Obtener habilidades
skills = get_skills()
print(f"Habilidades destacadas: {skills['highlighted']}")
```

### Uso con el Agente

```python
# El agente usa automáticamente las herramientas refactorizadas
from personal_agent.agent import invoke_agent

response = invoke_agent("¿Cuáles son tus habilidades en Python?")
print(response)
```

## 🔧 Compatibilidad

### Compatibilidad Hacia Atrás

El archivo `tools.py` en el directorio raíz mantiene **compatibilidad hacia atrás** completa:

```python
# Esto sigue funcionando sin cambios
from personal_agent.tools import search_cv_info
```

### Migración Gradual

Los desarrolladores pueden migrar gradualmente a la nueva estructura:

```python
# Forma antigua (sigue funcionando)
from personal_agent.tools import search_cv_info

# Forma nueva (recomendada)
from personal_agent.tools.cv import search_cv_info
```

## 🧪 Testing

### Tests Existentes

Todos los tests existentes siguen funcionando sin modificaciones:

```bash
# Tests manuales
python test/test_api.py

# Tests automatizados
pytest test/test_api_pytest.py
```

### Verificación de Funcionamiento

```python
# Verificar que las importaciones funcionan
from personal_agent.tools import search_cv_info
from personal_agent.tools.cv import get_cv_data

# Verificar funcionalidad básica
result = search_cv_info("experiencia")
assert result['type'] == 'work_experience'
```

## 🔮 Futuras Expansiones

Esta estructura modular permite fácilmente agregar nuevos módulos de herramientas:

### Módulos Planificados

- `tools/weather/` - Información meteorológica y clima
- `tools/calendar/` - Gestión de calendario y eventos
- `tools/email/` - Manejo de correos electrónicos
- `tools/notifications/` - Sistema de notificaciones
- `tools/analytics/` - Análisis de datos y métricas

### Estructura para Nuevos Módulos

```
tools/
├── weather/
│   ├── __init__.py
│   ├── api_client.py
│   └── forecast.py
├── calendar/
│   ├── __init__.py
│   ├── events.py
│   └── reminders.py
└── cv/ (existente)
```

## 🤝 Contribución

Para agregar nuevas herramientas:

1. Crear un nuevo directorio en `tools/`
2. Implementar las funciones necesarias
3. Actualizar `tools/__init__.py` para exportar las nuevas funciones
4. Agregar documentación en este README
5. Crear tests para las nuevas funcionalidades

## 📞 Soporte

Para problemas o preguntas sobre las herramientas:

- Revisar la documentación de cada módulo
- Verificar los tests existentes
- Consultar la estructura de importaciones
