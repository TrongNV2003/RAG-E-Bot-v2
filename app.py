
import logging
import uvicorn
from fastapi import FastAPI
from db.elasticsearch.operations import ElasticsearchProvider

from routers.chatbot import router as chatbot_router
from routers.healthcheck import router as healthcheck_router
from routers.data_manager import router as data_manager_router

logger = logging.getLogger()
logger = logging.getLogger("app")

app = FastAPI(
    title="RAG-E Bot",
    version="1.0.0",
    )

elastic_provider = ElasticsearchProvider()

app.include_router(data_manager_router)
app.include_router(chatbot_router)
app.include_router(healthcheck_router)


if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=2206)