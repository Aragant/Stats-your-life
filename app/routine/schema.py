from pydantic import BaseModel
from datetime import datetime

class RoutineCreate(BaseModel):
    name: str
    cooldown_days: int
    

class RoutineRead(BaseModel):
    id: int
    name: str
    validated: bool
    cooldown_days: int
    last_validation: datetime
    strike: int
    
    class Config:
        from_attributes = True