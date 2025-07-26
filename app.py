import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import logging
import uvicorn
from fastapi import FastAPI

from rag.db.elasticsearch.operations import ElasticsearchProvider
from rag.routers.queries import router as chatbot_router
from rag.routers.upsert import router as data_manager_router
from rag.routers.healthcheck import router as healthcheck_router

logger = logging.getLogger()
logger = logging.getLogger("app")

app = FastAPI(
    title="RAG-E Ver2",
    version="2.0.0",
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