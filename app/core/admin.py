# app/core/admin.py
from sqladmin import Admin, ModelView
from app.core.db import engine
from app.user.model import User
from app.task.model import Task
from app.routine.model import Routine
from app.timer.model import Timer
from fastapi_users.password import PasswordHelper
from fastapi import FastAPI


def init_admin(app: FastAPI):
    """Initialise le panneau d'administration avec User et Task."""
    admin = Admin(app, engine)

    # --- UserAdmin ---
    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.email, User.hashed_password, User.name, User.last_name]

        async def on_model_change(self, data, model, is_created, request):
            """Hache le mot de passe avant insertion si nouvel utilisateur"""
            if is_created and "hashed_password" in data:
                helper = PasswordHelper()
                data["hashed_password"] = helper.hash(data["hashed_password"])

    # --- TaskAdmin ---
    class TaskAdmin(ModelView, model=Task):
        column_list = [Task.id, Task.name, Task.validated, Task.deadline, Task.owner_id]
        
    class RoutineAdmin(ModelView, model=Routine):
        column_list = [Routine.id, Routine.name, Routine.owner_id]
        
    class TimerAdmin(ModelView, model=Timer):
        column_list = [Timer.id, Timer.name, Timer.owner_id]
        
    

    # Ajoute les vues à l'admin
    admin.add_view(UserAdmin)
    admin.add_view(TaskAdmin)
    admin.add_view(RoutineAdmin)
    admin.add_view(TimerAdmin)

    return admin
