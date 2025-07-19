import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_invoke_endpoint_success():
    """
    Tests the /invoke endpoint with a valid message.
    """
    response = client.post("/invoke", json={"message": "Hola, ¿quién eres?"})
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert isinstance(response_data["response"], str)
    assert len(response_data["response"]) > 0

def test_invoke_endpoint_invalid_payload():
    """
    Tests the /invoke endpoint with an invalid payload.
    """
    response = client.post("/invoke", json={"not_a_message": "Hola"})
    assert response.status_code == 422  # Unprocessable Entity
