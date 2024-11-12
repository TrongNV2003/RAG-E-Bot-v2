# RAG-E Bot v1

Chatbot Retrieval-Augmented Generation (RAG) áp dụng ElasticSearch là một hệ thống trả lời câu hỏi tận dụng khả năng vector store và vector search của ElasticSearch để truy xuất thông tin có liên quan và sức mạnh tạo ngôn ngữ tự nhiên của mô hình "Llama 3.2 1B Instruct". Chatbot này có thể xử lý các truy vấn phức tạp bằng cách kết hợp truy xuất dữ liệu với các phản hồi do AI tạo ra trôi chảy và có nhận thức về ngữ cảnh.

- Llama model for chatbot: 'unsloth/Llama-3.2-1B-Instruct'.

- RoBerta model for embedding: 'Trongdz/roberta-embeddings-auto-labeling-tasks': model được huấn luyện riêng cho tác vụ Embedding.

## Features
- Upsert data: Cho phép insert các tài liệu dạng "pdf" hoặc "một đoạn mô tả" của người dùng lên database cho phép bot truy xuất dữ liệu để trả lời câu hỏi liên quan.
- Normal chatbot: Cho phép trả lời các câu hỏi thường nhật của người dùng.
- RAG chatbot: Truy xuất vào dữ liệu người dùng cung cấp để trả lời câu hỏi liên quan.

## Installation
### Clone repo
```sh
git clone https://github.com/TrongNV2003/RAG-E-Bot-v1.git

cd Chatbot-RAG-ElasticSearch
```

### Install pakages

```sh
pip install -r requirements.txt
```

### Download ElasticSearch and Kibana
Hướng dẫn tải ElasticSearch để sử dụng tính năng Retrieval: [Elasticsearch](https://www.youtube.com/watch?v=0EJoVQkjXps)

(Optional) Kibana dùng như UI để hiển thị các tính năng trong ElasticSearch

Sau khi tải xong, mở "Command Prompt", truy cập vào folder "bin" trong Elasticsearch và mở file "elasticsearch.bat" để chạy ElasticSearch: 
```
elasticsearch.bat
```

- Lưu ý: Replace username và password của Elasticsearch: path: 'db/elasticsearch/connector.py' để truy cập 

## Usage
### Running
```
python app.py
```

### UI
Streamlit được sử dụng để xây dựng UI cho model:
```
streamlit run streamlit_app.py
```