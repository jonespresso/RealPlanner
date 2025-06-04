from fastapi import APIRouter, HTTPException
from app.schemas.route import RoutePlanRequest, RoutePlanResponse
from app.services.routing import plan_optimized_route
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.post("/plan-route", response_model=RoutePlanResponse)
def plan_route(request: RoutePlanRequest):
    try:
        logger.info(f"Received route planning request for {len(request.houses)} houses")
        logger.debug(f"Request details: {request.model_dump()}")
        
        start_info = {
            "start_lat": 47.6062,
            "start_lng": -122.3321,
            "start_ts": int(request.houses[0].start_time.timestamp()) - 1800,
            "end_ts": int(request.houses[-1].end_time.timestamp()) + 1800,
        }
        logger.info(f"Calculated start_info: {start_info}")
        
        result = plan_optimized_route(request.houses, start_info)
        logger.info("Successfully generated route plan")
        return result
    except Exception as e:
        logger.error(f"Error planning route: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))