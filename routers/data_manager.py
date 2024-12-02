import uuid
import logging
import traceback
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from config.yaml_loader import load_config
from schemas.schemas import InputText, DocumentTypes
from fastapi import UploadFile, File, status, Request
from db.elasticsearch.operations import ElasticsearchProvider

router = APIRouter()
logger = logging.getLogger()
elastic_provider = ElasticsearchProvider()

config = load_config()

"""
upsert docs
"""

@router.post("/upsert-text",
            tags=["data manager"],
            summary="API upsert dữ liệu text")

async def upsert_labels(request: Request, input: InputText):
    request.state.trace_id = str(uuid.uuid4())
    try:  
        if not input:
            return JSONResponse(
                content = {
                    "code": status.HTTP_404_NOT_FOUND,
                    "message": f"Không tìm thấy file dữ liệu nhãn",
                    "description": [{"message": "Không tìm thấy file dữ liệu nhãn"}],
                    "trace_id": request.state.trace_id
                },
                status_code=status.HTTP_404_NOT_FOUND
            )
        text = input.text_input
        elastic_provider.upsert_from_text(text, index_name = config["elasticsearch"]["index_name"])

        return {"message": "Labels upserted successfully from file"}

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


@router.post("/upsert-file",
            tags=["data manager"],
            summary="API upsert dữ liệu nhãn")

async def upsert_labels_by_file(request: Request, doc_type: str, file_path: UploadFile = File(...)):
    request.state.trace_id = str(uuid.uuid4())
   
    try:
        file_bytes = await file_path.read()
        
        if not file_bytes:
            return JSONResponse(
                content = {
                    "code": status.HTTP_404_NOT_FOUND,
                    "message": f"Không tìm thấy file dữ liệu nhãn",
                    "description": [{"message": "Không tìm thấy file dữ liệu nhãn"}],
                    "trace_id": request.state.trace_id
                },
                status_code=status.HTTP_404_NOT_FOUND
            )
            
        elastic_provider.upsert_from_files(file_bytes, doc_type, index_name=config["elasticsearch"]["index_name"])

        return {"message": "Labels upserted successfully from file"}

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

@router.delete("/delete-index",
            tags=["data manager"],
            summary="API xoá dữ liệu nhãn")

async def delete_index(request: Request, index_name: str):
    request.state.trace_id = str(uuid.uuid4())
    try:
        elastic_provider.delete_index(index_name)
        return {"message": f"labels {index_name} deleted successfully"}

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