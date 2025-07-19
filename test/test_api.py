"""
Unit tests for the FastAPI application's API endpoints.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def override_invoke_agent():
    """
    Pytest fixture to automatically mock invoke_agent_async for all tests in this file.
    This isolates the API layer from the agent's internal logic.
    """
    with patch(
        "main.invoke_agent_async", new_callable=AsyncMock
    ) as mock_invoke_agent:
        # Define a default return value for the mock
        mock_invoke_agent.return_value = "Esta es una respuesta simulada por el agente."
        yield mock_invoke_agent


def test_invoke_endpoint_success(override_invoke_agent):
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
    assert "response" in response_data
    assert response_data["response"] == "Esta es una respuesta simulada por el agente."

    # Verify that the mocked agent function was called correctly
    override_invoke_agent.assert_called_once_with(user_message)


def test_invoke_endpoint_agent_error(override_invoke_agent):
    """
    Tests how the endpoint handles an exception from the agent.
    """
    # Arrange
    user_message = "Provocar un error"
    error_message = "Error simulado en el agente"
    override_invoke_agent.side_effect = Exception(error_message)

    # Act
    response = client.post("/api/invoke", json={"message": user_message})

    # Assert
    assert response.status_code == 200  # The endpoint itself handles the error gracefully
    response_data = response.json()
    assert "error" in response_data
    assert error_message in response_data["error"]


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
    FastAPI should return a 422 Unprocessable Entity error.
    """
    response = client.post("/api/invoke", json={})
    assert response.status_code == 422


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