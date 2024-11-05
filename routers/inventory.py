from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import crud
from database import get_db

router = APIRouter()

class UpdateStockRequest(BaseModel):
    item_id: int
    quantity: int

@router.get("/inventory")
def get_inventory(db: Session = Depends(get_db)):
    return crud.get_inventory(db)

@router.post("/inventory/update")
def update_stock(data: UpdateStockRequest, db: Session = Depends(get_db)):
    item = crud.update_stock_level(db, data.item_id, data.quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Stock level updated", "new_stock_level": item.stock_level}
