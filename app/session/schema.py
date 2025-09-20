from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import time

from app.movement.schema import MovementRead

class SetCreate(BaseModel):
    repetitions: int
    weight: Optional[int] = None
    duration: Optional[time] = None

class SetRead(BaseModel):
    id: int
    repetitions: int
    weight: Optional[int] = None
    duration: Optional[time] = None

class ExerciseCreate(BaseModel):
    movement_id: int
    type: str

class ExerciseRead(BaseModel):
    id: int
    type: str
    movement: MovementRead
    sets: list[SetRead]

class SessionCreate(BaseModel):
    name: str
    
class SessionRead(BaseModel):
    id: int
    name: str
    exercises: list[ExerciseRead]

    
    

