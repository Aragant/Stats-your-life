from fastapi import APIRouter, Depends, HTTPException
from app.task.schema import TaskRead, TaskCreate
from app.task.task import TaskService
from app.user.model import User
from app.user.users import current_active_user


router = APIRouter(prefix="/tasks", tags=["tasks"])

task_service = TaskService()


@router.get("/", response_model=list[TaskRead])
async def get_tasks(user: User = Depends(current_active_user)):
    return await task_service.get_tasks(user.id)

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, user: User = Depends(current_active_user)):
        task = await task_service.get_task(task_id, user.id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate, user: User = Depends(current_active_user)):
    print(user)
    return await task_service.create_task(task, user.id)

@router.put("/{task_id}", response_model=TaskRead)
async def update_task_endpoint(task_id: int, task_data: TaskCreate, User: User = Depends(current_active_user)):
    task = await task_service.update_task(task_id, task_data, User.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: int, user: User = Depends(current_active_user)):
    return await task_service.delete_task(task_id, user.id)