import requests
from app.core.config import settings

def geocode_address(address: str):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": settings.GOOGLE_MAPS_API_KEY}
    response = requests.get(url, params=params).json()
    if response["status"] == "OK":
        loc = response["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    else:
        raise Exception(f"Geocoding failed: {response['status']}")