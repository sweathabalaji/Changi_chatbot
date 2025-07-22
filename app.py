import streamlit as st
from scripts.rag_chain import load_qa_chain
import time

# Page configuration
st.set_page_config(
    page_title="Changi & Jewel Airport Chatbot",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #006633;
    text-align: center;
    margin-bottom: 1rem;
}
.subheader {
    font-size: 1.1rem;
    color: #555;
    text-align: center;
    margin-bottom: 2rem;
}
.stTextInput > div > div > input {
    font-size: 1rem;
}
.response-container {
    background-color: #f0f2f6;
    padding: 1.25rem;
    border-radius: 0.5rem;
    border-left: 5px solid #006633;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Headers
st.markdown('<p class="main-header">🛫 Changi & Jewel Airport Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Your guide to Singapore Changi Airport & Jewel</p>', unsafe_allow_html=True)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Cache and load chain
@st.cache_resource
def get_qa_chain():
    return load_qa_chain()

qa_chain = get_qa_chain()

# Sidebar examples
with st.sidebar:
    st.header("Example Questions")
    examples = [
        "What attractions can I find at Jewel Changi Airport?",
        "What facilities are available for transit passengers in Terminal 4?",
        "What dining options are available at Changi Airport?",
        "How many terminals does Changi Airport have?",
        "What is the Rain Vortex at Jewel?"
    ]
    for q in examples:
        if st.button(q):
            st.session_state.user_input = q

# User input
user_input = st.text_input("Ask a question about Changi or Jewel Airport:", key="user_input")

# Process input
if st.button("Get Answer") and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    st.markdown(f"**You:** {user_input}")

    with st.spinner("Searching for information..."):
        start = time.time()
        answer = qa_chain.run(user_input)
        duration = time.time() - start

    st.session_state.chat_history.append({"role": "assistant", "content": answer})

    st.markdown("<div class='response-container'>", unsafe_allow_html=True)
    st.markdown(f"**Changi Assistant:** {answer}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption(f"Response generated in {duration:.2f} seconds")

# Show chat history toggle
if st.session_state.chat_history and st.checkbox("Show chat history"):
    st.subheader("Conversation Log")
    for msg in st.session_state.chat_history:
        role = "You" if msg["role"] == "user" else "Changi Assistant"
        st.markdown(f"**{role}:** {msg['content']}")
        st.markdown("---")

# Footer
st.markdown("---")
st.caption("© 2024 Changi Airport Chatbot | Powered by LangChain & Gemini")
