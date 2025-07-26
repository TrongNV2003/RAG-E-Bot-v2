import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import requests
import streamlit as st

from rag.config.setting import elasticsearch_config

api_url = os.getenv("API_URL")


st.set_page_config(
    page_title="RAG-E Ver2",
    page_icon="🧊",
    # layout="wide",
    initial_sidebar_state="auto",
)

# Custom CSS
st.markdown("""
    <style>
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
        }
        .user-message, .bot-message {
            border-radius: 1.5rem;
            padding: .625rem 1.25rem;
            margin: 5px 0;
            display: inline-block;
            max-width: 80%;
        }
        .user-message {
            background-color: rgba(50, 50, 50, .85);
            text-align: right;
            color: white;
            font-size: 18px;
            align-self: flex-end;
        }
        .bot-message {
            background-color: transparent;
            color: white;
            font-size: 18px;
            align-self: flex-start;
        }
        .chat {
            display: flex;
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("# :rainbow[RAG-E version 2.0.0]")
st.sidebar.header("Chatbot")

st.sidebar.subheader("Temperature")
temperature = st.sidebar.slider(
    "Độ sáng tạo của RAG-E:", 
    min_value=0.0, max_value=1.0, value=0.5, step=0.1,
)

st.sidebar.subheader("Top K")
top_k = st.sidebar.slider(
    "Số lượng documents truy xuất:", 
    min_value=1, max_value=10, value=5, step=1,
)

def Chatbot_RAG():
    # Upsert PART
    st.sidebar.markdown("---")
    st.sidebar.subheader("Select document types")
    selected_document = st.sidebar.selectbox("Chọn thể loại document muốn upsert:", 
                                        options=["Văn bản", "Thơ"])
    st.sidebar.markdown("---")
    st.sidebar.subheader("Select Upsert types")
    selected_upsert = st.sidebar.selectbox("Chọn kiểu upsert:", 
                                        options=["Upsert text", "Upsert file"])
    
    if selected_upsert == "Upsert text":
        st.sidebar.subheader("Upsert text")
        input_text = st.sidebar.text_area("Enter here:", 
                                placeholder="Nhập text cần upsert...",
                                label_visibility="collapsed")

        if st.sidebar.button("Upsert text"):
            if input_text:
                with st.spinner("Đang xử lý..."):
                    response = requests.post(
                        f"{api_url}/upsert-text",
                        json={"index_name": elasticsearch_config.index_name, "text_input": input_text}
                    )
                    if response.status_code == 200:
                        st.sidebar.write("Dữ liệu đã được upsert thành công.")
                    else:
                        st.sidebar.write("Lỗi khi gọi API:", response.status_code)
            else:
                st.write("Vui lòng nhập đầy đủ thông tin.")
    
    elif selected_upsert == "Upsert file":
        st.sidebar.subheader("Upsert file")
        uploaded_file = st.sidebar.file_uploader("Drag file pdf here:", 
                                        type=["pdf"],
                                        label_visibility="collapsed")
        if st.sidebar.button("Upsert file"):
            with st.spinner("Đang xử lý..."):
                response = requests.post(
                    f"{api_url}/upsert-file?doc_type={selected_document}",
                    files={"file_path": uploaded_file}
                )
                if response.status_code == 200:
                    st.sidebar.write("Dữ liệu đã được upsert từ file.")
                else:
                    st.sidebar.write("Lỗi khi gọi API:", response.status_code)

    # Delete Index PART
    st.sidebar.markdown("---")
    st.sidebar.header("Delete Index")
    index_to_delete = st.sidebar.text_input("Nhập tên index để xoá:",
                                            placeholder='text_embeddings')
    if st.sidebar.button("Xoá Index"):
        if index_to_delete:
            response = requests.delete(
                f"{api_url}/delete-index?index_name={index_to_delete}"
            )
            if response.status_code == 200:
                st.sidebar.write("Index đã được xoá thành công.")
            else:
                st.sidebar.write("Lỗi khi gọi API:", response.status_code)
        else:
            st.sidebar.write("Vui lòng nhập tên index.")


def query_processing(query_text: str, temperature: float, top_k: int, api_endpoint: str, history: list) -> str:
    with st.spinner("Đang xử lý..."):
        payload = {
            "input": {"text_input": query_text},
            "params": {"temperature": temperature, "top_k": top_k},
            "history": {"chat_history": history}
        }
        response = requests.post(f"{api_url}{api_endpoint}", json=payload)
        
        if response.status_code == 200:
            bot_response = response.json()["Answer"]
        else:
            st.write("Lỗi khi call API:", response.status_code, response.text)
    return bot_response

def health_check():
    st.sidebar.markdown("---")
    st.sidebar.header("Health Check")
    if st.sidebar.button("Kiểm tra trạng thái"):
        response = requests.get(f"{api_url}/healthz")
        if response.status_code == 200:
            st.sidebar.write("I am fine! 👍🏻")
        else:
            st.sidebar.write("Ọc Ọc Ọc! 😱")

#Sending processing
def main():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        initial_bot_message = "Hello! I am RAG-E. How can I assist you today?"
        st.session_state.chat_history.append({"role": "assistant", "content": initial_bot_message})
        
    query_text = st.chat_input("Ask RAG-E something...")
    if query_text:
        api_endpoint = "/chatbot-retrieval-query"


        bot_response = query_processing(query_text, temperature, top_k, api_endpoint, st.session_state.chat_history)
        if bot_response:
            st.session_state.chat_history.append({"role": "user", "content": query_text})
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

    # Display chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="chat"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat"><div class="bot-message">{message["content"]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    Chatbot_RAG()
    health_check()