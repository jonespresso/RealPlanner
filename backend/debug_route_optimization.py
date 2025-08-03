#!/usr/bin/env python3
"""
Debug script for route optimization API
This script allows you to debug the route optimization API step by step
"""
import sys
import os
from datetime import datetime, timezone, timedelta

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.route_optimization_api import (
    get_oauth_token,
    build_payload,
    call_api,
    process_response,
    optimize_route
)
from app.schemas.route import HouseVisit
from app.core.logging import get_logger

logger = get_logger(__name__)

def debug_route_optimization():
    """Debug the route optimization API step by step"""
    
    print("🔍 Starting Route Optimization API Debug Session")
    print("=" * 60)
    
    # Use a future date to avoid timestamp errors
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    
    # Sample house visits for debugging
    houses = [
        HouseVisit(
            address="123 Main St, San Francisco, CA",
            start_time=tomorrow.replace(hour=9, minute=0, second=0, microsecond=0),
            end_time=tomorrow.replace(hour=17, minute=0, second=0, microsecond=0),
            duration_minutes=30
        ),
        HouseVisit(
            address="456 Oak Ave, San Francisco, CA", 
            start_time=tomorrow.replace(hour=9, minute=0, second=0, microsecond=0),
            end_time=tomorrow.replace(hour=17, minute=0, second=0, microsecond=0),
            duration_minutes=30
        )
    ]
    
    start_address = "100 Market St, San Francisco, CA"
    
    try:
        # Step 1: Debug OAuth token generation
        print("\n🔑 Step 1: Testing OAuth Token Generation")
        print("-" * 40)
        token = get_oauth_token()
        if token:
            print(f"✅ OAuth token obtained: {token[:20]}...")
        else:
            print("❌ Failed to get OAuth token")
            return
        
        # Step 2: Debug payload building
        print("\n📦 Step 2: Testing Payload Building")
        print("-" * 40)
        
        # Convert houses to locations format
        from app.services.geocoding import geocode_address
        
        start_lat, start_lng = geocode_address(start_address)
        start_location = {"lat": start_lat, "lng": start_lng}
        
        locations = []
        for h in houses:
            lat, lng = geocode_address(h.address)
            locations.append({
                "lat": lat,
                "lng": lng,
                "start_ts": int(h.start_time.timestamp()),
                "end_ts": int(h.end_time.timestamp()),
                "visit_duration_sec": h.duration_minutes * 60,
                "original_index": len(locations),
                "house_data": h
            })
        
        start_ts = int(houses[0].start_time.timestamp())
        
        payload = build_payload(locations, start_location, None, start_ts)
        print(f"✅ Payload built successfully")
        print(f"   - {len(payload['model']['shipments'])} shipments")
        print(f"   - {len(payload['model']['vehicles'])} vehicles")
        print(f"   - Global time window: {payload['model']['globalStartTime']} to {payload['model']['globalEndTime']}")
        
        # Step 3: Debug API call
        print("\n🌐 Step 3: Testing API Call")
        print("-" * 40)
        response = call_api(payload)
        print(f"✅ API call successful")
        print(f"   - Response keys: {list(response.keys())}")
        
        # Step 4: Debug response processing
        print("\n🔄 Step 4: Testing Response Processing")
        print("-" * 40)
        route_plan = process_response(response, locations)
        print(f"✅ Response processed successfully")
        print(f"   - Generated {len(route_plan)} route stops")
        
        # Step 5: Debug full optimization
        print("\n🚀 Step 5: Testing Full Optimization")
        print("-" * 40)
        final_route = optimize_route(locations, start_location, None, start_ts)
        print(f"✅ Full optimization successful")
        print(f"   - Final route has {len(final_route)} stops")
        
        # Display the optimized route
        print("\n📋 Optimized Route:")
        print("-" * 40)
        for i, stop in enumerate(final_route):
            print(f"{i+1}. {stop['address']}")
            print(f"   Arrival: {stop['arrival_time']}")
            print(f"   Departure: {stop['departure_time']}")
            print(f"   Original order: {stop['original_order']}, Optimized order: {stop['optimized_order']}")
            print()
        
        print("🎉 Debug session completed successfully!")
        
    except Exception as e:
        print(f"❌ Debug session failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_route_optimization() 