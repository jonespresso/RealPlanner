#!/bin/bash

# Test script for Route Optimization API using curl
# Make sure the FastAPI server is running on http://localhost:8000

BASE_URL="http://localhost:8000"
API_ENDPOINT="$BASE_URL/api/v1"

echo "🧪 Testing Route Optimization API with curl"
echo "============================================="

# Test 1: Basic health check
echo -e "\n1️⃣ Testing health check..."
curl -X GET "$BASE_URL/" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"

# Test 2: Ping endpoint
echo -e "\n2️⃣ Testing ping endpoint..."
curl -X GET "$API_ENDPOINT/ping" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"

# Test 3: Route optimization with 2 houses
echo -e "\n3️⃣ Testing route optimization (2 houses)..."
curl -X POST "$API_ENDPOINT/plan-route" \
  -H "Content-Type: application/json" \
  -d '{
    "start_address": "100 Market St, San Francisco, CA",
    "destination_address": "200 Mission St, San Francisco, CA",
    "houses": [
      {
        "address": "123 Main St, San Francisco, CA",
        "start_time": "2024-12-20T09:00:00Z",
        "end_time": "2024-12-20T17:00:00Z",
        "duration_minutes": 30
      },
      {
        "address": "456 Oak Ave, San Francisco, CA",
        "start_time": "2024-12-20T09:00:00Z",
        "end_time": "2024-12-20T17:00:00Z",
        "duration_minutes": 30
      }
    ]
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"

# Test 4: Route optimization with 3 houses (more complex)
echo -e "\n4️⃣ Testing route optimization (3 houses)..."
curl -X POST "$API_ENDPOINT/plan-route" \
  -H "Content-Type: application/json" \
  -d '{
    "start_address": "100 Market St, San Francisco, CA",
    "houses": [
      {
        "address": "123 Main St, San Francisco, CA",
        "start_time": "2024-12-20T09:00:00Z",
        "end_time": "2024-12-20T17:00:00Z",
        "duration_minutes": 30
      },
      {
        "address": "456 Oak Ave, San Francisco, CA",
        "start_time": "2024-12-20T09:00:00Z",
        "end_time": "2024-12-20T17:00:00Z",
        "duration_minutes": 45
      },
      {
        "address": "789 Pine St, San Francisco, CA",
        "start_time": "2024-12-20T09:00:00Z",
        "end_time": "2024-12-20T17:00:00Z",
        "duration_minutes": 60
      }
    ]
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"

# Test 5: Route optimization with time windows
echo -e "\n5️⃣ Testing route optimization with specific time windows..."
curl -X POST "$API_ENDPOINT/plan-route" \
  -H "Content-Type: application/json" \
  -d '{
    "start_address": "100 Market St, San Francisco, CA",
    "houses": [
      {
        "address": "123 Main St, San Francisco, CA",
        "start_time": "2024-12-20T10:00:00Z",
        "end_time": "2024-12-20T12:00:00Z",
        "duration_minutes": 30
      },
      {
        "address": "456 Oak Ave, San Francisco, CA",
        "start_time": "2024-12-20T13:00:00Z",
        "end_time": "2024-12-20T15:00:00Z",
        "duration_minutes": 30
      }
    ]
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"

# Test 6: Error case - invalid address
echo -e "\n6️⃣ Testing error handling (invalid address)..."
curl -X POST "$API_ENDPOINT/plan-route" \
  -H "Content-Type: application/json" \
  -d '{
    "start_address": "Invalid Address, Nowhere, ZZ",
    "houses": [
      {
        "address": "Also Invalid, Nowhere, ZZ",
        "start_time": "2024-12-20T09:00:00Z",
        "end_time": "2024-12-20T17:00:00Z",
        "duration_minutes": 30
      }
    ]
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"

echo -e "\n✅ All tests completed!"
echo "📝 Check the server logs for detailed debugging information." 