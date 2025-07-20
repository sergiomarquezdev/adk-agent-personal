"""
Unit tests for the FastAPI application's API endpoints.
"""

from unittest.mock import AsyncMock, patch, ANY

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def mock_invoke_agent():
    """
    Pytest fixture to mock invoke_agent_async.
    This isolates the API layer from the agent's internal logic.
    """
    with patch("main.invoke_agent_async", new_callable=AsyncMock) as mock:
        # Define a default return value for the mock, matching the expected tuple
        mock.return_value = ("Esta es una respuesta simulada.", "mock_session_id")
        yield mock


def test_invoke_endpoint_success(mock_invoke_agent):
    """
    Tests the /api/invoke endpoint with a valid message.
    Verifies that the endpoint calls the agent and returns its response.
    """
    # Arrange
    user_message = "Hola, ¿quién eres?"

    # Act
    response = client.post("/api/invoke", json={"message": user_message})

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["response"] == "Esta es una respuesta simulada."
    assert response_data["session_id"] == "mock_session_id"

    # Verify that the mocked agent function was called correctly
    mock_invoke_agent.assert_called_once_with(
        message=user_message, session_id=None, user_id=ANY
    )


def test_invoke_endpoint_agent_error(mock_invoke_agent):
    """
    Tests how the endpoint handles an exception from the agent.
    It should return a 500 Internal Server Error.
    """
    # Arrange
    user_message = "Provocar un error"
    error_message = "Error simulado en el agente"
    mock_invoke_agent.side_effect = Exception(error_message)

    # Act
    response = client.post("/api/invoke", json={"message": user_message})

    # Assert
    assert response.status_code == 500
    response_data = response.json()
    assert "detail" in response_data
    assert error_message in response_data["detail"]


def test_invoke_endpoint_invalid_payload():
    """
    Tests the /api/invoke endpoint with an invalid payload (wrong field name).
    FastAPI should return a 422 Unprocessable Entity error.
    """
    response = client.post("/api/invoke", json={"not_a_message": "Hola"})
    assert response.status_code == 422


def test_invoke_endpoint_missing_message():
    """
    Tests the /api/invoke endpoint with a missing message field.
    The custom validation should return a 400 Bad Request.
    """
    response = client.post("/api/invoke", json={"message": ""})
    assert response.status_code == 400


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
