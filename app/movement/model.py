from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Movement(Base):
    __tablename__ = "movement"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=256), nullable=False)
    muscle_group = Column(String(length=256), nullable=False)
    
    owner_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    owner = relationship("User", back_populates="movements")