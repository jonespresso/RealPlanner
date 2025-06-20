import math
from datetime import datetime, timezone
from app.core.logging import get_logger

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
            
            # Add to route plan
            house_data = nearest["house_data"]
            arrival_time = datetime.fromtimestamp(current_time, timezone.utc)
            departure_time = datetime.fromtimestamp(current_time + nearest["visit_duration_sec"], timezone.utc)
            
            route_plan.append({
                "address": house_data.address,
                "arrival_time": arrival_time,
                "departure_time": departure_time,
                "original_order": nearest["original_index"],
                "optimized_order": len(route_plan),
                "time_window_violation": False,  # We'll check this later
                "method": "greedy_algorithm",
                "location_data": nearest  # Store the full location data for validation
            })
            
            # Update current location and time
            current_location = nearest
            current_time += nearest["visit_duration_sec"]
            
            # Add estimated travel time to next location
            if len(unvisited_locations) > 1:
                travel_time_estimate = 15 * 60  # 15 minutes estimate
                current_time += travel_time_estimate
            
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
    """
    Validate that the route respects time windows and add warnings for violations.
    Returns route plan with time window violation flags.
    """
    logger.info("Validating time window constraints for greedy algorithm result")
    
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
            "method": "greedy_algorithm"
        })
        
        current_time += location["visit_duration_sec"]
        
        # Add travel time to next location (if not the last one)
        if i < len(route_plan) - 1:
            travel_time_estimate = 15 * 60  # 15 minutes estimate
            current_time += travel_time_estimate
    
    if violations:
        logger.warning(f"Time window violations detected: {', '.join(violations)}")
        logger.warning("Greedy algorithm does not respect time windows. Consider using Route Optimization API for time-constrained routing.")
    
    return corrected_route 