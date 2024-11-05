from database import SessionLocal, engine, Base
from models import Inventory

Base.metadata.create_all(bind=engine)

def seed_inventory():
    db = SessionLocal()
    try:
        if db.query(Inventory).count() == 0:
            sample_items = [
                Inventory(item_name="Rice", stock_level=100),
                Inventory(item_name="Wheat", stock_level=200),
                Inventory(item_name="Sugar", stock_level=150),
                Inventory(item_name="Oil", stock_level=80)
            ]
            db.add_all(sample_items)
            db.commit()
            print("Sample inventory data added.")
        else:
            print("Inventory already seeded.")
    finally:
        db.close()

seed_inventory()
