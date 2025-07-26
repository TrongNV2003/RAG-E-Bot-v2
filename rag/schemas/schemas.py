from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from typing import List

class InputText(BaseModel):
    index_name: str = Field(..., description="Tên index", examples=["text_embeddings"])
    text_input: str = Field(..., description="Text to be upserted", examples=["Tôi tên là Trọng, tôi đã tốt nghiệp trường Đại học Khoa học và Công nghệ Hà Nội với tấm bằng loại khá. Tôi rất thích học lập trình và đang theo đuổi chuyên ngành AI Engineer, tôi rất đam mê làm việc với NLP và hiện tôi đang làm việc tại công ty GHTK."])

class InputQuery(BaseModel):
    text_input: str = Field(..., description="Question query", examples=["Hoàng Sa, Trường Sa là của nước nào?"])
    
class InputParams(BaseModel):
    temperature: float = Field(..., description="Temperature", examples=[0.8])
    threshold: float = Field(..., description="Threshold", examples=[1])
    top_k: int = Field(..., description="Top K", examples=[5])
    is_retrieval: bool = Field(..., description="Is retrieval", examples=[True, False])
    
class InputFile(BaseModel):
    index_name: str = Field(..., description="Index", examples=["text_embeddings"])
    file_path: UploadFile = File(...)
    
class ChatMessage(BaseModel):
    role: str = Field(None, description="Role of the participant", examples=["user", "assistant"])
    content: str = Field(None, description="Content of the message", examples=["Hello!", "How can I help you?"])

class ChatHistory(BaseModel):
    chat_history: List[ChatMessage] = Field(
        None, 
        description="Chat history as a list of messages",
        examples=[[
            {"role": "assistant", "content": "Hello! I am RAG-E. How can I assist you today?"},
            {"role": "user", "content": "Bạn tên là gì?"},
            {"role": "assistant", "content": "Tôi là RAG-E, một AI hỗ trợ tìm kiếm thông tin. Bạn cần giúp gì?"},
            ]
        ]
    )

class HealthCheckResponse(BaseModel):
    messages: str = Field(..., description="Message", examples=["I am fine! 👍🏻"])
    
class DocumentTypes(BaseModel):
    document_type: str = Field(..., description="Document type", examples=["Document"])