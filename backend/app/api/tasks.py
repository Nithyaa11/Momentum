from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import User
from app.models.enums import TaskStatus
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(
    goal_id: int | None = None,
    status: TaskStatus | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return task_service.list_tasks(db, user, goal_id, status)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return task_service.create_task(db, user, data)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return task_service.get_task(db, user, task_id)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return task_service.update_task(db, user, task_id, data)
