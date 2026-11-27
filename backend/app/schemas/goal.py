from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import GoalStatus
from app.schemas.common import PartialUpdate

Title = Annotated[str, Field(min_length=1, max_length=200)]
Category = Annotated[str, Field(min_length=1, max_length=50)]
Priority = Annotated[int, Field(ge=1, le=3, description="1 = high, 3 = low")]


class GoalCreate(BaseModel):
    title: Title
    description: str | None = None
    category: Category
    target_date: date | None = None
    priority: Priority = 2


class GoalUpdate(PartialUpdate):
    """All fields optional: only the ones sent are changed."""

    non_nullable = ("title", "category", "priority", "status")

    title: Title | None = None
    description: str | None = None
    category: Category | None = None
    target_date: date | None = None
    priority: Priority | None = None
    status: GoalStatus | None = None


class GoalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    category: str
    target_date: date | None
    priority: int
    status: GoalStatus
    created_at: datetime
    updated_at: datetime
