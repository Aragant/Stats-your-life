from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.core.db import Base

class Timer(Base):
    __tablename__ = "timer"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=256), nullable=False)
    worktime = Column(Time, nullable=False)
    breaktime = Column(Time, nullable=False)
    custom = Column(Boolean, nullable=False)
    
    owner_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    owner = relationship("User", back_populates="timers")
    