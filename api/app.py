from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import sys
from typing import Dict, Any, List, Optional

# Add the project root to the Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Determine if we're running on Vercel
is_vercel = os.environ.get('VERCEL') == '1'

# Import the appropriate RAG chain implementation
if is_vercel and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rag_chain_vercel.py')):
    print("Running on Vercel, using Vercel-specific RAG chain")
    from api.rag_chain_vercel import load_qa_chain
else:
    print("Running locally, using standard RAG chain")
    from scripts.rag_chain import load_qa_chain

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Changi Airport Chatbot API",
    description="API for querying information about Changi Airport and Jewel",
    version="1.0.0"
)

# Load QA chain once at startup
qa_chain = load_qa_chain()

# Allow CORS if using with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Query(BaseModel):
    question: str
    conversation_id: Optional[str] = None

# Response model
class Response(BaseModel):
    answer: str
    processing_time: float
    conversation_id: Optional[str] = None

# Simple in-memory conversation store
# In a production app, this would be a database
conversations: Dict[str, List[Dict[str, str]]] = {}

@app.post("/ask", response_model=Response)
def ask_question(query: Query):
    try:
        # Track processing time
        start_time = time.time()
        
        # Process the query
        answer = qa_chain.run(query.question)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Store conversation if ID provided
        if query.conversation_id:
            if query.conversation_id not in conversations:
                conversations[query.conversation_id] = []
            
            # Add to conversation history
            conversations[query.conversation_id].append(
                {"role": "user", "content": query.question}
            )
            conversations[query.conversation_id].append(
                {"role": "assistant", "content": answer}
            )
        
        # Return response
        return Response(
            answer=answer,
            processing_time=processing_time,
            conversation_id=query.conversation_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Changi Airport Chatbot API",
        "endpoints": ["/ask"],
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
