from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TaskStatus
from app.schemas.common import PartialUpdate

Title = Annotated[str, Field(min_length=1, max_length=200)]
Category = Annotated[str, Field(min_length=1, max_length=50)]
# Capped at 4 hours: longer blocks should be split into smaller tasks
Minutes = Annotated[int, Field(ge=1, le=240)]


class TaskCreate(BaseModel):
    title: Title
    category: Category
    estimated_minutes: Minutes
    goal_id: int | None = None


class TaskUpdate(PartialUpdate):
    """All fields optional: only the ones sent are changed. goal_id may be null (detach)."""

    non_nullable = ("title", "category", "estimated_minutes", "status")

    title: Title | None = None
    category: Category | None = None
    estimated_minutes: Minutes | None = None
    goal_id: int | None = None
    status: TaskStatus | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    goal_id: int | None
    title: str
    category: str
    estimated_minutes: int
    status: TaskStatus
    times_skipped: int
    created_at: datetime
    updated_at: datetime
