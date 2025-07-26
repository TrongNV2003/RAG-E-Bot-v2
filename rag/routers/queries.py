import uuid
import logging
import traceback
from fastapi import status, Request
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from rag.models.llm_model import LlmModel
from rag.db.elasticsearch.operations import ElasticsearchProvider
from rag.schemas.schemas import InputQuery, InputParams, ChatHistory

model = LlmModel()
router = APIRouter()
elastic_provider = ElasticsearchProvider()

logger = logging.getLogger("factoryAI")

@router.post("/chatbot-retrieval-query",
            tags=["RAGBOT"],
            summary="API call chatbot retrieval")

async def chatbot(input: InputQuery, params: InputParams, history: ChatHistory, request: Request):
    request.state.trace_id = str(uuid.uuid4())
    try:
        query = input.text_input
        
        top_k = params.top_k
        is_retrieval = params.is_retrieval
        history = history.chat_history

        documents, response = model.run(query, top_k, is_retrieval=is_retrieval, chat_history=history)
        return {
            "Documents": documents,
            "Question": query, 
            "Answer": response,
            "History": history
        }

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