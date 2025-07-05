import json
import requests
from datetime import datetime, timezone, timedelta
from app.core.logging import get_logger
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from app.core.config import settings

logger = get_logger(__name__)

def get_oauth_token():
    """Get OAuth 2.0 token for Google Route Optimization API"""
    try:
        # Try to use service account credentials
        service_account_info = settings.get_service_account_key()
        if service_account_info:
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
        else:
            logger.warning("No service account credentials found for Route Optimization API")
            return None
            
        credentials.refresh(Request())
        return credentials.token
    except Exception as e:
        logger.error(f"Error getting OAuth token: {e}")
        return None

def build_payload(locations_with_windows, start_location, destination_location=None, start_ts=None):
    """
    Build payload for Google Route Optimization API
    Args:
        locations_with_windows: List of locations to visit
        start_location: Dict with lat/lng of start location
        destination_location: Optional dict with lat/lng of destination. If None, returns to start location.
        start_ts: Start timestamp
    """
    # Build shipments (houses to visit)
    shipments = []
    for i, loc in enumerate(locations_with_windows):
        shipment = {
            "deliveries": [{
                "arrivalLocation": {
                    "latitude": loc["lat"],
                    "longitude": loc["lng"]
                },
                "timeWindows": [{
                    "startTime": datetime.fromtimestamp(loc["start_ts"], timezone.utc).isoformat(),
                    "endTime": datetime.fromtimestamp(loc["end_ts"], timezone.utc).isoformat()
                }]
            }],
            "label": f"House {i+1}",
            "penaltyCost": 0  # No penalty for missing visits
        }
        shipments.append(shipment)

    # Build vehicle (realtor's car)
    vehicle_start_location = {
        "latitude": start_location["lat"],
        "longitude": start_location["lng"]
    }
    
    vehicle_end_location = vehicle_start_location
    if destination_location:
        vehicle_end_location = {
            "latitude": destination_location["lat"],
            "longitude": destination_location["lng"]
        }

    vehicle = {
        "startLocation": vehicle_start_location,
        "endLocation": vehicle_end_location,
        "travelMode": 1,  # DRIVING
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False
        }
    }

    # Compute global time window
    earliest_start = min(loc["start_ts"] for loc in locations_with_windows)
    latest_end = max(loc["end_ts"] for loc in locations_with_windows)
    global_start_time = datetime.fromtimestamp(earliest_start, timezone.utc).isoformat()
    global_end_time = datetime.fromtimestamp(latest_end, timezone.utc).isoformat()

    return {
        "parent": f"projects/{settings.GOOGLE_CLOUD_PROJECT_ID}",
        "model": {
            "globalStartTime": global_start_time,
            "globalEndTime": global_end_time,
            "shipments": shipments,
            "vehicles": [vehicle]
        },
        "searchMode": 1,  # GLOBAL_MODE for best optimization
        "timeout": "60s"  # Allow up to 60 seconds for optimization
    }

def call_api(request_payload):
    """Call Google Route Optimization API"""
    try:
        logger.info("Calling Google Route Optimization API")
        logger.debug(f"Request payload: {json.dumps(request_payload, indent=2)}")
        
        # Get OAuth token
        auth_token = get_oauth_token()
        if not auth_token:
            raise Exception("No OAuth token available for Route Optimization API")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        
        response = requests.post(
            f"https://routeoptimization.googleapis.com/v1/projects/{settings.GOOGLE_CLOUD_PROJECT_ID}:optimizeTours",
            headers=headers,
            data=json.dumps(request_payload)
        )
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully received optimized route from Route Optimization API")
        logger.debug(f"API Response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Route Optimization API failed: {str(e)}", exc_info=True)
        if hasattr(e.response, 'text'):
            logger.error(f"API Error details: {e.response.text}")
        raise

def process_response(raw_response, locations):
    """Process Route Optimization API response"""
    route_plan = []
    if "routes" in raw_response and len(raw_response["routes"]) > 0:
        route = raw_response["routes"][0]
        
        # Process the optimized route
        for i, visit in enumerate(route.get("visits", [])):
            if "shipmentIndex" in visit:
                shipment_index = visit["shipmentIndex"]
                if shipment_index < len(locations):
                    location = locations[shipment_index]
                    house_data = location["house_data"]
                    
                    # Extract timing information
                    arrival_time = datetime.fromisoformat(visit["startTime"].replace("Z", "+00:00"))
                    departure_time = arrival_time + timedelta(seconds=location["visit_duration_sec"])
                    
                    route_plan.append({
                        "address": house_data.address,
                        "arrival_time": arrival_time,
                        "departure_time": departure_time,
                        "original_order": location["original_index"],
                        "optimized_order": i,
                        "time_window_violation": False,  # Route Optimization API respects time windows
                        "method": "route_optimization_api"
                    })
                    logger.debug(f"Processed optimized visit: {house_data.address} (original: {location['original_index']}, optimized: {i})")
    
    return route_plan

def optimize_route(locations, start_location, destination_location=None, start_ts=None):
    """
    Optimize route using Google Route Optimization API
    Returns optimized route plan or raises exception if failed
    """
    try:
        payload = build_payload(locations, start_location, destination_location, start_ts)
        raw_response = call_api(payload)
        route_plan = process_response(raw_response, locations)
        
        if not route_plan:
            raise Exception("No route plan generated from Route Optimization API")
            
        logger.info("Successfully created optimized route plan using Route Optimization API")
        return route_plan
        
    except Exception as e:
        logger.error(f"Route Optimization API optimization failed: {str(e)}")
        raise 