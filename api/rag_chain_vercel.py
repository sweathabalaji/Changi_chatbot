from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Define a custom prompt template to guide the model's responses
CHANGI_TEMPLATE = """
You are a helpful assistant for Changi Airport and Jewel in Singapore. 
Use the following pieces of context to answer the question at the end.

The context contains factual information about Changi Airport, including:
- The number of terminals and their features
- Facilities available at different terminals
- Information about Jewel Changi Airport
- General facts about Changi Airport's operations

Answer the question based ONLY on the information provided in the context. Be specific and direct.
If you don't know the answer based on the context provided, don't make up an answer or provide disclaimers about not having real-time information. 
Instead, provide the most relevant information from the context or suggest that the user check the official Changi Airport website for the most up-to-date information.

Context: {context}

Question: {question}

Helpful Answer:"""

def load_qa_chain():
    # Determine the correct path for the vector database
    # For Vercel deployment, the database should be in the same directory as this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persist_directory = os.path.join(current_dir, "chroma_store")
    
    # Check if the database exists in the current directory
    if not os.path.exists(persist_directory):
        # Fall back to the project root directory
        persist_directory = os.path.join(os.path.dirname(current_dir), "chroma_store")
    
    print(f"Using vector database at: {persist_directory}")
    
    # Load HuggingFace sentence transformer model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load Chroma vector DB from disk
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    
    # Configure retriever with search parameters
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}  # Retrieve more documents for better context
    )

    # Create the custom prompt
    prompt = PromptTemplate(
        template=CHANGI_TEMPLATE,
        input_variables=["context", "question"]
    )

    # Initialize Gemini LLM with correct model name
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.2,
        max_output_tokens=1024  # Ensure we get detailed responses
    )

    # Create Retrieval QA chain with custom prompt
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Stuff all retrieved documents into the prompt
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}
    )

    return chain