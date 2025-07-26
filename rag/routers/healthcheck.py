import logging
from fastapi import Response, status
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from rag.schemas.schemas import HealthCheckResponse

router = APIRouter(tags=["Health Check"])
logger = logging.getLogger("factoryAI")

@router.get("/healthz",
            responses={
                200: {
                  "model": HealthCheckResponse,
                    "description": "Agent is available"
                },
                500: {
                    "model": HealthCheckResponse,
                    "content": {
                        "application/json": {
                            "example": {
                                "message": "Internal Server Error, Agent is not initialized",
                            }
                        }
                    }
                }
            })
async def health_check(response: Response):
    return JSONResponse(content={"message": "Hello World! 👍🏻"}, status_code=status.HTTP_200_OK)