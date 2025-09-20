from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Movement(Base):
    __tablename__ = "movement"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=256), nullable=False)
    muscle_group = Column(String(length=256), nullable=False)
    
    exercises = relationship("Exercise", back_populates="movement", cascade="all, delete-orphan")
    
    owner_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    owner = relationship("User", back_populates="movements")
    
    def __repr__(self) -> str:
        return f"Movement(id={self.id}, name={self.name}, muscle_group={self.muscle_group}, owner_id={self.owner_id})"