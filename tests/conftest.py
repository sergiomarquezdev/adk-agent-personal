"""
Configuración y fixtures compartidas para tests de pytest.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def mock_cv_data():
    """Datos de CV de ejemplo para tests."""
    return {
        "name": "Sergio Márquez",
        "title": "Desarrollador Full Stack",
        "experience": [
            {
                "company": "TechCorp",
                "position": "Senior Developer",
                "years": "2020-2024",
            }
        ],
        "skills": ["Python", "JavaScript", "Docker"],
    }


@pytest.fixture
def mock_search_results():
    """Resultados de búsqueda de ejemplo para tests."""
    return [
        "https://blog.sergiomarquez.dev/python-tips",
        "https://blog.sergiomarquez.dev/fastapi-tutorial",
    ]


@pytest.fixture
def mock_googlesearch(mocker):
    """Mock para googlesearch.search - usando el path correcto."""
    return mocker.patch("assistant.tools.search")


async def mock_adk_event_generator():
    """Async generator que simula eventos del ADK runner."""
    mock_event = MagicMock()
    mock_event.is_final_response.return_value = True
    mock_event.content.parts = [MagicMock(text="Respuesta del agente")]
    yield mock_event


@pytest.fixture
def mock_adk_runner(mocker):
    """Mock para ADK Runner con async generator correcto."""
    mock_runner = mocker.patch("assistant.services._runner")
    mock_runner.run_async.return_value = mock_adk_event_generator()
    return mock_runner


@pytest.fixture
def mock_session_service(mocker):
    """Mock para el servicio de sesiones ADK."""
    mock_service = mocker.patch("assistant.services._session_service")
    mock_service.get_session = AsyncMock()
    mock_service.create_session = AsyncMock()
    return mock_service


@pytest.fixture
def test_client():
    """Cliente de test para FastAPI."""
    from main import app

    return TestClient(app)
