"""
Simple test script to verify API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")

def test_create_stack():
    """Test creating a stack"""
    data = {
        "name": "Test Stack",
        "description": "A test stack for API testing"
    }
    response = requests.post(f"{BASE_URL}/api/stacks", json=data)
    print(f"Create stack: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
        return response.json()["id"]
    return None

def test_get_stacks():
    """Test getting all stacks"""
    response = requests.get(f"{BASE_URL}/api/stacks")
    print(f"Get stacks: {response.status_code}")
    print(f"Response: {response.json()}")

def test_llm_generate():
    """Test LLM generation"""
    data = {
        "prompt": "Hello, how are you?",
        "model": "gpt-4o-mini",
        "temperature": 0.7
    }
    response = requests.post(f"{BASE_URL}/api/llm/generate", json=data)
    print(f"LLM generate: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("Testing GenAI Stack API...")
    print("=" * 50)
    
    try:
        test_health()
        print()
        
        stack_id = test_create_stack()
        print()
        
        test_get_stacks()
        print()
        
        # Uncomment to test LLM (requires OpenAI API key)
        # test_llm_generate()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")
