from fastapi import APIRouter, Depends, HTTPException
from app.movement.schema import MovementRead, MovementCreate
from app.movement.movement import MovementService
from app.user.model import User
from app.user.users import current_active_user


router = APIRouter(prefix="/movements", tags=["movements"])

movement_service = MovementService()

@router.get("/", response_model=list[MovementRead])
async def get_movements(user: User = Depends(current_active_user)):
    return await movement_service.get_movements(user.id)

@router.get("/{movement_id}", response_model=MovementRead)
async def get_movement(movement_id: int, user: User = Depends(current_active_user)):
    movement = await movement_service.get_movement(movement_id, user.id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement

@router.post("/", response_model=MovementRead)
async def create_movement(movement: MovementCreate, user: User = Depends(current_active_user)):
    return await movement_service.create_movement(movement, user.id)

@router.delete("/{movement_id}", response_model=bool)
async def delete_movement(movement_id: int, user: User = Depends(current_active_user)):
    return await movement_service.delete_movement(movement_id, user.id)

@router.put("/{movement_id}", response_model=MovementRead)
async def update_movement(movement_id: int, movement_data: MovementCreate, user: User = Depends(current_active_user)):
    movement = await movement_service.update_movement(movement_id, movement_data, user.id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement