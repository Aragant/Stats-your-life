from fastapi import APIRouter, Depends, HTTPException
from app.timer.schema import TimerRead, TimerCreate
from app.timer.timer import TimerService
from app.user.model import User
from app.user.users import current_active_user


router = APIRouter(prefix="/timers", tags=["timers"])

timer_service = TimerService()

@router.get("/", response_model=list[TimerRead])
async def get_timers(user: User = Depends(current_active_user)):
    return await timer_service.get_timers(user.id)


@router.get("/{timer_id}", response_model=TimerRead)
async def get_timer(timer_id: int, user: User = Depends(current_active_user)):
    timer = await timer_service.get_timer(timer_id, user.id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    return timer


@router.post("/", response_model=TimerRead)
async def create_timer(timer: TimerCreate, user: User = Depends(current_active_user)):
    return await timer_service.create_timer(timer, user.id)


@router.put("/{timer_id}", response_model=TimerRead)
async def update_timer(timer_id: int, timer_data: TimerCreate, user: User = Depends(current_active_user)):
    timer = await timer_service.update_timer(timer_id, timer_data, user.id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    return timer


@router.delete("/{timer_id}", response_model=bool)
async def delete_timer(timer_id: int, user: User = Depends(current_active_user)):
    return await timer_service.delete_timer(timer_id, user.id)