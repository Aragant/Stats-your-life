import uuid
from fastapi import Depends
from sqlalchemy import UUID, String
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from sqlalchemy import Column

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name: str = Column(String(length=50), nullable=True)
    last_name: str = Column(String(length=50), nullable=True)
    
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    routines = relationship("Routine", back_populates="owner", cascade="all, delete-orphan")
    timers = relationship("Timer", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, name={self.name}, last_name={self.last_name})"
    
    

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)