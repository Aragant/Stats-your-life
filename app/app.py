from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.admin import init_admin

from app.user.presentation import router as user_routes
from app.auth.presentation import router as auth_routes
from app.task.presentation import router as task_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

init_admin(app)


app.include_router(auth_routes, prefix="/auth")

# Inclure les routers custom users
app.include_router(user_routes, prefix="/users")

# Inclure les routers custom tasks
app.include_router(task_routes, prefix="/tasks")