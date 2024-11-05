import random
import time
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Inventory
from database import SessionLocal

route_warehouse_to_fps = [
    {"lat": 40.712776, "lon": -74.005974},  # Start (Warehouse)
    {"lat": 40.713000, "lon": -74.004000},
    {"lat": 40.714000, "lon": -74.003000},
    {"lat": 40.730610, "lon": -73.935242},  # End (FPS)
]


def mock_inventory_movement():
    db = SessionLocal()
    try:
        while True:
            item_id = random.randint(1, 10)  # Adjust range to match item IDs
            quantity_change = random.choice([-1, 1]) * random.randint(1, 5)

            item = db.query(Inventory).filter(Inventory.id == item_id).first()
            if item:
                item.stock_level += quantity_change
                item.last_updated = func.now()
                db.commit()
                print(f"Updated stock for item {item.item_name}: {item.stock_level}")
            
            time.sleep(5)  # Run every 5 seconds
    finally:
        db.close()

if __name__ == "__main__":
    mock_inventory_movement()
