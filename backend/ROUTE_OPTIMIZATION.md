# Route Optimization Implementation

## Overview

RealPlanner uses a **dual-API approach** for route optimization:

1. **Primary**: Google Route Optimization API (enterprise-grade optimization)
2. **Fallback**: Google Routes API with waypoint optimization (simpler, API key-based)

This ensures reliable optimization even when OAuth setup is complex.

## How It Works

### 1. Primary: Google Route Optimization API

The app first attempts to use Google's Route Optimization API which is specifically designed for:
- **Vehicle Fleet Optimization**: Assigns tasks and routes to vehicles optimally
- **Complex Constraints**: Handles time windows, capacity limits, and preferences
- **Advanced Algorithms**: Uses sophisticated optimization algorithms
- **Real-time Traffic**: Incorporates current traffic conditions

### 2. Fallback: Google Routes API with Waypoint Optimization

If the Route Optimization API fails (due to authentication or other issues), the app automatically falls back to:
- **Google Routes API** with `optimizeWaypointOrder: true`
- **API Key Authentication**: Simpler setup, no OAuth required
- **Good Optimization**: Still provides effective route optimization
- **Reliable Fallback**: Ensures the app always works

### 3. Optimization Process

1. **Geocoding**: All addresses are converted to lat/lng coordinates
2. **Primary Attempt**: Try Route Optimization API with OAuth authentication
3. **Fallback**: If primary fails, use Routes API with API key
4. **Response Processing**: Extract optimized route and timing information

### 4. Key Features

- **Dual Reliability**: Two optimization methods ensure the app always works
- **Advanced Optimization**: Route Optimization API when available
- **Simple Setup**: Routes API fallback for easy deployment
- **Time Window Support**: Respects property open hours and visit durations
- **Traffic-Aware**: Uses real-time traffic data for accurate timing

## API Structure

### Route Optimization API (Primary)
**Shipments (Houses):**
```json
{
  "deliveries": [{
    "arrivalLocation": {"latLng": {"latitude": 37.7749, "longitude": -122.4194}},
    "timeWindows": [{"startTime": "2024-01-15T09:00:00Z", "endTime": "2024-01-15T17:00:00Z"}]
  }],
  "label": "House 1"
}
```

**Vehicle (Realtor's Car):**
```json
{
  "startLocation": {"latLng": {"latitude": 37.7749, "longitude": -122.4194}},
  "endLocation": {"latLng": {"latitude": 37.7749, "longitude": -122.4194}},
  "travelMode": 1
}
```

### Routes API (Fallback)
**Waypoints with Optimization:**
```json
{
  "origin": {"location": {"latLng": {"latitude": 37.7749, "longitude": -122.4194}}},
  "destination": {"location": {"latLng": {"latitude": 37.7749, "longitude": -122.4194}}},
  "intermediates": [...],
  "optimizeWaypointOrder": true
}
```

## API Response Structure

### Route Optimization API Response
- `routes[0].visits[]`: Optimized visit sequence with timing
- `routes[0].vehicleIndex`: Which vehicle performs the route
- `routes[0].metrics`: Total distance, duration, and cost metrics

### Routes API Response
- `routes[0].optimizedIntermediateWaypointIndex`: Array showing the optimal visit order
- `routes[0].legs[]`: Detailed route segments with timing and distance
- `routes[0].duration`: Total route duration

## Example

**Input Houses (in order):**
1. 123 Main St, San Francisco, CA
2. 456 Oak Ave, San Francisco, CA  
3. 789 Pine St, San Francisco, CA

**Optimized Output (both APIs):**
- Visit 2, then 1, then 3 (optimization algorithm determines the most efficient order)
- Each stop includes precise arrival/departure times
- Original vs optimized order is tracked for reference

## Benefits

- **Reliability**: Dual API approach ensures the app always works
- **Flexibility**: Can use advanced features when available, fallback when needed
- **Easy Deployment**: Routes API fallback requires only API key
- **Professional Results**: Both APIs provide good optimization quality
- **Future-Proof**: Can upgrade to full Route Optimization API when ready

## Technical Implementation

- **Backend**: FastAPI service with dual API integration
- **Authentication**: OAuth 2.0 for Route Optimization API, API key for Routes API
- **Error Handling**: Automatic fallback with graceful degradation
- **Response Processing**: Unified handling of both API responses
- **Logging**: Clear indication of which API is being used

## Configuration Requirements

### Minimum Setup (Routes API only)
- **Google Maps API Key**: For Routes API fallback
- **Google Cloud Project ID**: For API access

### Full Setup (Route Optimization API + Routes API)
- **Google Cloud Project ID**: Required for both APIs
- **OAuth 2.0 Credentials**: Service account for Route Optimization API
- **API Enablement**: Both APIs enabled in Google Cloud Console

## Future Enhancements

- Multi-vehicle routing (multiple realtors)
- Capacity constraints (vehicle limits)
- Priority-based optimization
- Integration with calendar systems
- Real-time route updates 