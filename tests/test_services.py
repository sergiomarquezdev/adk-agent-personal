"""
Tests para el módulo assistant.services
"""

import pytest

from assistant.services import invoke_agent_async


class TestServicesModule:
    """Tests básicos para el módulo de servicios."""

    def test_invoke_agent_async_function_exists(self):
        """Test que verifica que la función invoke_agent_async existe."""
        # Assert
        assert callable(invoke_agent_async)

    def test_invoke_agent_async_is_async(self):
        """Test que verifica que invoke_agent_async es una función asíncrona."""
        import asyncio

        # Assert
        assert asyncio.iscoroutinefunction(invoke_agent_async)

    def test_module_imports_successfully(self):
        """Test que verifica que el módulo se puede importar sin errores."""
        # Act & Assert
        try:
            import assistant.services

            assert True
        except ImportError:
            pytest.fail("No se pudo importar assistant.services")

    def test_module_has_required_components(self):
        """Test que verifica que el módulo tiene los componentes necesarios."""
        import assistant.services as services

        # Assert
        assert hasattr(services, "invoke_agent_async")
        assert hasattr(services, "_session_service")
        assert hasattr(services, "_runner")
        assert hasattr(services, "_APP_NAME")

    def test_app_name_is_string(self):
        """Test que verifica que APP_NAME es un string válido."""
        from assistant.services import _APP_NAME

        # Assert
        assert isinstance(_APP_NAME, str)
        assert len(_APP_NAME) > 0
        assert _APP_NAME == "assistant_app"


class TestServicesConfiguration:
    """Tests para la configuración del módulo de servicios."""

    def test_session_service_exists(self):
        """Test que verifica que el servicio de sesiones existe."""
        from assistant.services import _session_service

        # Assert
        assert _session_service is not None

    def test_runner_exists(self):
        """Test que verifica que el runner existe."""
        from assistant.services import _runner

        # Assert
        assert _runner is not None

    def test_root_agent_imported(self):
        """Test que verifica que el root_agent se importa correctamente."""
        try:
            from assistant.services import _runner

            # Si llegamos aquí, significa que root_agent se importó correctamente
            # porque _runner se inicializa con root_agent
            assert True
        except ImportError as e:
            pytest.fail(f"Error importando root_agent: {e}")


class TestTypesAndImports:
    """Tests para los tipos e imports del módulo."""

    def test_types_import(self):
        """Test que verifica que types se importa correctamente."""
        try:
            from google.genai import types

            assert types is not None
        except ImportError:
            pytest.skip("google.genai.types no disponible en entorno de test")

    def test_function_signature(self):
        """Test que verifica la signatura de invoke_agent_async."""
        import inspect

        # Act
        sig = inspect.signature(invoke_agent_async)
        params = list(sig.parameters.keys())

        # Assert
        assert "message" in params
        assert "session_id" in params
        assert "user_id" in params
        assert len(params) == 3
