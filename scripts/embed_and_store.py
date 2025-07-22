# Updated for LangChain >= v0.2

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from text_splitter import load_and_split_text
import os
import shutil

def embed_text_and_store():
    # Get absolute path to data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(script_dir), "data", "changi_jewel.txt")
    
    print(f"Loading and splitting text from {data_path}")
    texts = load_and_split_text(data_path)
    print(f"Loaded {len(texts)} text chunks")
    
    # Use Sentence Transformers (SBERT)
    print("Initializing embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Set the persist directory with absolute path
    persist_dir = os.path.join(os.path.dirname(script_dir), "chroma_store")
    
    # Clear existing database if it exists
    if os.path.exists(persist_dir):
        print(f"Removing existing database at {persist_dir}")
        shutil.rmtree(persist_dir)
    
    print(f"Creating new vector database at {persist_dir}")
    
    # Create Chroma DB with metadata
    db = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        persist_directory=persist_dir,
        collection_metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )
    
    # Persist to disk (note: this is now automatic in newer Chroma versions)
    try:
        db.persist()
    except Exception as e:
        print(f"Note: {e}")
        print("This is expected with newer Chroma versions as persistence is automatic.")
    
    print(f"✅ Successfully embedded {len(texts)} chunks and stored in {persist_dir}")
    
    # Get vector dimension safely
    try:
        vector = embedding_model.embed_documents(['test'])[0]
        if hasattr(vector, 'shape'):
            print(f"Vector dimension: {vector.shape[0]}")
        else:
            print(f"Vector dimension: {len(vector)}")
    except Exception as e:
        print(f"Could not determine vector dimension: {e}")
    
    print("Database is ready for querying!")

if __name__ == "__main__":
    embed_text_and_store()
