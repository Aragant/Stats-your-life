# app/core/admin.py
from sqladmin import Admin, ModelView
from app.core.db import engine
from app.user.model import User
from app.task.model import Task
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

    # Ajoute les vues à l'admin
    admin.add_view(UserAdmin)
    admin.add_view(TaskAdmin)

    return admin
