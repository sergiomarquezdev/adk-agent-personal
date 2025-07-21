# main.py
# Define la API web con FastAPI y gestiona las peticiones/respuestas HTTP.

import uuid
from typing import Optional

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response
from pydantic import BaseModel

# Importamos la lógica de invocación desde la nueva capa de servicios.
from assistant.services import invoke_agent_async

# --- Modelos de Datos y Gestión de Cookies ---


class InvokeRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class InvokeResponse(BaseModel):
    response: str
    session_id: str


USER_COOKIE_NAME = "assistant_user_id"


async def get_user_id(request: Request, response: Response) -> str:
    """Obtiene el ID de usuario de la cookie o crea uno nuevo si no existe."""
    user_id = request.cookies.get(USER_COOKIE_NAME)
    if not user_id:
        user_id = f"user_{uuid.uuid4().hex}"
        response.set_cookie(
            key=USER_COOKIE_NAME,
            value=user_id,
            max_age=60 * 60 * 24 * 365,  # 1 año
            httponly=True,
        )
    return user_id


# --- Definición de Rutas de la API ---

api_router = APIRouter(prefix="/api")


@api_router.post("/invoke", response_model=InvokeResponse)
async def invoke_agent_endpoint(
    request: InvokeRequest, user_id: str = Depends(get_user_id)
):
    """Endpoint principal para interactuar con el agente."""
    if not request.message:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")

    try:
        agent_response, session_id = await invoke_agent_async(
            message=request.message, session_id=request.session_id, user_id=user_id
        )
        return InvokeResponse(response=agent_response, session_id=session_id)
    except Exception as e:
        print(f"Error en el endpoint del agente: {e}")
        raise HTTPException(
            status_code=500, detail=f"Ha ocurrido un error en el agente: {e}"
        )


@api_router.get("/health")
async def health_check():
    """Endpoint de health check para verificar que el servicio está activo."""
    return {"status": "OK"}


# --- Creación de la Aplicación FastAPI ---

app = FastAPI(
    title="API del Asistente Personal de Sergio",
    description="Un servidor para interactuar con un sistema multi-agente basado en ADK.",
    version="2.0.0",
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
