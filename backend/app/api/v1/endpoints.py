from fastapi import APIRouter
from app.schemas.route import RoutePlanRequest, RoutePlanResponse
from app.services.routing import plan_optimized_route
from app.core.config import settings

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.post("/plan-route", response_model=RoutePlanResponse)
def plan_route(request: RoutePlanRequest):
    start_info = {
        "start_lat": 47.6062,
        "start_lng": -122.3321,
        "start_ts": int(request.houses[0].start_time.timestamp()) - 1800,
        "end_ts": int(request.houses[-1].end_time.timestamp()) + 1800,
    }
    return plan_optimized_route(request.houses, start_info, settings)