from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    name: str
    deadline: datetime
    priority: int
    

class TaskRead(BaseModel):
    id: int
    name: str
    validated: bool
    priority: int
    deadline: datetime
    
    class Config:
        from_attributes = True