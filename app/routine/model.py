from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Routine(Base):
    __tablename__ = "routine"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=256), nullable=False)
    validated = Column(Boolean, default=False, nullable=False)
    cooldown_days = Column(Integer, default=1, nullable=False)
    last_validation = Column(DateTime(timezone=True), nullable=True)
    strike = Column(Integer, default=0, nullable=False)
    
    owner_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="routines")
    
    def __repr__(self):
        return f"Routine(id={self.id}, name={self.name}, validated={self.validated}, cooldown_days={self.cooldown_days}, last_validation={self.last_validation}, strike={self.strike}, owner_id={self.owner_id})"