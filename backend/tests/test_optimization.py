#!/usr/bin/env python3
"""
Test script to verify route optimization functionality
"""
import sys
import os
from datetime import datetime, timezone, timedelta

# Add the parent directory to the Python path to import from app
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.routing import plan_optimized_route
from app.schemas.route import HouseVisit

def test_route_optimization():
    """Test the route optimization with sample data"""
    
    # Use a future date (tomorrow) to avoid timestamp errors
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    
    # Sample house visits in San Francisco area
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
        ),
        HouseVisit(
            address="789 Pine St, San Francisco, CA",
            start_time=tomorrow.replace(hour=9, minute=0, second=0, microsecond=0), 
            end_time=tomorrow.replace(hour=17, minute=0, second=0, microsecond=0),
            duration_minutes=30
        )
    ]
    
    start_address = "100 Market St, San Francisco, CA"
    
    try:
        print("Testing route optimization...")
        print(f"Input houses: {[h.address for h in houses]}")
        print(f"Start location: {start_address}")
        print(f"Visit date: {tomorrow.strftime('%Y-%m-%d')}")
        print("-" * 50)
        
        result = plan_optimized_route(houses, start_address)
        
        print("Optimized route:")
        for i, stop in enumerate(result["route"]):
            print(f"{i+1}. {stop['address']}")
            print(f"   Arrival: {stop['arrival_time']}")
            print(f"   Departure: {stop['departure_time']}")
            print(f"   Original order: {stop['original_order']}, Optimized order: {stop['optimized_order']}")
            if stop.get('method'):
                print(f"   Method: {stop['method']}")
            if stop.get('time_window_violation'):
                print(f"   ⚠️  TIME WINDOW VIOLATION")
            print()
            
        print("✅ Route optimization test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_route_optimization() 