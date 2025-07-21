"""
Tests de integración para el sistema completo.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


class TestBasicIntegration:
    """Tests de integración básicos."""

    def setup_method(self):
        """Setup para cada test."""
        self.client = TestClient(app)

    def test_health_check_availability(self):
        """Test que el health check esté disponible."""
        # Act
        response = self.client.get("/api/health")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}

    def test_api_endpoints_return_json(self):
        """Test que los endpoints principales retornan JSON."""
        # Act
        health_response = self.client.get("/api/health")

        # Assert
        assert "application/json" in health_response.headers["content-type"]

    def test_invalid_endpoint_returns_404(self):
        """Test que endpoints inexistentes retornan 404."""
        # Act
        response = self.client.get("/api/nonexistent")

        # Assert
        assert response.status_code == 404

    def test_invoke_endpoint_exists(self):
        """Test que el endpoint de invoke existe (aunque falle por datos)."""
        # Act
        response = self.client.post("/api/invoke", json={})

        # Assert
        # El endpoint existe (no es 404), aunque falle por validación
        assert response.status_code != 404

    def test_app_configuration(self):
        """Test de configuración básica de la aplicación."""
        # Assert
        assert app.title == "API del Asistente Personal de Sergio"
        assert app.version == "2.0.0"
        assert "multi-agente" in app.description


class TestAPIDocumentation:
    """Tests para la documentación automática de la API."""

    def setup_method(self):
        """Setup para cada test."""
        self.client = TestClient(app)

    def test_openapi_schema_available(self):
        """Test que el schema OpenAPI esté disponible."""
        # Act
        response = self.client.get("/openapi.json")

        # Assert
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "API del Asistente Personal de Sergio"

    def test_docs_endpoint_available(self):
        """Test que la documentación interactiva esté disponible."""
        # Act
        response = self.client.get("/docs")

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_endpoint_available(self):
        """Test que ReDoc esté disponible."""
        # Act
        response = self.client.get("/redoc")

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestSystemImports:
    """Tests para verificar que todos los módulos se importan correctamente."""

    def test_main_module_imports(self):
        """Test que el módulo main se importa sin errores."""
        try:
            import main

            assert main.app is not None
        except ImportError as e:
            pytest.fail(f"Error importando main: {e}")

    def test_assistant_modules_import(self):
        """Test que los módulos de assistant se importan correctamente."""
        try:
            import assistant.agents
            import assistant.services
            import assistant.tools

            assert True
        except ImportError as e:
            pytest.fail(f"Error importando módulos assistant: {e}")

    def test_agents_configuration_loads(self):
        """Test que la configuración de agentes se carga sin errores."""
        try:
            from assistant.agents import blog_agent, cv_agent, root_agent

            assert cv_agent is not None
            assert blog_agent is not None
            assert root_agent is not None
        except Exception as e:
            pytest.fail(f"Error cargando configuración de agentes: {e}")


class TestErrorHandling:
    """Tests para el manejo de errores del sistema."""

    def setup_method(self):
        """Setup para cada test."""
        self.client = TestClient(app)

    def test_malformed_json_handling(self):
        """Test del manejo de JSON malformado."""
        # Act
        response = self.client.post(
            "/api/invoke",
            data="{ invalid json",
            headers={"Content-Type": "application/json"},
        )

        # Assert
        assert response.status_code == 422

    def test_missing_content_type(self):
        """Test cuando falta el Content-Type."""
        # Act
        response = self.client.post("/api/invoke", data="test")

        # Assert
        assert response.status_code == 422

    def test_wrong_http_method(self):
        """Test con método HTTP incorrecto."""
        # Act
        response = self.client.get("/api/invoke")

        # Assert
        assert response.status_code == 405  # Method not allowed
