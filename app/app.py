from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.admin import init_admin

from app.user.presentation import router as user_routes
from app.auth.presentation import router as auth_routes
from app.task.presentation import router as task_routes
from app.routine.presentation import router as routine_routes
from app.timer.presentation import router as timer_routes
from app.movement.presentation import router as movement_routes
from app.session.presentation import router as session_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "https://app.local.stats:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_admin(app)


app.include_router(auth_routes, prefix="/auth")

app.include_router(user_routes, prefix="/users")

app.include_router(task_routes)

app.include_router(routine_routes)

app.include_router(timer_routes)

app.include_router(movement_routes)

app.include_router(session_routes)