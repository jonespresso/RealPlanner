from datetime import datetime, timezone
from typing import Dict, List
from app.core.logging import get_logger

logger = get_logger(__name__)

def compute_schedule_with_time_windows(route_plan: List[Dict], start_ts: int, method: str) -> List[Dict]:
    """
    Compute arrival/departure schedule and annotate time window compliance for optimizers
    that do not natively enforce windows.

    Input requirements per stop in route_plan:
      - location_data: dict with start_ts, end_ts, visit_duration_sec, original_index, house_data
      - travel_duration_sec: seconds of travel from previous point to this stop (0 if first)
      - optimized_order: integer order
    Returns a new list of stops with address, arrival/departure, original/optimized order,
    violation flag, and method name.
    """
    corrected_route: List[Dict] = []
    current_time = start_ts
    violations: List[str] = []

    for i, stop in enumerate(route_plan):
        location = stop.get("location_data")
        if not location:
            # Pass-through if insufficient data to validate
            corrected_route.append({
                **stop,
                "time_window_violation": None,
                "method": method,
            })
            continue

        house_data = location["house_data"]
        travel_duration_sec = int(stop.get("travel_duration_sec", 0))
        arrival_epoch = current_time + travel_duration_sec

        arrival_time = datetime.fromtimestamp(arrival_epoch, timezone.utc)
        window_start = datetime.fromtimestamp(location["start_ts"], timezone.utc)
        window_end = datetime.fromtimestamp(location["end_ts"], timezone.utc)

        time_window_violation = False
        if arrival_time < window_start:
            logger.warning(
                f"Arrival time {arrival_time} is before window opens {window_start} for {house_data.address}"
            )
            time_window_violation = True
            violations.append(f"Early arrival at {house_data.address}")
        elif arrival_time > window_end:
            logger.error(
                f"Arrival time {arrival_time} is after window closes {window_end} for {house_data.address}"
            )
            time_window_violation = True
            violations.append(f"Late arrival at {house_data.address}")

        departure_time = datetime.fromtimestamp(
            arrival_epoch + location["visit_duration_sec"], timezone.utc
        )

        corrected_route.append({
            "address": house_data.address,
            "arrival_time": arrival_time,
            "departure_time": departure_time,
            "original_order": location["original_index"],
            "optimized_order": stop.get("optimized_order", i),
            "time_window_violation": time_window_violation,
            "method": method,
        })

        # Advance clock by this travel + visit duration
        current_time = arrival_epoch + location["visit_duration_sec"]

    if violations:
        logger.warning(
            f"Time window violations detected: {', '.join(violations)}"
        )
        if method != "route_optimization_api":
            logger.warning(
                f"{method} does not respect time windows. Consider using Route Optimization API for time-constrained routing."
            )

    return corrected_route


