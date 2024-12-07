from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from typing import List

class InputText(BaseModel):
    index_name: str = Field(..., description="Tên index", examples=["text_embeddings"])
    text_input: str = Field(..., description="Text to be upserted", examples=["Tôi tên là Trọng, Hiện tôi đã tốt nghiệp trường Đại học Khoa học và Công nghệ Hà Nội với tấm bằng loại khá. Tôi rất thích học lập trình và đang theo đuổi chuyên ngành AI Engineer, tôi rất đam mê làm việc với NLP và mong muốn tìm một công việc liên quan đến nó."])

class InputQuery(BaseModel):
    text_input: str = Field(..., description="Question query", examples=["Hoàng Sa, Trường Sa là của nước nào?"])
    
class InputParams(BaseModel):
    temperature: float = Field(..., description="Temperature", examples=[0.8])
    threshold: float = Field(..., description="Threshold", examples=[1])
    
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
            {"role": "user", "content": "Con chó poodle có mấy chân?"},
            {"role": "assistant", "content": "Con chó poodle có 4 chân"},
            ]
        ]
    )

class HealthCheckResponse(BaseModel):
    messages: str = Field(..., description="Message", examples=["I am fine! 👍🏻"])
    
class DocumentTypes(BaseModel):
    document_type: str = Field(..., description="Document type", examples=["Document"])