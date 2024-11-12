import uuid
import logging
import traceback
from fastapi import status, Request
from fastapi.routing import APIRouter
from schemas.schemas import InputQuery, InputParams
from fastapi.responses import JSONResponse
from llm_models.operations import LlmModel
from db.elasticsearch.operations import ElasticsearchProvider

model = LlmModel()
router = APIRouter()
elastic_provider = ElasticsearchProvider()

logger = logging.getLogger("factoryAI")


@router.post("/chatbot-text-query",
            tags=["Bot RAG"],
            summary="API call chatbot query")

async def chatbot(input: InputQuery, params: InputParams, request: Request):
    request.state.trace_id = str(uuid.uuid4())
    try:
        query = input.text_input
        temperature = params.temperature
        
        requests = model.text_query(query, temperature)
        return {"Question": query, 
                "Answer": requests}

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(tb)
        return JSONResponse(
            content = {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"An unexpected error occurred during classification process.",
                "description": [{"message": tb}],
                "trace_id": request.state.trace_id
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/chatbot-retrieval-query",
            tags=["Bot RAG"],
            summary="API call chatbot retrieval")

async def chatbot(input: InputQuery, params: InputParams, request: Request):
    request.state.trace_id = str(uuid.uuid4())
    try:
        query = input.text_input
        
        temperature = params.temperature
        threshold = params.threshold
        
        documents, requests = model.retrieve_query(query, temperature, threshold)
        return {"Documents": documents,
                "Question": query, 
                "Answer": requests}

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(tb)
        return JSONResponse(
            content = {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"An unexpected error occurred during classification process.",
                "description": [{"message": tb}],
                "trace_id": request.state.trace_id
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )