from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    stock_level = Column(Integer, default=0)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())


class Journey(Base):
    __tablename__ = "journey"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory.id"))
    checkpoint = Column(String, index=True)  # e.g., "Warehouse", "FPS"
    timestamp = Column(DateTime, default=func.now())

    item = relationship("Inventory")

class GPSLocation(Base):
    __tablename__ = "gps_location"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=func.now())

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    alert_type = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=func.now())