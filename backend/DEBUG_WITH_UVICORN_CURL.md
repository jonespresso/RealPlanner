# Debugging with Uvicorn and Curl

This guide shows you how to debug the Route Optimization API by running the FastAPI server with uvicorn and testing it with curl commands.

## 🚀 Quick Start

### 1. Start the Server with Debugging

**Option A: VS Code Debugging (Recommended)**
1. Open VS Code Debug panel (`Ctrl+Shift+D`)
2. Select **"Debug FastAPI with Uvicorn"**
3. Press `F5` to start debugging
4. Set breakpoints in your code
5. The server will start on `http://localhost:8000`

**Option B: Command Line**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### 2. Test with Curl

**Option A: Use the test script**
```bash
cd backend
./test_with_curl.sh
```

**Option B: Use Python script**
```bash
cd backend
python test_with_curl.py
```

**Option C: Manual curl commands**
```bash
# Health check
curl -X GET "http://localhost:8000/"

# Ping endpoint
curl -X GET "http://localhost:8000/api/v1/ping"

# Route optimization
curl -X POST "http://localhost:8000/api/v1/plan-route" \
  -H "Content-Type: application/json" \
  -d '{
    "start_address": "100 Market St, San Francisco, CA",
    "houses": [
      {
        "address": "123 Main St, San Francisco, CA",
        "start_time": "2024-12-20T09:00:00Z",
        "end_time": "2024-12-20T17:00:00Z",
        "duration_minutes": 30
      }
    ]
  }'
```

## 🔧 Debugging Workflow

### Step 1: Set Breakpoints

Set breakpoints by **clicking in the gutter** next to line numbers in these key locations:

1. **API Endpoint** (`backend/app/api/v1/endpoints.py:15`):
   - Click in the gutter next to `logger.info(f"Received route planning request...")`

2. **OAuth Token** (`backend/app/services/route_optimization_api.py:25`):
   - Click in the gutter next to `service_account_info = settings.get_service_account_key()`

3. **API Call** (`backend/app/services/route_optimization_api.py:95`):
   - Click in the gutter next to `auth_token = get_oauth_token()`

4. **Response Processing** (`backend/app/services/route_optimization_api.py:120`):
   - Click in the gutter next to `if "unperformedShipments" in raw_response:`

### Step 2: Start Debugging

1. **Start VS Code debugging** with "Debug FastAPI with Uvicorn"
2. **Wait for server to start** (you'll see uvicorn startup logs)
3. **Send a curl request** to trigger the breakpoint
4. **Step through the code** using VS Code debug controls

### Step 3: Inspect Variables

When you hit a breakpoint, you can inspect:

- **Request data**: `request.houses`, `request.start_address`
- **API responses**: `response`, `result`
- **Intermediate variables**: `payload`, `locations`, `route_plan`

## 📋 Test Scenarios

### 1. Basic Route Optimization
```bash
curl -X POST "http://localhost:8000/api/v1/plan-route" \
  -H "Content-Type: application/json" \
  -d '{
    "start_address": "100 Market St, San Francisco, CA",
    "houses": [
      {
        "address": "123 Main St, San Francisco, CA",
        "start_time": "2024-12-20T09:00:00Z",
        "end_time": "2024-12-20T17:00:00Z",
        "duration_minutes": 30
      }
    ]
  }'
```

### 2. Multiple Houses with Time Windows
```bash
curl -X POST "http://localhost:8000/api/v1/plan-route" \
  -H "Content-Type: application/json" \
  -d '{
    "start_address": "100 Market St, San Francisco, CA",
    "destination_address": "200 Mission St, San Francisco, CA",
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
        "duration_minutes": 45
      }
    ]
  }'
```

### 3. Error Testing
```bash
curl -X POST "http://localhost:8000/api/v1/plan-route" \
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
  }'
```

## 🔍 Debugging Tips

### 1. Monitor Server Logs

Watch the uvicorn console for:
- Request logs
- Error messages
- Debug information

### 2. Use VS Code Debug Console

When paused at a breakpoint, use the debug console to:
```python
# Inspect request data
print(request.model_dump())

# Check service account credentials
from app.core.config import settings
print(settings.get_service_account_key() is not None)

# Test individual functions
from app.services.route_optimization_api import get_oauth_token
token = get_oauth_token()
print(f"Token: {token[:20]}..." if token else "No token")
```

### 3. Step Through Different Optimization Methods

The system tries multiple optimization methods. You can debug each one:

1. **Route Optimization API** (best)
2. **Routes API** (fallback)
3. **Greedy Algorithm** (final fallback)

### 4. Check API Responses

Inspect the raw API responses:
```python
# In debug console
import json
print(f"API Response: {json.dumps(response, indent=2)}")
```

## 🛠️ Common Debugging Scenarios

### Scenario 1: OAuth Token Issues

**Symptoms**: 401 Unauthorized errors

**Debug Steps**:
1. Check if service account key is loaded
2. Verify credentials format
3. Test token refresh

```python
# In debug console
from app.core.config import settings
key = settings.get_service_account_key()
print(f"Service account key loaded: {key is not None}")
if key:
    print(f"Key type: {key.get('type')}")
    print(f"Project ID: {key.get('project_id')}")
```

### Scenario 2: API Call Failures

**Symptoms**: HTTP errors (400, 403, 500)

**Debug Steps**:
1. Check request payload structure
2. Verify authentication headers
3. Inspect API response details

```python
# In debug console
import json
print(f"Request payload: {json.dumps(payload, indent=2)}")
print(f"Headers: {headers}")
```

### Scenario 3: Response Processing Issues

**Symptoms**: Empty route plan or parsing errors

**Debug Steps**:
1. Inspect raw API response
2. Check response structure
3. Validate data mapping

```python
# In debug console
print(f"Raw response: {json.dumps(response, indent=2)}")
print(f"Response keys: {list(response.keys())}")
```

## 📊 Monitoring and Logging

### Enable Detailed Logging

The server runs with debug logging. You'll see:
- Request/response details
- API call information
- Error stack traces
- Optimization method selection

### Key Log Messages

Watch for these important log messages:
- `"Received route planning request for X houses"`
- `"Calling Google Route Optimization API"`
- `"Successfully received optimized route"`
- `"Error getting OAuth token"`
- `"Route Optimization API failed"`

## 🧹 Cleanup

When done debugging:

1. **Stop the server**: Press `Ctrl+C` in the terminal or stop VS Code debugging
2. **Remove breakpoints**: Run the cleanup script
   ```bash
   cd backend
   python remove_debug_breakpoints.py
   ```

## 🎯 Pro Tips

1. **Start Small**: Test with 1-2 houses first
2. **Use Future Dates**: Avoid timestamp validation issues
3. **Monitor Network**: Check internet connectivity
4. **Watch Quotas**: Monitor API usage limits
5. **Save Responses**: Log successful responses for reference
6. **Test Error Cases**: Always test with invalid data
7. **Use Different Optimization Methods**: Test the fallback chain

## 🆘 Troubleshooting

### Server Won't Start
- Check if port 8000 is available
- Verify Python environment and dependencies
- Check for syntax errors in the code

### Breakpoints Not Hitting
- Ensure you're using the VS Code debug configuration
- Check that the server is running in debug mode
- Verify the request is reaching the correct endpoint

### Curl Commands Failing
- Check server is running on correct port
- Verify JSON syntax in request body
- Ensure Content-Type header is set correctly

This approach gives you real-world debugging experience with actual HTTP requests and responses! 