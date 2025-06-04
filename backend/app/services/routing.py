import json
import requests
from app.core.config import settings
from app.services.geocoding import geocode_address
from datetime import datetime, timezone
from app.core.logging import get_logger

logger = get_logger(__name__)

def build_cfr_payload(locations_with_windows):
    """
    Build payload for Google Routes API
    """
    origin = {
        "location": {
            "latLng": {
                "latitude": START_LAT,
                "longitude": START_LNG
            }
        }
    }
    
    destination = {
        "location": {
            "latLng": {
                "latitude": START_LAT,  # Return to start
                "longitude": START_LNG
            }
        }
    }
    
    intermediates = []
    for i, loc in enumerate(locations_with_windows):
        intermediates.append({
            "location": {
                "latLng": {
                    "latitude": loc["lat"],
                    "longitude": loc["lng"]
                }
            }
        })

    return {
        "origin": origin,
        "destination": destination,
        "intermediates": intermediates,
        "routingPreference": "TRAFFIC_AWARE",
        "departureTime": datetime.fromtimestamp(START_TS, timezone.utc).isoformat(),
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False
        },
        "languageCode": "en-US",
        "units": "METRIC",
        "travel_mode": 1  # 1 = DRIVING in the RouteTravelMode enum
    }

def call_cfr_api(request_payload, api_key):
    try:
        logger.info("Calling Google Routes API")
        logger.debug(f"Request payload: {json.dumps(request_payload, indent=2)}")
        
        response = requests.post(
            "https://routes.googleapis.com/directions/v2:computeRoutes",
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": api_key,
                "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.legs.duration,routes.legs.distanceMeters,routes.legs.steps"
            },
            data=json.dumps(request_payload)
        )
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully received response from Routes API")
        logger.debug(f"API Response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {str(e)}", exc_info=True)
        if hasattr(e.response, 'text'):
            logger.error(f"API Error details: {e.response.text}")
        raise

def basic_route_optimizer(houses):
    # Placeholder for basic greedy algorithm
    return sorted(houses, key=lambda h: h["address"])

def plan_optimized_route(houses, start_info):
    try:
        logger.info(f"Starting route optimization for {len(houses)} houses")
        locations = []
        for h in houses:
            logger.info(f"Geocoding address: {h.address}")
            lat, lng = geocode_address(h.address)
            locations.append({
                "lat": lat,
                "lng": lng,
                "start_ts": int(h.start_time.timestamp()),
                "end_ts": int(h.end_time.timestamp()),
                "visit_duration_sec": h.duration_minutes * 60
            })
            logger.debug(f"Geocoded location: lat={lat}, lng={lng}")

        global START_LAT, START_LNG, START_TS, END_TS
        START_LAT = start_info["start_lat"]
        START_LNG = start_info["start_lng"]
        START_TS = start_info["start_ts"]
        END_TS = start_info["end_ts"]

        payload = build_cfr_payload(locations)
        logger.info("Built Routes API payload")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        raw_response = call_cfr_api(payload, settings.GOOGLE_MAPS_API_KEY)
        logger.info("Processing API response")

        route_plan = []
        if "routes" in raw_response and len(raw_response["routes"]) > 0:
            route = raw_response["routes"][0]
            current_time = START_TS
            for i, leg in enumerate(route["legs"]):
                if i < len(locations):  # Skip the last leg (return to start)
                    address = houses[i].address
                    leg_duration = int(leg["duration"].replace("s", ""))
                    arrival = datetime.fromtimestamp(current_time, timezone.utc)
                    departure = datetime.fromtimestamp(current_time + locations[i]["visit_duration_sec"], timezone.utc)
                    route_plan.append({
                        "address": address,
                        "arrival_time": arrival,
                        "departure_time": departure
                    })
                    current_time += leg_duration + locations[i]["visit_duration_sec"]
                    logger.debug(f"Processed visit: {address}")

        logger.info("Successfully created route plan")
        return {"route": route_plan}
    except Exception as e:
        logger.error(f"Error in route optimization: {str(e)}", exc_info=True)
        raise