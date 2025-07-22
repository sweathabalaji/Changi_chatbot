import requests
import json
import time

# API endpoint (change this to your deployed URL when available)
API_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    response = requests.get(f"{API_URL}/health")
    print(f"Health check status code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check test passed!\n")

def test_root_endpoint():
    """Test the root endpoint"""
    response = requests.get(f"{API_URL}/")
    print(f"Root endpoint status code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert "message" in response.json()
    print("✅ Root endpoint test passed!\n")

def test_ask_endpoint():
    """Test the ask endpoint with a simple question"""
    payload = {
        "question": "How many terminals does Changi Airport have?",
        "conversation_id": f"test_{int(time.time())}"
    }
    
    print(f"Sending question: {payload['question']}")
    response = requests.post(f"{API_URL}/ask", json=payload)
    print(f"Ask endpoint status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Answer: {result['answer']}")
        print(f"Processing time: {result['processing_time']:.2f} seconds")
        print(f"Conversation ID: {result['conversation_id']}")
        assert "answer" in result
        print("✅ Ask endpoint test passed!\n")
    else:
        print(f"❌ Error: {response.text}")

def main():
    print("🧪 Starting API tests...\n")
    
    try:
        test_health_endpoint()
        test_root_endpoint()
        test_ask_endpoint()
        print("🎉 All tests passed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    main()