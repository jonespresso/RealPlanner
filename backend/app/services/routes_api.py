import json
import requests
from datetime import datetime, timezone
from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger(__name__)

def build_payload(locations_with_windows, start_location, destination_location=None, start_ts=None):
    """
    Build payload for Google Routes API with waypoint optimization
    Note: Routes API does NOT support time window constraints
    """
    origin = {
        "location": {
            "latLng": {
                "latitude": start_location["lat"],
                "longitude": start_location["lng"]
            }
        }
    }
    
    # Use provided destination or fall back to start location
    dest_lat = destination_location["lat"] if destination_location else start_location["lat"]
    dest_lng = destination_location["lng"] if destination_location else start_location["lng"]
    
    destination = {
        "location": {
            "latLng": {
                "latitude": dest_lat,
                "longitude": dest_lng
            }
        }
    }
    
    # Build waypoints with optimization enabled
    waypoints = []
    for i, loc in enumerate(locations_with_windows):
        waypoint = {
            "location": {
                "latLng": {
                    "latitude": loc["lat"],
                    "longitude": loc["lng"]
                }
            }
        }
        waypoints.append(waypoint)

    return {
        "origin": origin,
        "destination": destination,
        "intermediates": waypoints,
        "routingPreference": "TRAFFIC_AWARE",
        "departureTime": datetime.fromtimestamp(start_ts, timezone.utc).isoformat(),
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False
        },
        "languageCode": "en-US",
        "units": "METRIC",
        "travel_mode": 1,  # 1 = DRIVING in the RouteTravelMode enum
        "optimizeWaypointOrder": True  # Enable waypoint optimization
    }

def call_api(request_payload):
    """Call Google Routes API with waypoint optimization"""
    try:
        logger.info("Calling Google Routes API with waypoint optimization")
        logger.warning("Note: Routes API does NOT support time window constraints - will validate manually")
        logger.debug(f"Request payload: {json.dumps(request_payload, indent=2)}")
        
        response = requests.post(
            "https://routes.googleapis.com/directions/v2:computeRoutes",
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
                "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.legs.duration,routes.legs.distanceMeters,routes.legs.steps,routes.optimizedIntermediateWaypointIndex"
            },
            data=json.dumps(request_payload)
        )
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully received optimized route from Routes API")
        logger.debug(f"API Response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Routes API failed: {str(e)}", exc_info=True)
        if hasattr(e.response, 'text'):
            logger.error(f"API Error details: {e.response.text}")
        raise

def validate_time_windows(route_plan, locations, start_ts):
    """
    Validate that the route respects time windows and add warnings for violations.
    Returns route plan with time window violation flags.
    """
    logger.info("Validating time window constraints for Routes API result")
    
    corrected_route = []
    current_time = start_ts
    violations = []
    
    for i, stop in enumerate(route_plan):
        # Get location data from the stop's location_data field
        location = stop["location_data"]
        house_data = location["house_data"]
        
        # Check if arrival time is within the time window
        arrival_time = datetime.fromtimestamp(current_time, timezone.utc)
        window_start = datetime.fromtimestamp(location["start_ts"], timezone.utc)
        window_end = datetime.fromtimestamp(location["end_ts"], timezone.utc)
        
        # Check for time window violations
        time_window_violation = False
        if arrival_time < window_start:
            logger.warning(f"Arrival time {arrival_time} is before window opens {window_start} for {house_data.address}")
            time_window_violation = True
            violations.append(f"Early arrival at {house_data.address}")
        elif arrival_time > window_end:
            logger.error(f"Arrival time {arrival_time} is after window closes {window_end} for {house_data.address}")
            time_window_violation = True
            violations.append(f"Late arrival at {house_data.address}")
        
        departure_time = datetime.fromtimestamp(current_time + location["visit_duration_sec"], timezone.utc)
        
        corrected_route.append({
            "address": house_data.address,
            "arrival_time": arrival_time,
            "departure_time": departure_time,
            "original_order": location["original_index"],
            "optimized_order": i,
            "time_window_violation": time_window_violation,
            "method": "routes_api"
        })
        
        current_time += location["visit_duration_sec"]
        
        # Add travel time to next location (if not the last one)
        if i < len(route_plan) - 1:
            # Estimate travel time (this is a simplified approach)
            # In a real implementation, you'd want to get actual travel times
            travel_time_estimate = 15 * 60  # 15 minutes estimate
            current_time += travel_time_estimate
    
    if violations:
        logger.warning(f"Time window violations detected: {', '.join(violations)}")
        logger.warning("Routes API does not respect time windows. Consider using Route Optimization API for time-constrained routing.")
    
    return corrected_route

def process_response(raw_response, locations, start_ts):
    """Process Routes API response"""
    route_plan = []
    if "routes" in raw_response and len(raw_response["routes"]) > 0:
        route = raw_response["routes"][0]
        
        # Get the optimized waypoint order
        optimized_order = route.get("optimizedIntermediateWaypointIndex", list(range(len(locations))))
        logger.info(f"Optimized waypoint order: {optimized_order}")
        
        # Reorder locations based on optimization
        optimized_locations = [locations[i] for i in optimized_order]
        
        current_time = start_ts
        for i, leg in enumerate(route["legs"]):
            if i < len(optimized_locations):  # Skip the last leg (return to start/destination)
                location = optimized_locations[i]
                house_data = location["house_data"]
                leg_duration = int(leg["duration"].replace("s", ""))
                arrival = datetime.fromtimestamp(current_time, timezone.utc)
                departure = datetime.fromtimestamp(current_time + location["visit_duration_sec"], timezone.utc)
                route_plan.append({
                    "address": house_data.address,
                    "arrival_time": arrival,
                    "departure_time": departure,
                    "original_order": location["original_index"],
                    "optimized_order": i,
                    "location_data": location  # Store the full location data for validation
                })
                current_time += leg_duration + location["visit_duration_sec"]
                logger.debug(f"Processed optimized visit: {house_data.address} (original: {location['original_index']}, optimized: {i})")

    return route_plan

def optimize_route(locations, start_location, destination_location=None, start_ts=None):
    """
    Optimize route using Google Routes API with waypoint optimization
    Returns optimized route plan or raises exception if failed
    """
    try:
        payload = build_payload(locations, start_location, destination_location, start_ts)
        raw_response = call_api(payload)
        route_plan = process_response(raw_response, locations, start_ts)
        
        if not route_plan:
            raise Exception("No route plan generated from Routes API")
        
        # Validate time windows and add warnings
        corrected_route = validate_time_windows(route_plan, locations, start_ts)
        
        logger.info("Successfully created optimized route plan using Routes API (with time window validation)")
        return corrected_route
        
    except Exception as e:
        logger.error(f"Routes API optimization failed: {str(e)}")
        raise 