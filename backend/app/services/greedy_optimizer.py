import math
from datetime import datetime, timezone
from app.core.logging import get_logger
from app.services.time_windows import compute_schedule_with_time_windows

logger = get_logger(__name__)

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def find_nearest_neighbor(current_location, unvisited_locations):
    """Find the nearest unvisited location to the current location"""
    if not unvisited_locations:
        return None
    
    min_distance = float('inf')
    nearest_location = None
    
    for location in unvisited_locations:
        distance = calculate_distance(
            current_location["lat"], current_location["lng"],
            location["lat"], location["lng"]
        )
        if distance < min_distance:
            min_distance = distance
            nearest_location = location
    
    return nearest_location

def optimize_route(locations, start_location, destination_location=None, start_ts=None):
    """
    Optimize route using greedy nearest neighbor algorithm
    Returns optimized route plan
    """
    try:
        logger.info("Using greedy nearest neighbor algorithm for route optimization")
        logger.warning("Greedy algorithm does not respect time windows and may not be optimal")
        
        # Start from the start location
        current_location = start_location
        unvisited_locations = locations.copy()
        route_plan = []
        current_time = start_ts
        
        # Visit each location using nearest neighbor
        while unvisited_locations:
            nearest = find_nearest_neighbor(current_location, unvisited_locations)
            if not nearest:
                break

            # Estimate travel time from current_location to nearest using simple speed model
            try:
                distance_km = calculate_distance(
                    current_location["lat"], current_location["lng"],
                    nearest["lat"], nearest["lng"]
                )
                # Assume average speed 40 km/h; minimum 5 minutes to avoid zero
                travel_time_estimate = max(5 * 60, int((distance_km / 40.0) * 3600))
            except Exception:
                travel_time_estimate = 15 * 60

            # Add to route plan (times will be recomputed in validator; set reasonable placeholders)
            house_data = nearest["house_data"]
            arrival_time = datetime.fromtimestamp(current_time + travel_time_estimate, timezone.utc)
            departure_time = datetime.fromtimestamp(current_time + travel_time_estimate + nearest["visit_duration_sec"], timezone.utc)

            route_plan.append({
                "address": house_data.address,
                "arrival_time": arrival_time,
                "departure_time": departure_time,
                "original_order": nearest["original_index"],
                "optimized_order": len(route_plan),
                "time_window_violation": False,
                "method": "greedy_algorithm",
                "location_data": nearest,
                "travel_duration_sec": travel_time_estimate
            })

            # Update current location and time (travel + visit)
            current_location = nearest
            current_time += travel_time_estimate + nearest["visit_duration_sec"]

            # Remove visited location
            unvisited_locations.remove(nearest)
        
        # Validate time windows and add warnings
        corrected_route = validate_time_windows(route_plan, locations, start_ts)
        
        logger.info("Successfully created route plan using greedy algorithm")
        return corrected_route
        
    except Exception as e:
        logger.error(f"Greedy algorithm failed: {str(e)}")
        raise

def validate_time_windows(route_plan, locations, start_ts):
    return compute_schedule_with_time_windows(route_plan, start_ts, method="greedy_algorithm")