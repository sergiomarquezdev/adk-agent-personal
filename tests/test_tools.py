"""
Tests para el módulo assistant.tools
"""

import json

from assistant.tools import load_cv_data, search_blog_posts


class TestLoadCvData:
    """Tests para la función load_cv_data."""

    def test_load_cv_data_success(self, mocker, mock_cv_data):
        """Test de carga exitosa del CV desde archivo local."""
        # Arrange
        mock_file = mocker.mock_open(read_data=json.dumps(mock_cv_data))
        mocker.patch("builtins.open", mock_file)

        # Act
        result = load_cv_data()

        # Assert
        mock_file.assert_called_once()
        assert "Sergio Márquez" in result
        assert "Desarrollador Full Stack" in result

        # Verificar que es JSON válido
        parsed_result = json.loads(result)
        assert parsed_result["name"] == "Sergio Márquez"

    def test_load_cv_data_file_not_found(self, mocker):
        """Test cuando no se encuentra el archivo CV local."""
        # Arrange
        mocker.patch("builtins.open", side_effect=FileNotFoundError())

        # Act
        result = load_cv_data()

        # Assert
        parsed_result = json.loads(result)
        assert parsed_result["name"] == "Sergio Márquez"
        assert "CV no disponible" in parsed_result["note"]
        assert parsed_result["title"] == "Desarrollador IA/ML"

    def test_load_cv_data_json_decode_error(self, mocker):
        """Test cuando el archivo CV contiene JSON inválido."""
        # Arrange
        mock_file = mocker.mock_open(read_data="invalid json content")
        mocker.patch("builtins.open", mock_file)

        # Act
        result = load_cv_data()

        # Assert
        parsed_result = json.loads(result)
        assert parsed_result["name"] == "Sergio Márquez"
        assert "error" in parsed_result

    def test_load_cv_data_path_construction(self, mocker, mock_cv_data):
        """Test que verifica la construcción correcta del path del archivo."""
        # Arrange
        mock_file = mocker.mock_open(read_data=json.dumps(mock_cv_data))
        mock_open = mocker.patch("builtins.open", mock_file)

        # Act
        load_cv_data()

        # Assert
        # Verificar que se construye el path correcto
        call_args = mock_open.call_args[0][0]
        assert "nginx" in call_args
        assert "cv.json" in call_args


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
