"""
Tests para el módulo assistant.agents
"""

import pytest

from assistant.agents import blog_agent, cv_agent, root_agent


class TestCvAgent:
    """Tests para el agente CV_Expert."""

    def test_cv_agent_configuration(self):
        """Test de configuración del CV agent."""
        # Assert
        assert cv_agent.name == "CV_Expert"
        assert "especialista" in cv_agent.description.lower()
        assert cv_agent.model == "gemini-1.5-flash"
        assert "Sergio Márquez" in cv_agent.instruction
        assert cv_agent.tools == []

    def test_cv_agent_instruction_contains_cv_data(self):
        """Test que la instrucción del CV agent contiene datos del CV."""
        # Assert
        assert "CV Data:" in cv_agent.instruction
        assert "Sergio Márquez" in cv_agent.instruction
        assert "primera persona" in cv_agent.instruction.lower()


class TestBlogAgent:
    """Tests para el agente Blog_Expert."""

    def test_blog_agent_configuration(self):
        """Test de configuración del Blog agent."""
        # Assert
        assert blog_agent.name == "Blog_Expert"
        assert "especialista" in blog_agent.description.lower()
        assert blog_agent.model == "gemini-1.5-flash"
        assert "search_blog_posts" in blog_agent.instruction
        assert len(blog_agent.tools) == 1

    def test_blog_agent_has_search_tool(self):
        """Test que el Blog agent tiene la herramienta de búsqueda."""
        from assistant.tools import search_blog_posts

        # Assert
        assert search_blog_posts in blog_agent.tools


class TestRootAgent:
    """Tests para el agente orquestador root_agent."""

    def test_root_agent_configuration(self):
        """Test de configuración del root agent."""
        # Assert
        assert root_agent.name == "Personal_Orchestrator"
        assert "coordinador" in root_agent.description.lower()
        assert root_agent.model == "gemini-1.5-flash"
        assert "delegación" in root_agent.instruction.lower()
        assert len(root_agent.sub_agents) == 2

    def test_root_agent_has_sub_agents(self):
        """Test que el root agent tiene los sub-agentes correctos."""
        # Assert
        assert cv_agent in root_agent.sub_agents
        assert blog_agent in root_agent.sub_agents

    def test_root_agent_delegation_logic(self):
        """Test que la instrucción del root agent contiene lógica de delegación."""
        instruction = root_agent.instruction.lower()

        # Assert
        assert "cv_expert" in instruction
        assert "blog_expert" in instruction
        assert "experiencia profesional" in instruction
        assert "artículos" in instruction or "blog" in instruction


class TestAgentsModule:
    """Tests generales del módulo agents."""

    def test_all_agents_have_required_attributes(self):
        """Test que todos los agentes tienen los atributos requeridos."""
        agents = [cv_agent, blog_agent, root_agent]

        for agent in agents:
            # Assert
            assert hasattr(agent, "name")
            assert hasattr(agent, "description")
            assert hasattr(agent, "model")
            assert hasattr(agent, "instruction")
            assert agent.name is not None
            assert agent.description is not None
            assert agent.model == "gemini-1.5-flash"
            assert agent.instruction is not None

    def test_agents_have_unique_names(self):
        """Test que todos los agentes tienen nombres únicos."""
        agents = [cv_agent, blog_agent, root_agent]
        names = [agent.name for agent in agents]

        # Assert
        assert len(names) == len(set(names))  # Todos los nombres son únicos

    def test_cv_agent_tools_empty(self):
        """Test que el CV agent no tiene herramientas."""
        # Assert
        assert cv_agent.tools == []

    def test_blog_agent_has_tools(self):
        """Test que el Blog agent tiene herramientas."""
        # Assert
        assert len(blog_agent.tools) > 0
        assert callable(blog_agent.tools[0])

    def test_root_agent_has_no_tools_but_has_sub_agents(self):
        """Test que el root agent no tiene tools pero sí sub_agents."""
        # Assert
        assert not hasattr(root_agent, "tools") or not root_agent.tools
        assert hasattr(root_agent, "sub_agents")
        assert len(root_agent.sub_agents) > 0

    def test_module_imports_successfully(self):
        """Test que el módulo agents se importa correctamente."""
        try:
            import assistant.agents

            assert True
        except ImportError as e:
            pytest.fail(f"Error importando assistant.agents: {e}")


class TestAgentInstructions:
    """Tests específicos para las instrucciones de los agentes."""

    def test_cv_agent_instruction_security(self):
        """Test que la instrucción del CV agent enfatiza seguridad de datos."""
        instruction = cv_agent.instruction.lower()

        # Assert
        assert "exclusivamente" in instruction
        assert "no inventes" in instruction or "no interpretes" in instruction

    def test_blog_agent_instruction_focus(self):
        """Test que la instrucción del Blog agent está enfocada en búsqueda."""
        instruction = blog_agent.instruction.lower()

        # Assert
        assert "search_blog_posts" in instruction
        assert "herramienta" in instruction
        assert "únicamente" in instruction or "exclusiva" in instruction

    def test_root_agent_instruction_delegation_rules(self):
        """Test que la instrucción del root agent contiene reglas claras."""
        instruction = root_agent.instruction.lower()

        # Assert
        assert "delega" in instruction or "delegación" in instruction
        assert "cv" in instruction
        assert "blog" in instruction
        assert "nunca reveles" in instruction or "confidencialidad" in instruction
