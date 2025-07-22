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

# Custom CSS for better appearance
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #006633;
    text-align: center;
    margin-bottom: 1rem;
}
.subheader {
    font-size: 1.2rem;
    color: #666;
    text-align: center;
    margin-bottom: 2rem;
}
.stTextInput > div > div > input {
    font-size: 1.1rem;
}
.response-container {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 0.5rem;
    border-left: 5px solid #006633;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🛫 Changi & Jewel Airport Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Your guide to Singapore Changi Airport & Jewel</p>', unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Load QA chain (only once)
@st.cache_resource
def get_qa_chain():
    return load_qa_chain()

qa_chain = get_qa_chain()

# Sidebar with example questions
with st.sidebar:
    st.header("Example Questions")
    example_questions = [
        "What attractions can I find at Jewel Changi Airport?",
        "What facilities are available for transit passengers in Terminal 4?",
        "What dining options are available at Changi Airport?",
        "How many terminals does Changi Airport have?",
        "What is the Rain Vortex at Jewel?"
    ]
    
    for question in example_questions:
        if st.button(question):
            st.session_state.user_input = question

# Get user input
user_input = st.text_input("Ask a question about Changi or Jewel Airport:", key="user_input")

# Process user query
if st.button("Get Answer") and user_input:
    # Add user query to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Display user query
    st.markdown(f"**You:** {user_input}")
    
    # Generate response with progress indicator
    with st.spinner("Searching for information..."):
        start_time = time.time()
        response = qa_chain.run(user_input)
        elapsed_time = time.time() - start_time
    
    # Add response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Display response with styling
    st.markdown("<div class='response-container'>", unsafe_allow_html=True)
    st.markdown(f"**Changi Assistant:** {response}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show response time
    st.caption(f"Response generated in {elapsed_time:.2f} seconds")

# Display chat history
if st.session_state.chat_history and st.checkbox("Show chat history", value=False):
    st.subheader("Chat History")
    for message in st.session_state.chat_history:
        role = "You" if message["role"] == "user" else "Changi Assistant"
        st.markdown(f"**{role}:** {message['content']}")
        st.markdown("---")

# Footer
st.markdown("---")
st.caption("© 2024 Changi Airport Chatbot | Powered by LangChain & Gemini")
