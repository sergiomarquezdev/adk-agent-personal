import os

import uvicorn
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

try:
    from personal_agent.agent import invoke_agent_async
except ImportError:
    print("Error: No se pudo encontrar 'invoke_agent_async' en el fichero 'agent.py'.")
    print(
        "Asegúrate de que el fichero existe y la función está definida correctamente."
    )
    exit()


class InvokeRequest(BaseModel):
    message: str


# Crear el router con prefijo
api_router = APIRouter(prefix="/api")


@api_router.post("/invoke")
async def invoke_agent_endpoint(request: InvokeRequest):
    """
    Recibe un mensaje del usuario, lo pasa al agente y devuelve la respuesta.
    """
    try:
        response = await invoke_agent_async(request.message)
        return {"response": response}
    except Exception as e:
        return {"error": f"Ha ocurrido un error en el agente: {e}"}


app = FastAPI(
    title="API del Agente Personal de Sergio",
    description="Un servidor para interactuar con el agente personal basado en ADK y Gemini.",
    version="1.0.0",
)


# Incluir el router en la app
app.include_router(api_router)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
