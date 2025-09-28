from fastapi import APIRouter, Depends, HTTPException
from app.routine.schema import RoutineRead, RoutineCreate
from app.routine.routine import RoutineService
from app.user.model import User
from app.user.users import current_active_user


router = APIRouter(prefix="/routines", tags=["routines"])

routine_service = RoutineService()


@router.get("/", response_model=list[RoutineRead])
async def get_routines(user: User = Depends(current_active_user)):
    return await routine_service.get_routines(user.id)

@router.get("/{routine_id}", response_model=RoutineRead)
async def get_routine(routine_id: int, user: User = Depends(current_active_user)):
    routine = await routine_service.get_routine(routine_id, user.id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    return routine

@router.post("/", response_model=RoutineRead)
async def create_routine(routine: RoutineCreate, user: User = Depends(current_active_user)):
    return await routine_service.create_routine(routine, user.id)

@router.delete("/{routine_id}")
async def delete_routine(routine_id: int, user: User = Depends(current_active_user)):
    return await routine_service.delete_routine(routine_id, user.id)

@router.put("/{routine_id}/validate", response_model=RoutineRead)
async def validate_routine(routine_id: int, user: User = Depends(current_active_user)):
    routine = await routine_service.validate_routine(routine_id, user.id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    return routine

@router.put("/{routine_id}", response_model=RoutineRead)
async def update_routine(routine_id: int, routine_data: RoutineCreate, user: User = Depends(current_active_user)):
    routine = await routine_service.update_routine(routine_id, routine_data, user.id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    return routine


