# routers/scanning.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Journey, Inventory
from database import get_db
import random
import datetime

router = APIRouter()

checkpoints = ["Warehouse", "In Transit", "FPS"]

@router.post("/scan")
def simulate_scan(item_id: int, db: Session = Depends(get_db)):
    # Get the item
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Generate a random checkpoint
    checkpoint = random.choice(checkpoints)

    # Create a new journey record
    journey_entry = Journey(item_id=item.id, checkpoint=checkpoint, timestamp=datetime.datetime.utcnow())
    db.add(journey_entry)
    db.commit()

    return {"message": f"Item {item.item_name} scanned at {checkpoint} checkpoint"}
