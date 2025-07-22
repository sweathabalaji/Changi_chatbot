from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def clean_text(text):
    """Clean and normalize text for better chunking"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove any strange characters
    text = re.sub(r'[^\w\s.,;:!?\-\'\"\(\)\[\]{}]', '', text)
    return text.strip()

def load_and_split_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Clean the text
    text = clean_text(text)
    
    # Use a larger chunk size to capture more context
    # but with significant overlap to maintain continuity between chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Larger chunks for more context
        chunk_overlap=200,  # Significant overlap to maintain context
        separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""],  # Custom separators
        length_function=len
    )
    
    chunks = splitter.split_text(text)
    print(f"Split text into {len(chunks)} chunks")
    return chunks