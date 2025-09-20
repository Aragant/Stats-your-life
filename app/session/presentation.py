from fastapi import APIRouter, Depends, HTTPException
from app.session.schema import SessionRead, SessionCreate, ExerciseCreate, SetCreate
from app.session.session import SessionService
from app.user.model import User
from app.user.users import current_active_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

session_service = SessionService()

@router.get("/", response_model=list[SessionRead])
async def get_sessions(user: User = Depends(current_active_user)):
    return await session_service.get_sessions(user.id)

@router.post("/", response_model=SessionRead)
async def create_session(session: SessionCreate, user: User = Depends(current_active_user)):
    return await session_service.create_session(session, user.id)

@router.get("/{session_id}", response_model=SessionRead)
async def get_session(session_id: int, user: User = Depends(current_active_user)):
    session = await session_service.get_session(session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{session_id}", response_model=SessionRead)
async def update_session(session_id: int, session_data: SessionCreate, user: User = Depends(current_active_user)):
    session = await session_service.update_session(session_id, session_data, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/{session_id}", response_model=bool)
async def delete_session(session_id: int, user: User = Depends(current_active_user)):
    return await session_service.delete_session(session_id, user.id)

@router.post("/{session_id}/exercises", response_model=SessionRead)
async def add_exercise(exercise: ExerciseCreate, session_id: int, user: User = Depends(current_active_user)):
    session = await session_service.add_exercise(exercise, session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/{session_id}/exercises/{exercise_id}", response_model=bool)
async def delete_exercise(exercise_id: int, session_id: int, user: User = Depends(current_active_user)):
    return await session_service.delete_exercise(exercise_id, session_id, user.id)

@router.put("/{session_id}/exercises/{exercise_id}", response_model=SessionRead)
async def update_exercise(exercise_id: int, exercise_data: ExerciseCreate, session_id: int, user: User = Depends(current_active_user)):
    session = await session_service.update_exercise(exercise_id, exercise_data, session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Exercice or movement not found")
    return session

@router.post("/{session_id}/exercises/{exercise_id}/sets", response_model=SessionRead)
async def add_set(set: SetCreate, exercise_id: int, session_id: int, user: User = Depends(current_active_user)):
    session = await session_service.add_set(set, exercise_id, session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Exercice not found")
    return session

@router.delete("/{session_id}/exercises/{exercise_id}/sets/{set_id}", response_model=bool)
async def delete_set(set_id: int, exercise_id: int, session_id: int, user: User = Depends(current_active_user)):
    return await session_service.delete_set(set_id, exercise_id, session_id, user.id)

@router.put("/{session_id}/exercises/{exercise_id}/sets/{set_id}", response_model=SessionRead)
async def update_set(set_id: int, set_data: SetCreate, exercise_id: int, session_id: int, user: User = Depends(current_active_user)):
    session = await session_service.update_set(set_id, set_data, exercise_id, session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return session