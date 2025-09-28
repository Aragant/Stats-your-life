from datetime import datetime, timezone
from sqlalchemy.future import select
from app.core.db import async_session_maker
from app.routine.model import Routine
from app.routine.schema import RoutineCreate
import pytz


class RoutineService:
    def __init__(self):
        self.session_maker = async_session_maker
        

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
            routines = result.scalars().all()
            
            # Configuration du fuseau horaire
            user_timezone = pytz.timezone('Europe/Paris')
            now_utc = datetime.now(timezone.utc)
            now_local = now_utc.astimezone(user_timezone)
            today_local = now_local.date()
            
            # Mise à jour des routines
            modified_routines = []
            for routine in routines:
                if routine.last_validation:
                    last_validation_local = routine.last_validation.astimezone(user_timezone)
                    last_validation_date = last_validation_local.date()
                    days_diff = (today_local - last_validation_date).days
                    
                    if days_diff > routine.cooldown_days:
                        routine.validated = False
                        routine.strike = 0
                        session.add(routine)
                        modified_routines.append(routine)
                    elif days_diff >= 1:
                        routine.validated = False
                        session.add(routine)
                        modified_routines.append(routine)

            if modified_routines:
                await session.commit()

            # Fonction de calcul de priorité de tri
            def calculate_routine_priority(routine):
                """
                Calcule la priorité de tri pour une routine.
                
                Ordre de priorité (du plus urgent au moins urgent) :
                1. En retard (days_until_available < 0)
                2. Disponible aujourd'hui (days_until_available == 0)  
                3. Disponible dans 1 jour, 2 jours, etc. (days_until_available > 0)
                4. Déjà validées aujourd'hui
                
                Returns:
                    tuple: (priorité_groupe, jours_jusqu_disponibilité)
                    - priorité_groupe: 1=en retard, 2=aujourd'hui, 3=futur, 4=validées
                    - jours_jusqu_disponibilité: pour le tri secondaire
                """
                
                # Cas spécial : pas de dernière validation
                if not routine.last_validation:
                    return (2, 0)  # Considéré comme disponible maintenant
                
                # Calculer les jours depuis la dernière validation
                last_validation_local = routine.last_validation.astimezone(user_timezone)
                last_validation_date = last_validation_local.date()
                days_since_validation = (today_local - last_validation_date).days
                
                # Calculer quand la routine sera/est disponible
                days_until_available = routine.cooldown_days - days_since_validation
                
                # Déterminer la catégorie de priorité
                if routine.validated:
                    # Routine déjà validée aujourd'hui - priorité la plus basse
                    priority_group = 4
                    secondary_sort = days_until_available  # Prochaine disponibilité
                    
                elif days_until_available < 0:
                    # EN RETARD - priorité maximale
                    priority_group = 1
                    secondary_sort = days_until_available  # Plus négatif = plus en retard
                    
                elif days_until_available == 0:
                    # DISPONIBLE AUJOURD'HUI - deuxième priorité
                    priority_group = 2
                    secondary_sort = 0
                    
                else:
                    # DISPONIBLE DANS LE FUTUR - troisième priorité
                    priority_group = 3
                    secondary_sort = days_until_available  # 1 jour, 2 jours, etc.
                
                return (priority_group, secondary_sort)

            # Trier les routines par priorité
            sorted_routines = sorted(routines, key=calculate_routine_priority)
            
            return sorted_routines
        

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
                if routine.validated:
                    return routine
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