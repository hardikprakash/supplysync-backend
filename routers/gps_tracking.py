# gps_tracking.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import GPSLocation, Alert
from database import get_db
from mock_data import route_warehouse_to_fps
from geopy.distance import geodesic
from datetime import datetime

MAX_DEVIATION_METERS = 500
MAX_DELAY_SECONDS = 300

router = APIRouter()

route_index = 0

@router.post("/gps/update")
def update_gps_location(vehicle_id: str, db: Session = Depends(get_db)):
    global route_index
    if route_index >= len(route_warehouse_to_fps):
        route_index = 0
    
    # Get the next GPS location from the route
    gps_data = route_warehouse_to_fps[route_index]
    route_index += 1

    # Create GPS location record
    gps_location = GPSLocation(
        vehicle_id=vehicle_id,
        latitude=gps_data["lat"],
        longitude=gps_data["lon"],
        timestamp=func.now()
    )
    db.add(gps_location)
    db.commit()

    # Check for deviations and delays
    if route_index > 1:
        last_location = route_warehouse_to_fps[route_index - 2]
        current_distance = geodesic(
            (gps_data["lat"], gps_data["lon"]),
            (last_location["lat"], last_location["lon"])
        ).meters
        
        # Alert for route deviation
        if current_distance > MAX_DEVIATION_METERS:
            alert = Alert(
                vehicle_id=vehicle_id,
                alert_type="Deviation",
                description=f"Vehicle deviated {current_distance:.2f} meters from the route."
            )
            db.add(alert)

        # Alert for delay
        last_timestamp = gps_location.timestamp  # Timestamp when the location was updated
        current_time = datetime.utcnow()
        time_difference = (current_time - last_timestamp).total_seconds()
        
        if time_difference > MAX_DELAY_SECONDS:
            alert = Alert(
                vehicle_id=vehicle_id,
                alert_type="Delay",
                description="Vehicle delayed at checkpoint."
            )
            db.add(alert)

    db.commit()

    return {"message": f"Vehicle {vehicle_id} location updated.", "location": gps_data}


@router.get("/alerts")
def get_alerts(vehicle_id: str, db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.vehicle_id == vehicle_id).all()
    return {"vehicle_id": vehicle_id, "alerts": alerts}
