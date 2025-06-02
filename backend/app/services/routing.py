import json
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from app.services.geocoding import geocode_address
from datetime import datetime, UTC

def build_cfr_payload(locations_with_windows):
    """
    locations_with_windows: List of dicts like:
    [
        {"lat": ..., "lng": ..., "start": "2025-06-01T10:00:00Z", "end": "2025-06-01T11:00:00Z", "visit_duration_sec": 1200}
    ]
    """
    jobs = []
    for i, loc in enumerate(locations_with_windows):
        jobs.append({
            "id": f"house-{i+1}",
            "tasks": [{
                "arrival_location": {
                    "latitude": loc["lat"],
                    "longitude": loc["lng"]
                },
                "duration": {
                    "seconds": loc["visit_duration_sec"]
                },
                "time_windows": [{
                    "start_time": {"seconds": int(loc["start_ts"])},
                    "end_time": {"seconds": int(loc["end_ts"])}
                }]
            }]
        })

    vehicle = {
        "id": "realtor-car",
        "start_location": {
            "latitude": START_LAT,
            "longitude": START_LNG
        },
        "start_time_windows": [{
            "start_time": {"seconds": START_TS}
        }],
        "end_time_windows": [{
            "end_time": {"seconds": END_TS}
        }]
    }

    return {
        "model": {
            "vehicles": [vehicle],
            "jobs": jobs
        }
    }

def call_cfr_api(request_payload, service_account_path):
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    credentials = service_account.Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
    authed_session = Request()
    credentials.refresh(authed_session)
    token = credentials.token

    response = requests.post(
        "https://fleetengine.googleapis.com/v1/fleetRouting:optimizeTours",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        data=json.dumps(request_payload)
    )
    return response.json()

def basic_route_optimizer(houses):
    # Placeholder for basic greedy algorithm
    return sorted(houses, key=lambda h: h["address"])

def plan_optimized_route(houses, start_info, settings):
    """
    - houses: list of dicts with address, start_time, end_time, duration
    - start_info: dict with start_lat, start_lng, start_ts, end_ts
    - settings: config with API key and service account path
    """
    # Step 1: Geocode all house addresses (call geocode_address from services/geocoding.py)
    # Step 2: Build full CFR payload (use build_cfr_payload)
    # Step 3: Call CFR API (use call_cfr_api)
    # Step 4: Parse and return response in a structured format
    locations = []
    for h in houses:
        lat, lng = geocode_address(h.address)
        locations.append({
            "lat": lat,
            "lng": lng,
            "start_ts": int(h.start_time.timestamp()),
            "end_ts": int(h.end_time.timestamp()),
            "visit_duration_sec": h.duration_minutes * 60
        })

    global START_LAT, START_LNG, START_TS, END_TS
    START_LAT = start_info["start_lat"]
    START_LNG = start_info["start_lng"]
    START_TS = start_info["start_ts"]
    END_TS = start_info["end_ts"]

    payload = build_cfr_payload(locations)
    raw_response = call_cfr_api(payload, settings.GOOGLE_APPLICATION_CREDENTIALS_PATH)

    route_plan = []
    for visit in raw_response["routes"][0]["visits"]:
        task = visit.get("shipmentLabel") or visit.get("visitRequestLabel") or "Unknown"
        arrival = datetime.fromtimestamp(visit["arrivalTime"]["seconds"], UTC)
        departure = datetime.fromtimestamp(visit["departureTime"]["seconds"], UTC)
        route_plan.append({
            "address": task,
            "arrival_time": arrival,
            "departure_time": departure
        })

    return {"route": route_plan}