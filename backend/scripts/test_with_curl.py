#!/usr/bin/env python3
"""
Python script to test Route Optimization API using requests
This provides the same functionality as the bash script but with better error handling
"""
import requests
import json
import time
from datetime import datetime, timezone, timedelta

BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/api/v1"

def test_endpoint(method, url, data=None, description=""):
    """Test an API endpoint and return the response"""
    print(f"\n{description}")
    print("-" * 50)
    
    try:
        start_time = time.time()
        
        if method.upper() == "GET":
            response = requests.get(url, timeout=30)
        elif method.upper() == "POST":
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=data, headers=headers, timeout=30)
        else:
            print(f"❌ Unsupported method: {method}")
            return
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"URL: {url}")
        print(f"Method: {method}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f}s")
        
        if response.status_code == 200:
            print("✅ Success!")
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
            except json.JSONDecodeError:
                print(f"Response: {response.text}")
        else:
            print("❌ Error!")
            print(f"Error Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

def main():
    """Run all API tests"""
    print("🧪 Testing Route Optimization API with Python requests")
    print("=" * 60)
    
    # Test 1: Health check
    test_endpoint("GET", BASE_URL, description="1️⃣ Testing health check")
    
    # Test 2: Ping endpoint
    test_endpoint("GET", f"{API_ENDPOINT}/ping", description="2️⃣ Testing ping endpoint")
    
    # Test 3: Route optimization with 2 houses
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    test_data_2_houses = {
        "start_address": "100 Market St, San Francisco, CA",
        "destination_address": "200 Mission St, San Francisco, CA",
        "houses": [
            {
                "address": "123 Main St, San Francisco, CA",
                "start_time": tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).isoformat(),
                "end_time": tomorrow.replace(hour=17, minute=0, second=0, microsecond=0).isoformat(),
                "duration_minutes": 30
            },
            {
                "address": "456 Oak Ave, San Francisco, CA",
                "start_time": tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).isoformat(),
                "end_time": tomorrow.replace(hour=17, minute=0, second=0, microsecond=0).isoformat(),
                "duration_minutes": 30
            }
        ]
    }
    test_endpoint("POST", f"{API_ENDPOINT}/plan-route", test_data_2_houses, 
                  description="3️⃣ Testing route optimization (2 houses)")
    
    # Test 4: Route optimization with 3 houses
    test_data_3_houses = {
        "start_address": "100 Market St, San Francisco, CA",
        "houses": [
            {
                "address": "123 Main St, San Francisco, CA",
                "start_time": tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).isoformat(),
                "end_time": tomorrow.replace(hour=17, minute=0, second=0, microsecond=0).isoformat(),
                "duration_minutes": 30
            },
            {
                "address": "456 Oak Ave, San Francisco, CA",
                "start_time": tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).isoformat(),
                "end_time": tomorrow.replace(hour=17, minute=0, second=0, microsecond=0).isoformat(),
                "duration_minutes": 45
            },
            {
                "address": "789 Pine St, San Francisco, CA",
                "start_time": tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).isoformat(),
                "end_time": tomorrow.replace(hour=17, minute=0, second=0, microsecond=0).isoformat(),
                "duration_minutes": 60
            }
        ]
    }
    test_endpoint("POST", f"{API_ENDPOINT}/plan-route", test_data_3_houses,
                  description="4️⃣ Testing route optimization (3 houses)")
    
    # Test 5: Route optimization with specific time windows
    test_data_time_windows = {
        "start_address": "100 Market St, San Francisco, CA",
        "houses": [
            {
                "address": "123 Main St, San Francisco, CA",
                "start_time": tomorrow.replace(hour=10, minute=0, second=0, microsecond=0).isoformat(),
                "end_time": tomorrow.replace(hour=12, minute=0, second=0, microsecond=0).isoformat(),
                "duration_minutes": 30
            },
            {
                "address": "456 Oak Ave, San Francisco, CA",
                "start_time": tomorrow.replace(hour=13, minute=0, second=0, microsecond=0).isoformat(),
                "end_time": tomorrow.replace(hour=15, minute=0, second=0, microsecond=0).isoformat(),
                "duration_minutes": 30
            }
        ]
    }
    test_endpoint("POST", f"{API_ENDPOINT}/plan-route", test_data_time_windows,
                  description="5️⃣ Testing route optimization with specific time windows")
    
    # Test 6: Error case - invalid address
    test_data_invalid = {
        "start_address": "Invalid Address, Nowhere, ZZ",
        "houses": [
            {
                "address": "Also Invalid, Nowhere, ZZ",
                "start_time": tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).isoformat(),
                "end_time": tomorrow.replace(hour=17, minute=0, second=0, microsecond=0).isoformat(),
                "duration_minutes": 30
            }
        ]
    }
    test_endpoint("POST", f"{API_ENDPOINT}/plan-route", test_data_invalid,
                  description="6️⃣ Testing error handling (invalid address)")
    
    print("\n✅ All tests completed!")
    print("📝 Check the server logs for detailed debugging information.")

if __name__ == "__main__":
    main() 