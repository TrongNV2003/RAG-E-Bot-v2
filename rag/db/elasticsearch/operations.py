import uuid
import pymupdf
from enum import Enum
from typing import Any, List
from pydantic import BaseModel
from elasticsearch.helpers import bulk
from fastapi.responses import JSONResponse
from langchain.text_splitter import RecursiveCharacterTextSplitter

from rag.models.embed_model import EmbeddingModel
from rag.config.setting import elasticsearch_config
from rag.db.elasticsearch.connector import connect_db


class ElasticsearchProvider:
    def __init__(self) -> None:
        self.client = connect_db()
        self.model = EmbeddingModel()
    
    def upsert_from_text(self, documents: str, index_name: str) -> dict:
        chunks = self._chunking(documents)
        actions = []
        for i, chunk in enumerate(chunks):
            embedding = self.model.embedding(chunk)
            doc = {
                "_op_type": "index",
                "_index": index_name,
                "_id": uuid.uuid4().hex,
                "_source": {
                    "text": chunk,
                    "embedding": embedding
                }
            }
            actions.append(doc)
        
        if actions:
            success, failed = bulk(self.client, actions)
            return {"success": success, "failed": failed}
        return {"success": 0, "failed": 0}

    def upsert_from_files(self, pdf_file: str, index_name: str) -> dict:
        pdf_content = self._process_pdf_file(pdf_file)
        pdf_content = self._clean_text(pdf_content)
        upsert_file = self.upsert_from_text(pdf_content, index_name)
        return upsert_file

    def _process_pdf_file(self, pdf_file: str) -> str:
        pdf_document = ""
        with pymupdf.open(stream=pdf_file, filetype="pdf") as pdf_reader:
            for page_num in range(pdf_reader.page_count):
                page = pdf_reader[page_num]
                pdf_document += page.get_text()
        return pdf_document

    def _clean_text(self, text: str) -> str:
        return ' '.join(text.split())

    def _chunking(self, text: str, chunk_size: int = 512, chunk_overlap: int = 50) -> List[str]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_text(text)
    
    def hybrid_search(self, query: str, top_k: int, bm25_boost: float = 1.0, vector_boost: float = 1.0) -> List[str]:
        text_embedding = self.model.embedding(query)
        query_body = {
            "size": top_k,
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["text"],
                                "boost": bm25_boost
                            }
                        },
                        {
                            "script_score": {
                                "query": {"match_all": {}},
                                "script": {
                                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                    "params": {"query_vector": text_embedding, "vector_boost": vector_boost}
                                }
                            }
                        }
                    ]
                }
            }
        }
        return self._retrieval(query_body, top_k)

    def _retrieval(self, query_body: dict, top_k: int) -> List[str]:
        results = self.client.search(index=elasticsearch_config.index_name, body=query_body)
        hits = results['hits']['hits']
        if not hits:
            return {"message": "No labels found for the given document type."}

        # top_label = [hit['_source']['text'] for hit in results['hits']['hits'] if hit['_score'] >= threshold]

        top_label = [hit['_source']['text'] for hit in hits[:top_k]]
        return top_label

    def _get_point_by_id(self, index_name: str, id: str) -> dict:
        index_name = index_name.lower()
        try:
            response = self.client.get(index=index_name, id=id)
            return response['_source']
        except Exception as e:
            return JSONResponse({"error": f"Failed to search documents by ID from index {index_name}"}, status_code=500)

    
    def convert_to_serializable(self, obj: Any) -> Any:
        """Chuyển đổi các đối tượng không thể serialize thành dạng đơn giản."""
        if isinstance(obj, BaseModel):
            return obj.model_dump()  # Convert Pydantic BaseModel sang dict
        elif isinstance(obj, Enum):
            return obj.value  # Convert Enum to value
        elif isinstance(obj, list):
            return [self.convert_to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.convert_to_serializable(value) for key, value in obj.items()}
        else:
            return obj

    def delete_index(self, index_name: str) -> None:
        self.client.indices.delete(index=index_name)