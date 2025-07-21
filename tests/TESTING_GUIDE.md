# 🧪 Guía de Testing - Personal Agent

## 🚀 **Comandos de Testing**

### Ejecutar todos los tests

```bash
pytest -v
```

### Ejecutar tests específicos

```bash
# Solo tests que pasan actualmente
pytest test_agents.py test_tools.py::TestLoadCvData -v

# Test específico
pytest test_main.py::TestFastAPIEndpoints::test_health_endpoint -v

# Tests por módulo
pytest test_tools.py -v
pytest test_agents.py -v
pytest test_main.py -v
pytest test_services.py -v
pytest test_integration.py -v
```

### Ejecutar con coverage

```bash
pip install pytest-cov
pytest --cov=assistant --cov-report=html
```

### Ejecutar tests en paralelo

```bash
pip install pytest-xdist
pytest -n auto
```

## 📁 **Estructura de Tests**

```
├── conftest.py              # Fixtures compartidas
├── test_tools.py            # Tests para herramientas
├── test_agents.py           # Tests para agentes
├── test_main.py             # Tests para FastAPI
├── test_services.py         # Tests para servicios
├── test_integration.py      # Tests de integración
├── TEST_RESULTS.md          # Resumen de resultados
└── TESTING_GUIDE.md         # Esta guía
```

## 🔧 **Fixtures Principales**

### Datos Mock

- `mock_cv_data`: Datos de CV de ejemplo
- `mock_search_results`: Resultados de búsqueda simulados

### Mocks de APIs

- `mock_requests_get`: Mock para requests HTTP
- `mock_googlesearch`: Mock para búsquedas de Google
- `mock_adk_runner`: Mock para el runner de ADK

### Cliente de Test

- `test_client`: Cliente de FastAPI para tests de endpoints

## 🎯 **Categorías de Tests**

### 1. **Tests Unitarios**

- Funciones individuales (`load_cv_data`, `search_blog_posts`)
- Configuración de agentes
- Modelos de datos Pydantic

### 2. **Tests de Integración**

- Flujo completo de endpoints
- Interacción entre servicios
- Gestión de sesiones

### 3. **Tests de API**

- Endpoints HTTP
- Validación de entrada/salida
- Códigos de estado HTTP

## 🔍 **Debugging Tests**

### Ver output detallado

```bash
pytest -v -s
```

### Ver solo tests fallidos

```bash
pytest --tb=short --failed-first
```

### Ejecutar un test específico con debug

```bash
pytest test_tools.py::TestLoadCvData::test_load_cv_data_success -v -s
```

## ⚡ **Tests Rápidos vs Completos**

### Solo tests que pasan (rápido)

```bash
pytest -k "not (test_invoke_agent_async or test_search_blog_posts_success or test_full_cv_query_flow)"
```

### Tests críticos

```bash
pytest test_main.py::TestFastAPIEndpoints::test_health_endpoint test_agents.py::TestCvAgent test_tools.py::TestLoadCvData::test_load_cv_data_success
```

## 🛠️ **Mejoras Futuras**

### 1. **Arreglar Mocks ADK**

```python
# TODO: Implementar async generator mock correcto
async def mock_adk_events():
    yield mock_event
```

### 2. **Tests de Performance**

```python
# TODO: Agregar tests de tiempo de respuesta
@pytest.mark.performance
def test_api_response_time():
    # Verificar que responde en < 2 segundos
```

### 3. **Tests de Carga**

```python
# TODO: Tests con múltiples usuarios simultáneos
@pytest.mark.load
def test_concurrent_requests():
    # Simular 100 usuarios simultáneos
```

### 4. **Tests E2E**

```python
# TODO: Tests end-to-end reales
@pytest.mark.e2e
def test_real_cv_loading():
    # Test real con CV desde web
```

### 5. **Tests de Regresión**

```python
# TODO: Guardar respuestas esperadas
@pytest.mark.regression
def test_agent_responses_unchanged():
    # Verificar que las respuestas no cambien
```

## 🎨 **Configuración Personalizada**

### pytest.ini

```ini
[tool:pytest]
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Marcadores personalizados

```python
@pytest.mark.slow
def test_heavy_operation():
    pass

@pytest.mark.integration
def test_full_flow():
    pass
```

## 📊 **Métricas de Calidad**

### Coverage deseado

- **Objetivo:** > 80% coverage total
- **Crítico:** > 95% en `tools.py` y `services.py`
- **Aceptable:** > 70% en `main.py`

### Performance benchmarks

- **Health endpoint:** < 50ms
- **CV loading:** < 3s
- **Agent response:** < 10s

## 🚨 **CI/CD Integration**

### GitHub Actions (futuro)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest --cov=assistant
```

## 💡 **Tips de Testing**

1. **Siempre mockear APIs externas** (Google, CV web)
2. **Usar fixtures para datos compartidos**
3. **Tests independientes** (no depender de orden)
4. **Nombres descriptivos** (`test_cv_loading_when_network_fails`)
5. **Arrange-Act-Assert** pattern
6. **Un assert por test** (cuando sea posible)

## 📚 **Recursos**

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [AsyncIO Testing](https://docs.python.org/3/library/unittest.html#testing-asyncio-code)
