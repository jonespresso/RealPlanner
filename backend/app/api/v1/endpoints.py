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
        
        result = plan_optimized_route(
            houses=request.houses,
            start_address=request.start_address,
            destination_address=request.destination_address
        )
        logger.info("Successfully generated route plan")
        return result
    except Exception as e:
        logger.error(f"Error planning route: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))