import streamlit as st
import requests
import uuid
from requests.exceptions import ChunkedEncodingError


# ================== CONFIG ==================

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RAG Chatbot",
    layout="wide"
)

st.title("📄 RAG Chatbot")

# ================== SESSION STATE ==================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"thread-{uuid.uuid4().hex[:8]}"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_ready" not in st.session_state:
    st.session_state.rag_ready = False

# ================== SIDEBAR (RAG UPLOAD) ==================

st.sidebar.title("📂 RAG Setup")

uploaded_file = st.sidebar.file_uploader(
    "Upload a document (PDF or TXT)",
    type=["pdf", "txt"]
)

if uploaded_file:
    if st.sidebar.button("Build RAG Index"):
        with st.spinner("Building index..."):
            files = {"file": uploaded_file}
            response = requests.post(
                f"{BASE_URL}/rag/upload",
                files=files
            )

        if response.status_code == 200:
            st.session_state.rag_ready = True
            st.sidebar.success("RAG index ready")
        else:
            st.sidebar.error("Failed to build index")

st.sidebar.divider()

if st.session_state.rag_ready:
    st.sidebar.markdown("✅ **RAG Enabled**")
else:
    st.sidebar.markdown("⚠️ **No document indexed**")

# ================== CHAT UI ==================

st.subheader("💬 Chat")

# Render chat history
for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask a question")

if user_input:
    # ---- User message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ---- Assistant (streaming)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        with requests.get(
            f"{BASE_URL}/chat/stream/{st.session_state.thread_id}",
            params={"message": user_input},
            stream=True,
            timeout=None
        ) as r:
            try:
                for chunk in r.iter_content(chunk_size=1024):
                    if not chunk:
                        continue
                    token = chunk.decode("utf-8", errors="ignore")
                    full_response += token
                    placeholder.markdown(full_response)
            except ChunkedEncodingError:
                pass


    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })

    st.rerun()
