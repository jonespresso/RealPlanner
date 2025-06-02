from pydantic import BaseModel
from typing import List
from datetime import datetime

class HouseVisit(BaseModel):
    address: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int = 20

class RoutePlanRequest(BaseModel):
    houses: List[HouseVisit]

class StopAssignment(BaseModel):
    address: str
    arrival_time: datetime
    departure_time: datetime

class RoutePlanResponse(BaseModel):
    route: List[StopAssignment]