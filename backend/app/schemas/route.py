from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class RouteOptimizationParams(BaseModel):
    """Parameters required for route optimization algorithms"""
    locations: List[Dict[str, Any]]
    start_location: Dict[str, float]
    destination_location: Optional[Dict[str, float]] = None
    global_start_time: datetime
    global_end_time: datetime

class HouseVisit(BaseModel):
    address: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int = 20

class RoutePlanRequest(BaseModel):
    start_address: str
    destination_address: Optional[str] = None
    houses: List[HouseVisit]
    global_start_time: datetime
    global_end_time: datetime

class StopAssignment(BaseModel):
    address: str
    arrival_time: datetime
    departure_time: datetime
    original_order: Optional[int] = None
    optimized_order: Optional[int] = None
    time_window_violation: Optional[bool] = None

class RoutePlanResponse(BaseModel):
    route: List[StopAssignment]
    optimization_method: str

class CurlCommandResponse(BaseModel):
    route_optimization_api: str
    routes_api: str
    setup_instructions: Dict[str, Dict[str, str]]