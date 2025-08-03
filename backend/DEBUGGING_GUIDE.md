# Route Optimization API Debugging Guide

This guide covers multiple methods for debugging the `route_optimization_api.py` file with breakpoints and stepping.

## 🚀 Quick Start - VS Code Debugging (Recommended)

### 1. Setup VS Code Debugging

1. **Install Python Extension**: Make sure you have the Python extension installed in VS Code
2. **Select Python Interpreter**: Press `Ctrl+Shift+P` → "Python: Select Interpreter" → Choose your virtual environment
3. **Open Debug Panel**: Press `Ctrl+Shift+D` or click the debug icon in the sidebar

### 2. Use the Debug Configurations

The `.vscode/launch.json` file provides several debugging configurations:

- **"Debug Route Optimization API"**: Runs the test file with debugging
- **"Debug Route Optimization API (Step Into)"**: Stops at the first line for step-by-step debugging
- **"Debug FastAPI Server"**: Debugs the entire FastAPI application
- **"Debug with Custom Test"**: Uses the custom debug script

### 3. Set Breakpoints

1. **Click in the gutter** next to line numbers in `route_optimization_api.py` to set breakpoints
2. **Key breakpoint locations**:
   - Line 25: OAuth token generation
   - Line 95: Before API call
   - Line 120: Response processing
   - Line 180: Full optimization function

### 4. Start Debugging

1. Select a debug configuration from the dropdown
2. Press `F5` or click the green play button
3. Use debugging controls:
   - `F10`: Step Over (execute current line)
   - `F11`: Step Into (go into function calls)
   - `F12`: Step Out (exit current function)
   - `F5`: Continue (run until next breakpoint)

## 🔧 Method 2: Python Debugger (pdb)

### Using the Built-in Breakpoints

The code already has strategic `pdb.set_trace()` breakpoints:

```python
# BREAKPOINT: OAuth token generation
import pdb; pdb.set_trace()  # Debug breakpoint - remove in production
```

### Running with pdb

```bash
cd backend
python debug_route_optimization.py
```

### pdb Commands

When you hit a breakpoint, use these commands:

- `n` (next): Execute current line and move to next
- `s` (step): Step into function calls
- `c` (continue): Continue execution until next breakpoint
- `l` (list): Show current code context
- `p variable_name`: Print variable value
- `pp variable_name`: Pretty print variable
- `w` (where): Show call stack
- `q` (quit): Exit debugger

### Example pdb Session

```
(Pdb) p service_account_info
{'type': 'service_account', 'project_id': '...'}
(Pdb) n
(Pdb) p credentials
<google.auth.service_account.Credentials object at 0x...>
(Pdb) c
```

## 🧪 Method 3: Custom Debug Script

### Running the Debug Script

```bash
cd backend
python debug_route_optimization.py
```

This script provides step-by-step debugging with detailed output for each stage:

1. **OAuth Token Generation**: Tests credential loading
2. **Payload Building**: Validates request structure
3. **API Call**: Tests the actual API request
4. **Response Processing**: Validates response parsing
5. **Full Optimization**: Tests the complete workflow

## 🔍 Method 4: Interactive Python Shell

### Start Interactive Debugging

```bash
cd backend
python -i debug_route_optimization.py
```

This allows you to:
- Import functions directly
- Test individual components
- Inspect variables interactively

### Example Interactive Session

```python
>>> from app.services.route_optimization_api import get_oauth_token
>>> token = get_oauth_token()
>>> print(f"Token: {token[:20]}..." if token else "No token")
>>> 
>>> from app.services.route_optimization_api import build_payload
>>> # Test payload building with your data
```

## 🐛 Method 5: Logging-Based Debugging

### Enable Debug Logging

The code uses structured logging. To see detailed logs:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Key Log Messages to Watch

- `"Calling Google Route Optimization API"`
- `"Successfully received optimized route"`
- `"Error getting OAuth token"`
- `"Route Optimization API failed"`

## 🔧 Method 6: Unit Test Debugging

### Debug Individual Tests

```bash
cd backend
python -m pytest tests/test_optimization.py -s -v --pdb
```

The `--pdb` flag drops you into the debugger on test failures.

## 🛠️ Common Debugging Scenarios

### 1. OAuth Token Issues

**Symptoms**: `"No OAuth token available"` error

**Debug Steps**:
1. Check if service account key is loaded
2. Verify credentials format
3. Test token refresh

```python
# Debug service account loading
from app.core.config import settings
key = settings.get_service_account_key()
print(f"Service account key loaded: {key is not None}")
```

### 2. API Call Failures

**Symptoms**: HTTP errors (401, 403, 400)

**Debug Steps**:
1. Check request payload structure
2. Verify authentication headers
3. Inspect API response details

```python
# Debug API call
import json
print(f"Request payload: {json.dumps(payload, indent=2)}")
print(f"Headers: {headers}")
```

### 3. Response Processing Issues

**Symptoms**: Empty route plan or parsing errors

**Debug Steps**:
1. Inspect raw API response
2. Check response structure
3. Validate data mapping

```python
# Debug response processing
print(f"Raw response: {json.dumps(response, indent=2)}")
print(f"Response keys: {list(response.keys())}")
```

## 🧹 Cleaning Up Debug Code

### Remove Debug Breakpoints

Before deploying to production, remove all debug breakpoints:

```python
# Remove these lines:
import pdb; pdb.set_trace()  # Debug breakpoint - remove in production
```

### Disable Debug Logging

Set logging level to INFO or WARNING in production:

```python
logging.basicConfig(level=logging.INFO)
```

## 📋 Debugging Checklist

- [ ] Environment variables set correctly
- [ ] Service account credentials loaded
- [ ] API endpoints accessible
- [ ] Request payload valid
- [ ] Response structure expected
- [ ] Error handling working
- [ ] Logging configured properly

## 🆘 Getting Help

If you encounter issues:

1. Check the logs for detailed error messages
2. Use the debug script to isolate the problem
3. Verify your Google Cloud configuration
4. Test with minimal data first
5. Check API quotas and billing

## 🎯 Pro Tips

1. **Start Small**: Test with 1-2 locations first
2. **Use Future Dates**: Avoid timestamp validation issues
3. **Check Network**: Ensure internet connectivity
4. **Monitor Quotas**: Watch API usage limits
5. **Save Responses**: Log successful responses for reference 