from datetime import datetime
from sqlalchemy.future import select
from app.core.db import async_session_maker
from app.routine.model import Routine
from app.routine.schema import RoutineCreate



class RoutineService:
    def __init__(self):
        self.session_maker = async_session_maker()
        

    async def create_routine(self, routine: RoutineCreate, user_id: str):
        async with self.session_maker() as session:
            new_routine = Routine(**routine.model_dump(), owner_id=user_id)
            session.add(new_routine)
            await session.commit()
            await session.refresh(new_routine)
            return new_routine
        

    async def get_routines(self, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Routine).filter(Routine.owner_id == user_id)
            )
            return result.scalars().all()
        

    async def get_routine(self, routine_id: int, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Routine).filter(Routine.id == routine_id, Routine.owner_id == user_id)
            )
            return result.scalars().first()
        

    async def delete_routine(self, routine_id: int, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Routine).filter(Routine.id == routine_id, Routine.owner_id == user_id)
            )
            routine = result.scalars().first()
            if routine:
                await session.delete(routine)
                await session.commit()
                return True
            return False
        
    
    async def validate_routine(self, routine_id: int, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Routine).filter(Routine.id == routine_id, Routine.owner_id == user_id)
            )
            routine = result.scalars().first()
            if routine:
                routine.validated = True
                routine.strike += 1
                routine.last_validation = datetime.now()
                await session.commit()
                await session.refresh(routine)
                return routine
            return None
        
        
    async def update_routine(self, routine_id: int, routine_data: RoutineCreate, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Routine).where(Routine.id == routine_id, Routine.owner_id == user_id)
            )
            routine = result.scalar_one_or_none()
            if not routine:
                return None
            routine.name = routine_data.name
            routine.cooldown_days = routine_data.cooldown_days
            await session.commit()
            await session.refresh(routine)
            return routine