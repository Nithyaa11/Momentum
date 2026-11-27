from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Goal, User
from app.models.enums import GoalStatus
from app.schemas.goal import GoalCreate, GoalUpdate
from app.services.errors import NotFoundError


def list_goals(db: Session, user: User, status: GoalStatus | None = None) -> list[Goal]:
    query = select(Goal).where(Goal.user_id == user.id)
    if status is not None:
        query = query.where(Goal.status == status)
    return list(db.scalars(query.order_by(Goal.priority, Goal.created_at)))


def get_goal(db: Session, user: User, goal_id: int) -> Goal:
    goal = db.get(Goal, goal_id)
    if goal is None or goal.user_id != user.id:
        raise NotFoundError("Goal", goal_id)
    return goal


def create_goal(db: Session, user: User, data: GoalCreate) -> Goal:
    goal = Goal(user_id=user.id, **data.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def update_goal(db: Session, user: User, goal_id: int, data: GoalUpdate) -> Goal:
    goal = get_goal(db, user, goal_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(goal, field, value)
    db.commit()
    db.refresh(goal)
    return goal
