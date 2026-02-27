import streamlit as st
import sys
import os

# Add src folder to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from chain import build_chain
from logger import init_db, log_query, log_feedback

# Initialize database on startup
init_db()

# Build RAG chain on startup
@st.cache_resource
def load_chain():
    return build_chain()

chain = load_chain()

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RAG-Powered Chatbot")
st.caption("Answers questions strictly from the knowledge base.")

# ─── Session State ───────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "log_ids" not in st.session_state:
    st.session_state.log_ids = []

# ─── Chat History Display ────────────────────────────────────────────────────
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show feedback buttons only on assistant messages
        if message["role"] == "assistant" and i // 2 < len(st.session_state.log_ids):
            log_id = st.session_state.log_ids[i // 2]
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button("👍", key=f"up_{i}"):
                    log_feedback(log_id, 1)
                    st.success("Thanks for your feedback!")
            with col2:
                if st.button("👎", key=f"down_{i}"):
                    log_feedback(log_id, 0)
                    st.warning("Feedback recorded. We'll improve this.")

# ─── Chat Input ──────────────────────────────────────────────────────────────
if query := st.chat_input("Ask a question..."):

    # Display user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke(query)
        st.markdown(response)

    # Log to database
    log_id = log_query(query, response)
    st.session_state.log_ids.append(log_id)
    st.session_state.messages.append({"role": "assistant", "content": response})