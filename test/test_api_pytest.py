from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_invoke_endpoint_success():
    """
    Tests the /api/invoke endpoint with a valid message.
    """
    response = client.post("/api/invoke", json={"message": "Hola, ¿quién eres?"})
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert isinstance(response_data["response"], str)
    assert len(response_data["response"]) > 0


def test_invoke_endpoint_invalid_payload():
    """
    Tests the /api/invoke endpoint with an invalid payload.
    """
    response = client.post("/api/invoke", json={"not_a_message": "Hola"})
    assert response.status_code == 422  # Unprocessable Entity


def test_invoke_endpoint_empty_message():
    """
    Tests the /api/invoke endpoint with an empty message.
    """
    response = client.post("/api/invoke", json={"message": ""})
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data


def test_invoke_endpoint_missing_message():
    """
    Tests the /api/invoke endpoint with missing message field.
    """
    response = client.post("/api/invoke", json={})
    assert response.status_code == 422  # Unprocessable Entity


def test_invoke_endpoint_with_cv_query():
    """
    Tests the /api/invoke endpoint with a query about CV information.
    """
    response = client.post(
        "/api/invoke", json={"message": "¿Cuál es tu experiencia laboral?"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert isinstance(response_data["response"], str)
    assert len(response_data["response"]) > 0


def test_invoke_endpoint_with_skills_query():
    """
    Tests the /api/invoke endpoint with a query about skills.
    """
    response = client.post(
        "/api/invoke", json={"message": "¿Qué habilidades técnicas tienes?"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert isinstance(response_data["response"], str)
    assert len(response_data["response"]) > 0


def test_root_endpoint():
    """
    Tests the root endpoint to ensure FastAPI is working.
    """
    response = client.get("/")
    assert response.status_code == 404  # No root endpoint defined


def test_docs_endpoint():
    """
    Tests that the API documentation is accessible.
    """
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_endpoint():
    """
    Tests that the OpenAPI schema is accessible.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200
