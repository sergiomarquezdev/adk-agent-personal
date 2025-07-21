"""
Tests para el módulo main.py (endpoints de FastAPI)
"""

from fastapi.testclient import TestClient

from main import app


class TestFastAPIEndpoints:
    """Tests para los endpoints de FastAPI."""

    def setup_method(self):
        """Setup para cada test."""
        self.client = TestClient(app)

    def test_health_endpoint(self):
        """Test del endpoint de health check."""
        # Act
        response = self.client.get("/api/health")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}

    def test_invoke_endpoint_empty_message(self):
        """Test del endpoint invoke con mensaje vacío."""
        # Arrange
        payload = {"message": "", "session_id": "session_123"}

        # Act
        response = self.client.post("/api/invoke", json=payload)

        # Assert
        assert response.status_code == 400
        assert "El mensaje no puede estar vacío" in response.json()["detail"]

    def test_invoke_endpoint_invalid_json(self):
        """Test con JSON inválido."""
        # Act
        response = self.client.post(
            "/api/invoke",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )

        # Assert
        assert response.status_code == 422

    def test_app_title_and_description(self):
        """Test que verifica la configuración de la aplicación."""
        # Assert
        assert app.title == "API del Asistente Personal de Sergio"
        assert "sistema multi-agente" in app.description
        assert app.version == "2.0.0"


class TestInvokeRequestModel:
    """Tests para el modelo InvokeRequest."""

    def test_invoke_request_with_session_id(self):
        """Test de creación de InvokeRequest con session_id."""
        from main import InvokeRequest

        # Act
        request = InvokeRequest(message="Test message", session_id="session_123")

        # Assert
        assert request.message == "Test message"
        assert request.session_id == "session_123"

    def test_invoke_request_without_session_id(self):
        """Test de creación de InvokeRequest sin session_id."""
        from main import InvokeRequest

        # Act
        request = InvokeRequest(message="Test message")

        # Assert
        assert request.message == "Test message"
        assert request.session_id is None


class TestInvokeResponseModel:
    """Tests para el modelo InvokeResponse."""

    def test_invoke_response_creation(self):
        """Test de creación de InvokeResponse."""
        from main import InvokeResponse

        # Act
        response = InvokeResponse(response="Agent response", session_id="session_456")

        # Assert
        assert response.response == "Agent response"
        assert response.session_id == "session_456"


class TestAPIConfiguration:
    """Tests para la configuración de la API."""

    def test_api_router_prefix(self):
        """Test que verifica que las rutas tienen el prefijo correcto."""
        # Arrange
        client = TestClient(app)

        # Act & Assert
        # Health endpoint debe estar en /api/health
        response = client.get("/api/health")
        assert response.status_code == 200

        # Endpoint raíz no debe existir
        response = client.get("/health")
        assert response.status_code == 404

    def test_openapi_schema_generation(self):
        """Test que verifica que el schema OpenAPI se genera correctamente."""
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/openapi.json")

        # Assert
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "API del Asistente Personal de Sergio"
