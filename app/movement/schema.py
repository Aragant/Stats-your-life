from pydantic import BaseModel

class MovementRead(BaseModel):
    id: int
    name: str
    muscle_group: str
    
class MovementCreate(BaseModel):
    name: str
    muscle_group: str