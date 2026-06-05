"""Test if the backend API is working"""
import requests
import sys

API_URL = "http://localhost:8000"

try:
    # Test health endpoint
    response = requests.get(f"{API_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print("✅ Backend is running!")
        print(f"   Status: {data['status']}")
        print(f"   Model loaded: {data['model_loaded']}")
        print(f"\n🎯 Backend API: {API_URL}")
        print(f"🌐 Frontend: http://localhost:3000")
        sys.exit(0)
    else:
        print(f"❌ Backend responded with status {response.status_code}")
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print("❌ Backend is not running!")
    print("\n💡 To start the backend:")
    print("   cd backend")
    print("   python api.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
