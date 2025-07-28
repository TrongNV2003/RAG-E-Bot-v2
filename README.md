# RAG-E Bot Version 2

**New Update Ver 2**: 
- Update with API calling model (Qwen3)
- Update Prompt template giúp LLM phản hồi tốt hơn
- Refactor upsert, retrieval tăng tốc quá trình inference

Chatbot Retrieval-Augmented Generation (RAG) áp dụng ElasticSearch là một hệ thống chatbot tận dụng khả năng vector store và vector search của ElasticSearch để truy xuất thông tin có liên quan và sức mạnh tạo ngôn ngữ tự nhiên của mô hình Qwen3. Chatbot này có thể xử lý các truy vấn phức tạp bằng cách kết hợp truy xuất dữ liệu với các phản hồi do AI tạo ra.

- Llama models for chatbot: 
    + [Qwen/Qwen3-4B-AWQ](https://huggingface.co/Qwen/Qwen3-4B-AWQ)     ***NEW***
    + [unsloth/Llama-3.2-1B-Instruct](https://huggingface.co/unsloth/Llama-3.2-1B-Instruct)
    + [phamhai/Llama-3.2-1B-Instruct-Frog](https://huggingface.co/phamhai/Llama-3.2-1B-Instruct-Frog)

- RoBerta model for embeddings:
    + [hiieu/halong_embedding](https://huggingface.co/hiieu/halong_embedding)   ***NEW***
    + [Trongdz/roberta-embeddings-auto-labeling-tasks](https://huggingface.co/Trongdz/roberta-embeddings-auto-labeling-tasks): model được huấn luyện riêng cho tác vụ Embedding.

## Features
- Upsert data: Cho phép insert các tài liệu dạng "pdf" hoặc "một đoạn mô tả" của người dùng lên vector db cho phép bot truy xuất dữ liệu để trả lời câu hỏi liên quan.
- RAG chatbot: Truy xuất vào dữ liệu người dùng cung cấp để trả lời câu hỏi liên quan.

## Installation
### Clone repo
```sh
git clone https://github.com/TrongNV2003/RAG-E-Bot-v2.git
cd RAG-E-Bot-v2
```

### Install dependancies
```sh
pip install -r requirements.txt
```

### Download ElasticSearch and Kibana
Hướng dẫn tải ElasticSearch để sử dụng tính năng Retrieval: [Elasticsearch](https://www.youtube.com/watch?v=0EJoVQkjXps)

(Optional) Kibana dùng như UI để hiển thị các tính năng và tương tác với ElasticSearch.

Sau khi tải xong, mở "Command Prompt", truy cập vào folder "bin" trong Elasticsearch và mở file "elasticsearch.bat" để chạy ElasticSearch: 
```
elasticsearch.bat
```

## Note
- TBD

## Usage
### Running
```
python app.py
```

### UI
Streamlit được sử dụng để xây dựng UI cho model:
```sh
cd rag/
streamlit run streamlit_app.py
```
or
```sh
cd rag/
$(python -c "import sys; print(sys.executable)") -m streamlit run streamlit_app.py
```

### Future feartures
- UI thân thiện với người dùng
- Cải thiện độ chính xác khi retrieval
- Cho phép select và upsert nhiều loại file (pdf, docs, txt, json ...)
- Hiện nay chỉ xử lý được pdf text thuần, chưa xử lý được dạng pdf có chứa hình ảnh hoặc các loại non-text.
- Optimize tính cách chatbot (Có thể là option lựa chọn)
- Cải thiện đọc lại lịch sử trò chuyện (Vấn đề hiện tại là khi lịch sử trò chuyện dài sẽ process lâu)

### Done feartures
- TBD