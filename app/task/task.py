from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.core.db import async_session_maker
from app.task.model import Task
from app.task.schema import TaskCreate


class TaskService:
    def __init__(self):
        self.session = async_session_maker()

    async def create_task(self, task: TaskCreate, user_id: str):
        async with self.session as session:
            new_task = Task(**task.model_dump(), owner_id=user_id)
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            return new_task

    async def get_tasks(self, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Task).filter(Task.owner_id == user_id)
            )
            return result.scalars().all()

    async def get_task(self, task_id: int, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Task).filter(Task.id == task_id, Task.owner_id == user_id)
            )
            return result.scalars().first()

    async def delete_task(self, task_id: int, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Task).filter(Task.id == task_id, Task.owner_id == user_id)
            )
            task = result.scalars().first()
            if task:
                await session.delete(task)
                await session.commit()
                return True
            return False


    async def update_task(self, task_id: int, task_data: TaskCreate, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.owner_id == user_id)
            )
            task = result.scalar_one_or_none()
            if not task:
                return None
            task.name = task_data.name
            task.deadline = task_data.deadline
            task.priority = task_data.priority
            await session.commit()
            await session.refresh(task)
            return task