"""Import every model here so Base.metadata knows about all tables (needed by Alembic)."""

from app.models.goal import Goal
from app.models.plan import Completion, Plan, PlanItem
from app.models.progress import BehaviorSnapshot, Win
from app.models.task import Task
from app.models.user import User

__all__ = ["BehaviorSnapshot", "Completion", "Goal", "Plan", "PlanItem", "Task", "User", "Win"]
