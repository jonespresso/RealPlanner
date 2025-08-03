from app.core.logging import get_logger
from app.services.geocoding import geocode_address
from app.services.route_optimization_api import optimize_route as route_optimization_api_optimize
from app.services.routes_api import optimize_route as routes_api_optimize
from app.services.greedy_optimizer import optimize_route as greedy_optimize

logger = get_logger(__name__)

def plan_optimized_route(houses, start_address, destination_address=None):
    """
    Plan optimized route using multiple fallback methods:
    1. Google Route Optimization API (best, respects time windows)
    2. Google Routes API (good, but doesn't respect time windows)
    3. Greedy Algorithm (basic, doesn't respect time windows)
    """
    try:
        logger.info(f"Starting route optimization for {len(houses)} houses")
        
        # Geocode start location
        logger.info(f"Geocoding start address: {start_address}")
        start_lat, start_lng = geocode_address(start_address)
        start_location = {"lat": start_lat, "lng": start_lng}
        logger.debug(f"Start location: lat={start_lat}, lng={start_lng}")
        
        # Geocode destination if provided
        destination_location = None
        if destination_address:
            logger.info(f"Geocoding destination address: {destination_address}")
            dest_lat, dest_lng = geocode_address(destination_address)
            destination_location = {"lat": dest_lat, "lng": dest_lng}
            logger.debug(f"Destination location: lat={dest_lat}, lng={dest_lng}")
        
        # Geocode intermediate locations
        locations = []
        for i, h in enumerate(houses):
            logger.info(f"Geocoding address: {h.address}")
            lat, lng = geocode_address(h.address)
            locations.append({
                "lat": lat,
                "lng": lng,
                "start_ts": int(h.start_time.timestamp()),
                "end_ts": int(h.end_time.timestamp()),
                "visit_duration_sec": h.duration_minutes * 60,
                "original_index": i,  # Keep track of original order
                "house_data": h  # Store the original house data
            })
            logger.debug(f"Geocoded location: lat={lat}, lng={lng}")

        start_ts = int(houses[0].start_time.timestamp())

        # Try optimization methods in order of preference
        optimization_methods = [
            ("Google Route Optimization API", route_optimization_api_optimize),
            ("Google Routes API", routes_api_optimize),
            ("Greedy Algorithm", greedy_optimize)
        ]

        for method_name, optimize_func in optimization_methods:
            try:
                logger.info(f"Attempting route optimization with {method_name}")
                route_plan = optimize_func(locations, start_location, destination_location, start_ts)
                
                if route_plan:
                    logger.info(f"Successfully created route plan using {method_name}")
                    return {"route": route_plan}
                else:
                    logger.warning(f"{method_name} returned empty route plan")
                    
            except Exception as e:
                logger.warning(f"{method_name} failed: {str(e)}")
                continue

        # If all methods failed
        raise Exception("All route optimization methods failed")

    except Exception as e:
        logger.error(f"Error in route optimization: {str(e)}", exc_info=True)
        raise