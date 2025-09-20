from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.core.db import async_session_maker
from app.movement.model import Movement
from app.session.model import Session, Exercise, Set
from app.session.schema import SessionCreate, ExerciseCreate, SetCreate


class SessionService:
    def __init__(self):
        self.session = async_session_maker()

    async def create_session(self, session: SessionCreate, user_id: str):
        async with self.session as session_db:
            new_session = Session(**session.model_dump(), owner_id=user_id)
            session_db.add(new_session)
            await session_db.commit()
            await session_db.refresh(new_session)
            return new_session

    async def get_sessions(self, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Session)
                .options(
                    joinedload(Session.exercises).joinedload(Exercise.movement),
                    joinedload(Session.exercises).joinedload(Exercise.sets),
                )
                .filter(Session.owner_id == user_id)
            )
            sessions = result.unique().scalars().all()
            return sessions

    async def get_session(self, session_id: int, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Session).filter(
                    Session.id == session_id, Session.owner_id == user_id
                )
            )
            return result.scalars().first()

    async def delete_session(self, session_id: int, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Session).filter(
                    Session.id == session_id, Session.owner_id == user_id
                )
            )
            session = result.scalars().first()
            if session:
                await session.delete(session)
                await session.commit()
                return True
            return False

    async def update_session(
        self, session_id: int, session_data: SessionCreate, user_id: str
    ):
        async with self.session as session:
            result = await session.execute(
                select(Session).where(
                    Session.id == session_id, Session.owner_id == user_id
                )
            )
            session_to_update = result.scalar_one_or_none()
            if not session_to_update:
                return None
            session_to_update.name = session_data.name
            await session.commit()
            await session.refresh(session_to_update)
            return session_to_update

    async def add_exercise(
        self, exercise: ExerciseCreate, session_id: int, user_id: str
    ):
        async with self.session as session:
            # On charge la session avec tous les exercices + leurs mouvements et sets
            result = await session.execute(
                select(Session)
                .options(
                    joinedload(Session.exercises).joinedload(Exercise.movement),
                    joinedload(Session.exercises).joinedload(Exercise.sets),
                )
                .filter(Session.id == session_id, Session.owner_id == user_id)
            )
            session_to_update = result.scalars().first()

            if not session_to_update:
                return None

            # On crée le nouvel exercice et on l'attache à la session
            new_exercise = Exercise(**exercise.model_dump(), session=session_to_update)
            session.add(new_exercise)

            await session.commit()
            await session.refresh(
                session_to_update
            )  # session_to_update est toujours attachée

            return session_to_update

    async def delete_exercise(self, exercise_id: int, session_id: int, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Exercise).filter(
                    Exercise.id == exercise_id, Exercise.session_id == session_id
                )
            )
            exercise = result.scalars().first()
            if exercise:
                await session.delete(exercise)
                await session.commit()
                return True
            return False

    async def update_exercise(
        self,
        exercise_id: int,
        exercise_data: ExerciseCreate,
        session_id: int,
        user_id: str,
    ):
        async with self.session as session:
            result = await session.execute(
                select(Exercise).where(
                    Exercise.id == exercise_id, Exercise.session_id == session_id
                )
            )
            exercise_to_update = result.scalar_one_or_none()
            if not exercise_to_update:
                return None
            
            movement = await session.get(Movement, exercise_data.movement_id)
            if not movement:
                return None

            exercise_to_update.movement_id = exercise_data.movement_id
            exercise_to_update.type = exercise_data.type
            exercise_to_update.sets = []

            await session.commit()

            # Reload the session with all exercises and their relations
            result = await session.execute(
                select(Session)
                .filter(Session.id == session_id)
                .options(
                    joinedload(Session.exercises).joinedload(Exercise.movement),
                    joinedload(Session.exercises).joinedload(Exercise.sets),
                )
            )
            session_to_return = result.unique().scalar_one()

            return session_to_return

    async def add_set(
        self, set: SetCreate, exercise_id: int, session_id: int, user_id: str
    ):
        async with self.session as session:
            result = await session.execute(
                select(Exercise).where(
                    Exercise.id == exercise_id, Exercise.session_id == session_id
                )
            )
            exercise_to_update = result.scalar_one_or_none()
            if not exercise_to_update:
                return None

            new_set = Set(**set.model_dump(), exercise=exercise_to_update)
            session.add(new_set)
            await session.commit()

            result = await session.execute(
                select(Session)
                .filter(Session.id == session_id)
                .options(
                    joinedload(Session.exercises).joinedload(Exercise.movement),
                    joinedload(Session.exercises).joinedload(Exercise.sets),
                )
            )
            session_to_return = result.unique().scalar_one()

            return session_to_return
    
    async def delete_set(self, set_id: int, exercise_id: int, session_id: int, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Set).filter(
                    Set.id == set_id, Set.exercise_id == exercise_id
                )
            )
            set_to_delete = result.scalars().first()
            if set_to_delete:
                await session.delete(set_to_delete)
                await session.commit()
                return True
            return False
        
    async def update_set(self, set_id: int, set_data: SetCreate, exercise_id: int, session_id: int, user_id: str):
        async with self.session as session:
            result = await session.execute(
                select(Set).where(
                    Set.id == set_id, Set.exercise_id == exercise_id
                )
            )
            set_to_update = result.scalar_one_or_none()
            if not set_to_update:
                return None
            set_to_update.repetitions = set_data.repetitions
            set_to_update.weight = set_data.weight
            set_to_update.duration = set_data.duration
            await session.commit()
            
            result = await session.execute(
                select(Session)
                .filter(Session.id == session_id)
                .options(
                    joinedload(Session.exercises).joinedload(Exercise.movement),
                    joinedload(Session.exercises).joinedload(Exercise.sets),
                )
            )
            session_to_return = result.unique().scalar_one()
            
            return session_to_return
