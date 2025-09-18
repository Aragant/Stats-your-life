from datetime import time
from pydantic import BaseModel


class TimerRead(BaseModel):
    id: int
    name: str
    worktime: time
    breaktime: time
    custom: bool
    
class TimerCreate(BaseModel):
    name: str
    worktime: time
    breaktime: time