import json
from datetime import datetime, timezone
from app.core.config import settings
from app.services.geocoding import geocode_address
from app.services.google.route_optimization_api import build_payload as build_route_optimization_payload
from app.services.google.routes_api import build_payload as build_routes_api_payload
from app.schemas.route import RouteOptimizationParams
from app.core.logging import get_logger

logger = get_logger(__name__)

def generate_curl_commands(request_data):
    """
    Generate curl commands for both Google APIs using the same request construction logic
    """
    try:
        # Convert request data to the format expected by the payload builders
        houses = request_data.houses
        start_address = request_data.start_address
        destination_address = request_data.destination_address
        
        # Geocode addresses
        start_lat, start_lng = geocode_address(start_address)
        start_location = {"lat": start_lat, "lng": start_lng}
        
        destination_location = None
        if destination_address:
            dest_lat, dest_lng = geocode_address(destination_address)
            destination_location = {"lat": dest_lat, "lng": dest_lng}
        
        # Build locations array (same format used by both APIs)
        locations = []
        for h in houses:
            lat, lng = geocode_address(h.address)
            # Convert datetime objects to timestamps
            start_ts = int(h.start_time.timestamp())
            end_ts = int(h.end_time.timestamp())
            locations.append({
                "lat": lat,
                "lng": lng,
                "start_ts": start_ts,
                "end_ts": end_ts,
                "visit_duration_sec": h.duration_minutes * 60,
                "original_index": len(locations),
                "house_data": h
            })
        
        # Create optimization parameters object
        optimization_params = RouteOptimizationParams(
            locations=locations,
            start_location=start_location,
            destination_location=destination_location,
            global_start_time=request_data.global_start_time,
            global_end_time=request_data.global_end_time
        )
        
        # Generate Route Optimization API curl command
        route_optimization_payload = build_route_optimization_payload(optimization_params)
        
        route_optimization_curl = f"""curl -X POST "https://routeoptimization.googleapis.com/v1/projects/{settings.GOOGLE_CLOUD_PROJECT_ID}:optimizeTours" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_OAUTH_TOKEN" \\
  -d '{json.dumps(route_optimization_payload, indent=2)}'"""
        
        # Generate Routes API curl command
        routes_api_payload = build_routes_api_payload(optimization_params)
        
        routes_api_curl = f"""curl -X POST "https://routes.googleapis.com/directions/v2:computeRoutes" \\
  -H "Content-Type: application/json" \\
  -H "X-Goog-Api-Key: YOUR_GOOGLE_MAPS_API_KEY" \\
  -H "X-Goog-FieldMask: routes.duration,routes.distanceMeters,routes.legs.duration,routes.legs.distanceMeters,routes.legs.steps,routes.optimizedIntermediateWaypointIndex" \\
  -d '{json.dumps(routes_api_payload, indent=2)}'"""
        
        return {
            "route_optimization_api": route_optimization_curl,
            "routes_api": routes_api_curl,
            "setup_instructions": {
                "route_optimization_api": {
                    "oauth_token": "Get OAuth token using: gcloud auth print-access-token",
                    "project_id": f"Replace YOUR_PROJECT_ID with: {settings.GOOGLE_CLOUD_PROJECT_ID}",
                    "requirements": "Requires service account with Route Optimization API enabled"
                },
                "routes_api": {
                    "api_key": "Replace YOUR_GOOGLE_MAPS_API_KEY with your Google Maps API key",
                    "requirements": "Requires Routes API enabled in Google Cloud Console"
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating curl commands: {str(e)}", exc_info=True)
        raise Exception(f"Failed to generate curl commands: {str(e)}") 