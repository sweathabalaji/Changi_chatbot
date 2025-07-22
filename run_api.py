import uvicorn
import os

def main():
    # Get the port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting Changi Airport Chatbot API on port {port}")
    print("📝 API documentation will be available at http://localhost:{port}/docs")
    
    # Run the FastAPI application
    uvicorn.run("api.app:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    main()