from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import User
from app.models.enums import GoalStatus
from app.schemas.goal import GoalCreate, GoalRead, GoalUpdate
from app.services import goal_service

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("", response_model=list[GoalRead])
def list_goals(
    status: GoalStatus | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return goal_service.list_goals(db, user, status)


@router.post("", response_model=GoalRead, status_code=status.HTTP_201_CREATED)
def create_goal(
    data: GoalCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return goal_service.create_goal(db, user, data)


@router.get("/{goal_id}", response_model=GoalRead)
def get_goal(goal_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return goal_service.get_goal(db, user, goal_id)


@router.patch("/{goal_id}", response_model=GoalRead)
def update_goal(
    goal_id: int,
    data: GoalUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Partial update. Archive a goal with {"status": "archived"}."""
    return goal_service.update_goal(db, user, goal_id, data)
