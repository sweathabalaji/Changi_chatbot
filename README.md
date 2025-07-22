# Changi Airport Chatbot

A chatbot application that leverages a Large Language Model (LLM) and a Vector Database to answer questions based on website content from Changi Airport and Jewel Changi Airport.

## Features

- Data scraping from Changi Airport and Jewel Changi Airport websites
- Text vectorization using Sentence Transformers
- Vector storage with ChromaDB
- Retrieval-Augmented Generation (RAG) using LangChain
- Streamlit web interface
- FastAPI backend for integration

## Local Development

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)

### Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### Running the Application

#### Streamlit UI

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

#### FastAPI Backend

```bash
uvicorn api.app:app --reload
```

The API will be available at http://localhost:8000

### Deployed
```bash
http://34.93.46.156:8501/
```
