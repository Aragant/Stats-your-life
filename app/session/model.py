from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.core.db import Base


class Session(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=256), nullable=False)
    date = Column(String, nullable=False)
    template = Column(Boolean, nullable=False, default=False)
    

    exercises = relationship(
        "Exercise",
        back_populates="session",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    owner_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    owner = relationship("User", back_populates="sessions")
    
    def __repr__(self) -> str:
        return f"Session(id={self.id}, name={self.name}, owner_id={self.owner_id})"


class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)

    sets = relationship(
        "Set", back_populates="exercise", cascade="all, delete-orphan", lazy="selectin"
    )

    movement_id = Column(Integer, ForeignKey("movement.id", ondelete="CASCADE"))
    movement = relationship("Movement", back_populates="exercises")

    session_id = Column(Integer, ForeignKey("session.id", ondelete="CASCADE"))
    session = relationship("Session", back_populates="exercises")
    
    def __repr__(self) -> str:
        return f"Exercise(id={self.id}, type={self.type})"


class Set(Base):
    __tablename__ = "set"
    id = Column(Integer, primary_key=True, index=True)
    repetitions = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=True)
    duration = Column(Time, nullable=True)

    exercise_id = Column(Integer, ForeignKey("exercise.id", ondelete="CASCADE"))
    exercise = relationship("Exercise", back_populates="sets")
    
    def __repr__(self) -> str:
        return f"Set(id={self.id}, repetitions={self.repetitions}, weight={self.weight}, time={self.time})"
