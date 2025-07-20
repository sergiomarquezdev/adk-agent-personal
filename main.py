import uuid
from typing import Optional

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response
from pydantic import BaseModel

from personal_agent.agent import invoke_agent_async


class InvokeRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class InvokeResponse(BaseModel):
    response: str
    session_id: str


USER_COOKIE_NAME = "personal_agent_user_id"


async def get_user_id(request: Request, response: Response) -> str:
    user_id = request.cookies.get(USER_COOKIE_NAME)
    if not user_id:
        print("DEBUG: No se encontró cookie de usuario. Creando una nueva.")
        user_id = f"user_{uuid.uuid4().hex}"
        response.set_cookie(
            key=USER_COOKIE_NAME,
            value=user_id,
            max_age=60 * 60 * 24 * 365,  # 1 año
            httponly=True,
        )
    else:
        print(f"DEBUG: Usuario reconocido con ID: {user_id}")
    return user_id


api_router = APIRouter(prefix="/api")


@api_router.post("/invoke", response_model=InvokeResponse)
async def invoke_agent_endpoint(
    request: InvokeRequest, user_id: str = Depends(get_user_id)
):
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


app = FastAPI(
    title="API del Agente Personal de Sergio",
    description="Un servidor para interactuar con el agente personal basado en ADK y Gemini.",
    version="1.2.0",
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
