from sqlalchemy import select
from app.core.db import async_session_maker
from app.timer.model import Timer
from app.timer.schema import TimerCreate


class TimerService:
    def __init__(self):
        self.session_maker = async_session_maker()
        
    async def create_timer(self, timer: TimerCreate, user_id: str):
        async with self.session_maker() as session:
            new_timer = Timer(**timer.model_dump(), owner_id=user_id)
            new_timer.custom = False
            
            session.add(new_timer)
            await session.commit()
            await session.refresh(new_timer)
            return new_timer
        
    async def get_timers(self, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Timer).filter(Timer.owner_id == user_id)
            )
            return result.scalars().all()
        
    async def get_timer(self, timer_id: int, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Timer).filter(Timer.id == timer_id, Timer.owner_id == user_id)
            )
            return result.scalars().first()
        
    async def delete_timer(self, timer_id: int, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Timer).filter(Timer.id == timer_id, Timer.owner_id == user_id)
            )
            timer = result.scalars().first()
            if timer:
                await session.delete(timer)
                await session.commit()
                return True
            return False
        
    
    async def update_timer(self, timer_id: int, timer_data: TimerCreate, user_id: str):
        async with self.session_maker() as session:
            result = await session.execute(
                select(Timer).where(Timer.id == timer_id, Timer.owner_id == user_id)
            )
            timer = result.scalar_one_or_none()
            if not timer:
                return None
            timer.name = timer_data.name
            timer.worktime = timer_data.worktime
            timer.breaktime = timer_data.breaktime
            await session.commit()
            await session.refresh(timer)
            return timer