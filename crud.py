from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Inventory

def get_inventory(db: Session):
    return db.query(Inventory).all()

def update_stock_level(db: Session, item_id: int, quantity: int):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if item:
        item.stock_level += quantity
        item.last_updated = func.now()
        db.commit()
        db.refresh(item)
    return item
