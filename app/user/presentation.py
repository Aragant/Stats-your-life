from fastapi import APIRouter, Depends
from app.user.model import User
from app.user.users import current_active_user
from app.user.schemas import UserRead, UserUpdate

from app.user.users import fastapi_users

router = APIRouter()


@router.get("/me", response_model=UserRead, tags=["users"])
async def get_current_user(user: User = Depends(current_active_user)):
    """
    Endpoint pour récupérer les infos du user connecté.
    """
    return user


@router.get("/authenticated-route", tags=["users"])
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

# Route CRUD utilisateurs (FastAPI-Users)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/crud",
    tags=["users"],
)