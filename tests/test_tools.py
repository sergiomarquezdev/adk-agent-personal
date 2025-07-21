"""
Tests para el módulo assistant.tools
"""

import json
from unittest.mock import MagicMock

from requests.exceptions import ConnectionError, Timeout

from assistant.tools import load_cv_data, search_blog_posts


class TestLoadCvData:
    """Tests para la función load_cv_data."""

    def test_load_cv_data_success(self, mock_requests_get, mock_cv_data):
        """Test de carga exitosa del CV desde la web."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = mock_cv_data
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        # Act
        result = load_cv_data()

        # Assert
        mock_requests_get.assert_called_once_with(
            "https://cv.sergiomarquez.dev/cv.json", timeout=10
        )
        assert "Sergio Márquez" in result
        assert "Desarrollador Full Stack" in result

        # Verificar que es JSON válido
        parsed_result = json.loads(result)
        assert parsed_result["name"] == "Sergio Márquez"

    def test_load_cv_data_request_exception(self, mock_requests_get, mocker):
        """Test cuando falla la petición HTTP."""
        # Arrange
        mock_requests_get.side_effect = ConnectionError("Error de conexión")
        mocker.patch("builtins.open", side_effect=FileNotFoundError())

        # Act
        result = load_cv_data()

        # Assert
        parsed_result = json.loads(result)
        assert parsed_result["name"] == "Sergio Márquez"
        assert "CV no disponible temporalmente" in parsed_result["note"]

    def test_load_cv_data_json_decode_error(self, mock_requests_get):
        """Test cuando la respuesta no es JSON válido."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        # Act
        result = load_cv_data()

        # Assert
        parsed_result = json.loads(result)
        assert parsed_result["name"] == "Sergio Márquez"
        assert "error" in parsed_result

    def test_load_cv_data_fallback_to_local(
        self, mock_requests_get, mocker, mock_cv_data
    ):
        """Test de fallback a archivo local cuando falla la descarga."""
        # Arrange
        mock_requests_get.side_effect = Timeout("Timeout")
        mock_file = mocker.mock_open(read_data=json.dumps(mock_cv_data))
        mocker.patch("builtins.open", mock_file)

        # Act
        result = load_cv_data()

        # Assert
        parsed_result = json.loads(result)
        assert parsed_result["name"] == "Sergio Márquez"


class TestSearchBlogPosts:
    """Tests para la función search_blog_posts."""

    def test_search_blog_posts_function_exists(self):
        """Test básico que verifica que la función existe y es callable."""
        # Assert
        assert callable(search_blog_posts)

    def test_search_blog_posts_returns_string(self):
        """Test que verifica que la función retorna un string."""
        # Act
        result = search_blog_posts("python")

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0

    def test_search_blog_posts_handles_empty_query(self):
        """Test que verifica el manejo de queries vacías."""
        # Act
        result = search_blog_posts("")

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0

    def test_search_blog_posts_includes_query_in_response(self):
        """Test que verifica que el query aparece en la respuesta."""
        # Arrange
        query = "test_query_123"

        # Act
        result = search_blog_posts(query)

        # Assert
        assert query in result
