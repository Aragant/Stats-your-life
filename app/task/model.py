from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=256), nullable=False)
    validated = Column(Boolean, default=False, nullable=False)
    priority = Column(Integer, default=1, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)

    owner_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, name={self.name}, validated={self.validated}, priority={self.priority}, deadline={self.deadline}, owner_id={self.owner_id})"
