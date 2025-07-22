from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Custom prompt guiding Gemini responses to be grounded in Changi/Jewel data
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

Helpful Answer:
"""

def load_qa_chain():
    # 1. Load sentence transformer model (for embedding text)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2. Load persisted Chroma vector DB
    db = Chroma(
        persist_directory="chroma_store", 
        embedding_function=embeddings
    )

    # 3. Configure retriever
    retriever = db.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 5}
    )

    # 4. Define prompt template
    prompt = PromptTemplate(
        template=CHANGI_TEMPLATE, 
        input_variables=["context", "question"]
    )

    # 5. Initialize Gemini Flash (faster, cheaper)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.2,
        max_output_tokens=1024
    )

    # 6. Return RAG pipeline
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}
    )
