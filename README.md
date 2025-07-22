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

## Deployment to Vercel

This project is configured for deployment on Vercel.

### Prerequisites

1. Install Vercel CLI:
   ```bash
   # Using npm
   npm install -g vercel
   
   # Using yarn
   yarn global add vercel
   
   # Or use our helper script
   ./install_vercel_cli.sh
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

### Automated Deployment

Use the provided deployment script:

```bash
./deploy.sh
```

This script will:
- Check if Vercel CLI is installed
- Verify login status
- Prepare the requirements file for Vercel
- Deploy the application
- Restore the original requirements file

### Manual Deployment Steps

1. Make sure your code is committed to a Git repository (GitHub, GitLab, or Bitbucket)

2. Deploy using Vercel CLI:
   ```bash
   vercel
   ```

3. For subsequent deployments:
   ```bash
   vercel --prod
   ```

### Deployment Without Vercel CLI

If you prefer not to install Vercel CLI, you can deploy directly through the Vercel dashboard:

1. Push your code to GitHub, GitLab, or Bitbucket
2. Visit https://vercel.com/new
3. Import your repository
4. Configure the project:
   - Set the Framework Preset to "Other"
   - Set the Root Directory to the project root
   - Set the Build Command to `pip install -r requirements-vercel.txt`
   - Set the Output Directory to `api`
5. Add the required environment variables (see below)
6. Deploy

### Environment Variables

Make sure to set the following environment variables in your Vercel project settings:

- `GOOGLE_API_KEY`: Your Google API key for Gemini model access

### Important Notes

- The Vercel deployment uses the FastAPI backend defined in `api/app.py`
- The vector database (ChromaDB) is included in the deployment
- For production use, consider using a managed vector database service

## Project Structure

- `api/`: FastAPI backend code
- `data/`: Scraped and processed data
- `scripts/`: Utility scripts for scraping, embedding, and RAG implementation
- `chroma_store/`: Vector database storage
- `app.py`: Streamlit web interface
- `vercel.json`: Vercel deployment configuration

## License

MIT