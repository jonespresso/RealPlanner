from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class HouseVisit(BaseModel):
    address: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int = 20

class RoutePlanRequest(BaseModel):
    start_address: str
    destination_address: Optional[str] = None
    houses: List[HouseVisit]

class StopAssignment(BaseModel):
    address: str
    arrival_time: datetime
    departure_time: datetime
    original_order: Optional[int] = None
    optimized_order: Optional[int] = None
    time_window_violation: Optional[bool] = None
    method: Optional[str] = None

class RoutePlanResponse(BaseModel):
    route: List[StopAssignment]

class CurlCommandResponse(BaseModel):
    route_optimization_api: str
    routes_api: str
    setup_instructions: Dict[str, Dict[str, str]]