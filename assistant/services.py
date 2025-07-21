# services.py
# Contiene la lógica de negocio para invocar al agente y gestionar sesiones.

import uuid
from typing import Optional, Tuple

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from assistant.agents import root_agent

_session_service = InMemorySessionService()
_APP_NAME = "assistant_app"
_runner = Runner(agent=root_agent, app_name=_APP_NAME, session_service=_session_service)


async def invoke_agent_async(
    message: str, session_id: Optional[str], user_id: str
) -> Tuple[str, str]:
    """
    Invoca al agente orquestador, gestionando la sesión del usuario.
    Crea una nueva sesión si no se proporciona una válida.
    """
    # Valida la sesión existente o asigna None para crear una nueva.
    if session_id:
        try:
            await _session_service.get_session(
                app_name=_APP_NAME, user_id=user_id, session_id=session_id
            )
        except KeyError:
            print(
                f"WARN: session_id '{session_id}' no encontrado. Se creará uno nuevo."
            )
            session_id = None

    # Crea una nueva sesión si es necesario.
    if not session_id:
        session_id = f"session_{uuid.uuid4().hex}"
        await _session_service.create_session(
            app_name=_APP_NAME, user_id=user_id, session_id=session_id
        )

    # Ejecuta el agente y procesa la respuesta.
    content = types.Content(role="user", parts=[types.Part(text=message)])
    final_response_text: str = "El agente no produjo una respuesta final."

    async for event in _runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = event.content.parts[0].text
            if response_text is not None:
                final_response_text = response_text
            break

    return final_response_text, session_id
