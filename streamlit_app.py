import requests
import streamlit as st

API_URL = "http://192.168.56.1:2206"
st.markdown("# :rainbow[Chatbot RAG-E v1]")

# Chatbot PART
st.sidebar.header("Chatbot")
selected_bot = st.sidebar.selectbox("Select chatbot:", 
                                    options=["Chatbot Basic", "Chatbot RAG"],
                                    label_visibility="collapsed")

if selected_bot == "Chatbot RAG":
    st.sidebar.subheader("Threshold")
    threshold = st.sidebar.slider(
        "Độ giới hạn kiến thức retrieval:", 
        min_value=0.0, max_value=5.0, value=1.0, step=0.2,
    )       

    st.sidebar.subheader("Temperature")
    temperature = st.sidebar.slider(
        "Độ sáng tạo của Bot:", 
        min_value=0.0, max_value=1.0, value=0.5, step=0.1,
    )
else:
    threshold = 0.8
    st.sidebar.subheader("Temperature")
    temperature = st.sidebar.slider(
        "Độ sáng tạo của Bot:", 
        min_value=0.0, max_value=1.0, value=0.5, step=0.1,
    )

query_text = st.text_area("Nhập câu hỏi của bạn:",
                          height=150,
                          placeholder="Nhập câu hỏi của bạn vào đây...",
                          label_visibility="collapsed")

if st.button("Send"):
    if query_text:
        if selected_bot == "Chatbot Basic":
            api_endpoint = "/chatbot-text-query"
        else:
            api_endpoint = "/chatbot-retrieval-query"
     
   
        with st.spinner("Đang xử lý..."):
            response = requests.post(
                f"{API_URL}{api_endpoint}",
                json = {
                    "input": {"text_input": query_text},
                    "params": {"temperature": temperature,
                               "threshold": threshold}
                }
            )
            if response.status_code == 200:
                st.write("**Phản hồi từ Chatbott:**")
                st.write(response.json())
            else:
                st.write("Lỗi khi call API:", response.status_code)
    else:
        st.write("Vui lòng nhập câu hỏi")


# Upsert PART
st.sidebar.header("")
st.sidebar.subheader("Upsert Document")
selected_document = st.sidebar.selectbox("Chọn thể loại document muốn upsert:", 
                                    options=["Văn bản", 
                                             "Thơ"])

st.header("")
st.header("Upsert text")
input_text = st.text_area("Enter here:", 
                          value="Tôi tên là Trọng, Hiện tôi đã tốt nghiệp trường Đại học Khoa học và Công nghệ Hà Nội với tấm bằng loại khá. Tôi rất thích học lập trình và đang theo đuổi chuyên ngành AI Engineer, tôi rất đam mê làm việc với NLP và mong muốn tìm một công việc liên quan đến nó.",
                          placeholder="Nhập text cần upsert vào đây...",
                          label_visibility="collapsed")

if st.button("Upsert text"):
    if input_text:
        with st.spinner("Đang xử lý..."):
            response = requests.post(
                f"{API_URL}/upsert-text",
                json={"index_name": "text_embeddings", "text_input": input_text}
            )
            if response.status_code == 200:
                st.write("Dữ liệu đã được upsert thành công.")
            else:
                st.write("Lỗi khi gọi API:", response.status_code)
    else:
        st.write("Vui lòng nhập đầy đủ thông tin.")


st.header("Upsert file")
uploaded_file = st.file_uploader("Drag file pdf here:", 
                                type=["pdf"],
                                label_visibility="collapsed")

if st.button("Upsert file"):
    with st.spinner("Đang xử lý..."):
        response = requests.post(
            f"{API_URL}/upsert-file?doc_type={selected_document}",
            files={"file_path": uploaded_file}
        )
        if response.status_code == 200:
            st.write("Dữ liệu đã được upsert từ file.")
        else:
            st.write("Lỗi khi gọi API:", response.status_code)


# Delete Index PART
st.sidebar.header("")
st.sidebar.header("Delete Index")
index_to_delete = st.sidebar.text_input("Nhập tên index để xoá:",
                                        
                                        placeholder='text_embeddings')
if st.sidebar.button("Xoá Index"):
    if index_to_delete:
        response = requests.delete(
            f"{API_URL}/delete-index?index_name={index_to_delete}"
        )
        if response.status_code == 200:
            st.sidebar.write("Index đã được xoá thành công.")
        else:
            st.sidebar.write("Lỗi khi gọi API:", response.status_code)
    else:
        st.sidebar.write("Vui lòng nhập tên index.")


st.sidebar.header("")
st.sidebar.header("Health Check")
if st.sidebar.button("Kiểm tra trạng thái"):
    response = requests.get(f"{API_URL}/healthz")
    if response.status_code == 200:
        st.sidebar.write("I am fine! 👍🏻")
    else:
        st.sidebar.write("Ọc Ọc Ọc! 😱")


# streamlit run streamlit_app.py
