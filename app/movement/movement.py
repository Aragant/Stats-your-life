from sqlalchemy import select
from app.core.db import async_session_maker
from app.movement.model import Movement
from app.movement.schema import MovementCreate

class MovementService:
    def __init__(self):
        self.session_maker = async_session_maker()
        
    async def create_movement(self, movement: MovementCreate, user_id: str):
        async with self.session_maker() as session:
            new_movement = Movement(**movement.model_dump(), owner_id=user_id)
            session.add(new_movement)
            await session.commit()
            await session.refresh(new_movement)
            return new_movement
        
    
    async def get_movements(self, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Movement).filter(Movement.owner_id == user_id)
            )
            return result.scalars().all()
        
    async def get_movement(self, movement_id: int, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Movement).filter(Movement.id == movement_id, Movement.owner_id == user_id)
            )
            return result.scalars().first()
        
        
    async def delete_movement(self, movement_id: int, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Movement).filter(Movement.id == movement_id, Movement.owner_id == user_id)
            )
            movement = result.scalars().first()
            if movement:
                await session.delete(movement)
                await session.commit()
                return True
            return False
        
        
    async def update_movement(self, movement_id: int, movement_data: MovementCreate, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Movement).where(Movement.id == movement_id, Movement.owner_id == user_id)
            )
            movement = result.scalar_one_or_none()
            if not movement:
                return None
            movement.name = movement_data.name
            movement.muscle_group = movement_data.muscle_group
            await session.commit()
            await session.refresh(movement)
            return movement