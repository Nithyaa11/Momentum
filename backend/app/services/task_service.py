from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task, User
from app.models.enums import TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.services import goal_service
from app.services.errors import NotFoundError, ValidationError


def list_tasks(
    db: Session,
    user: User,
    goal_id: int | None = None,
    status: TaskStatus | None = None,
) -> list[Task]:
    query = select(Task).where(Task.user_id == user.id)
    if goal_id is not None:
        query = query.where(Task.goal_id == goal_id)
    if status is not None:
        query = query.where(Task.status == status)
    return list(db.scalars(query.order_by(Task.created_at, Task.id)))


def get_task(db: Session, user: User, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None or task.user_id != user.id:
        raise NotFoundError("Task", task_id)
    return task


def _check_goal(db: Session, user: User, goal_id: int | None) -> None:
    if goal_id is None:
        return
    try:
        goal_service.get_goal(db, user, goal_id)
    except NotFoundError as e:
        raise ValidationError(f"goal_id {goal_id} does not exist") from e


def create_task(db: Session, user: User, data: TaskCreate) -> Task:
    _check_goal(db, user, data.goal_id)
    task = Task(user_id=user.id, **data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, user: User, task_id: int, data: TaskUpdate) -> Task:
    task = get_task(db, user, task_id)
    changes = data.model_dump(exclude_unset=True)
    if "goal_id" in changes:
        _check_goal(db, user, changes["goal_id"])
    for field, value in changes.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task
