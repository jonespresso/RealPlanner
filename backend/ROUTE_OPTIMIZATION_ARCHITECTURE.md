# Route Optimization Architecture

## Overview

RealPlanner now uses a **modular fallback architecture** for route optimization, with each optimization method in its own dedicated file. This ensures reliability and makes it easy to add new optimization methods.

## Architecture

```
app/services/
├── routing.py                    # Main orchestrator
├── route_optimization_api.py     # Google Route Optimization API
├── routes_api.py                 # Google Routes API (fallback)
└── greedy_optimizer.py           # Greedy algorithm (final fallback)
```

## Fallback Chain

The system tries optimization methods in order of preference:

1. **Google Route Optimization API** (Best)
   - ✅ Respects time windows
   - ✅ Advanced optimization algorithms
   - ❌ Requires OAuth 2.0 setup
   - ❌ More complex configuration

2. **Google Routes API** (Good)
   - ✅ Simple API key authentication
   - ✅ Good route optimization
   - ❌ Does NOT respect time windows
   - ⚠️ Includes time window validation warnings

3. **Greedy Algorithm** (Basic)
   - ✅ No external dependencies
   - ✅ Always works
   - ❌ Basic optimization only
   - ❌ Does NOT respect time windows
   - ⚠️ Includes time window validation warnings

## How It Works

### Main Orchestrator (`routing.py`)

```python
def plan_optimized_route(houses, start_address, destination_address=None):
    # 1. Geocode all addresses
    # 2. Try each optimization method in order
    # 3. Return first successful result
    # 4. Raise exception if all methods fail
```

### Optimization Methods

Each optimization method implements the same interface:

```python
def optimize_route(locations, start_location, destination_location=None, start_ts=None):
    # Returns: List of route stops with timing information
    # Raises: Exception if optimization fails
```

## Time Window Handling

### Route Optimization API
- **Respects time windows** natively
- No violations possible
- `time_window_violation: False`

### Routes API & Greedy Algorithm
- **Does NOT respect time windows**
- Validates and warns about violations
- `time_window_violation: True` for violations
- Logs detailed warnings

## Response Format

All methods return the same response format:

```json
{
  "route": [
    {
      "address": "123 Main St, San Francisco, CA",
      "arrival_time": "2025-06-21T09:00:00+00:00",
      "departure_time": "2025-06-21T09:30:00+00:00",
      "original_order": 0,
      "optimized_order": 0,
      "time_window_violation": false,
      "method": "routes_api"
    }
  ]
}
```

## Adding New Optimization Methods

To add a new optimization method:

1. **Create new file**: `app/services/new_optimizer.py`
2. **Implement interface**:
   ```python
   def optimize_route(locations, start_location, destination_location=None, start_ts=None):
       # Your optimization logic here
       return route_plan
   ```
3. **Add to fallback chain** in `routing.py`:
   ```python
   from app.services.new_optimizer import optimize_route as new_optimizer_optimize
   
   optimization_methods = [
       ("Google Route Optimization API", route_optimization_api_optimize),
       ("Google Routes API", routes_api_optimize),
       ("New Optimizer", new_optimizer_optimize),  # Add here
       ("Greedy Algorithm", greedy_optimize)
   ]
   ```

## Configuration Requirements

### Minimum Setup (Routes API + Greedy)
```env
GOOGLE_MAPS_API_KEY=your_api_key
GOOGLE_CLOUD_PROJECT_ID=your_project_id
```

### Full Setup (All Methods)
```env
GOOGLE_MAPS_API_KEY=your_api_key
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_SERVICE_ACCOUNT_KEY={"type": "service_account", ...}
```

## Benefits

- **Reliability**: Always works, even if some APIs fail
- **Modularity**: Easy to add/remove optimization methods
- **Transparency**: Clear logging of which method was used
- **Flexibility**: Can configure which methods to use
- **Maintainability**: Each method is isolated and testable

## Testing

Test the fallback chain:

```bash
# Test with minimal setup (Routes API + Greedy)
python3 tests/test_optimization.py

# Test with full setup (all methods)
# (Requires OAuth credentials for Route Optimization API)
```

## Logging

The system provides detailed logging:

```
INFO: Attempting route optimization with Google Route Optimization API
WARNING: Google Route Optimization API failed: No OAuth token available
INFO: Attempting route optimization with Google Routes API
WARNING: Routes API does NOT support time window constraints - will validate manually
INFO: Successfully created route plan using Google Routes API
```

## Future Enhancements

- **Custom TSP Solver**: Add advanced constraint satisfaction
- **Multi-vehicle Support**: Route multiple realtors
- **Real-time Updates**: Dynamic route adjustments
- **Performance Metrics**: Compare optimization quality
- **Configuration UI**: Enable/disable methods via API 