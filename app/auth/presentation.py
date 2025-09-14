
from fastapi import APIRouter
from app.user.users import fastapi_users, auth_backend
from app.user.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()

# Route pour JWT Auth
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"]
)

# Route pour inscription
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)

# Route pour reset password
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="",
    tags=["auth"],
)

# Route pour verification
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="",
    tags=["auth"],
)


