from datetime import date, datetime, time
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import Outcome, PlanStatus, SkipReason

Minutes = Annotated[int, Field(ge=1, le=240)]


# ---------- Requests ----------


class PlanItemIn(BaseModel):
    task_id: int
    planned_minutes: Minutes
    scheduled_start: time | None = None
    reason: str | None = Field(default=None, max_length=300)


class PlanIn(BaseModel):
    """Creates or replaces the plan for a day. Items are stored in the order given."""

    rationale: str | None = Field(default=None, max_length=2000)
    items: list[PlanItemIn] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def _no_duplicate_tasks(self) -> Self:
        task_ids = [item.task_id for item in self.items]
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("a task can appear only once in a plan")
        return self


class CheckInIn(BaseModel):
    outcome: Outcome
    # Defaults: done -> planned minutes, skipped -> 0. Required for partial.
    actual_minutes: int | None = Field(default=None, ge=0, le=600)
    skip_reason: SkipReason | None = None
    note: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def _rules_per_outcome(self) -> Self:
        if self.outcome == Outcome.SKIPPED:
            if self.skip_reason is None:
                raise ValueError("skip_reason is required when outcome is skipped")
            if self.actual_minutes:
                raise ValueError("a skipped task can't have actual minutes; use partial")
        elif self.outcome == Outcome.PARTIAL:
            if not self.actual_minutes:
                raise ValueError("actual_minutes (> 0) is required when outcome is partial")
        elif self.outcome == Outcome.DONE and self.skip_reason is not None:
            raise ValueError("skip_reason isn't allowed when outcome is done")
        return self


# ---------- Responses ----------


class TaskSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    goal_id: int | None
    title: str
    category: str


class CompletionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    outcome: Outcome
    actual_minutes: int
    skip_reason: SkipReason | None
    note: str | None
    completed_at: datetime


class PlanItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    position: int
    scheduled_start: time | None
    planned_minutes: int
    reason: str | None
    task: TaskSummary
    completion: CompletionRead | None


class PlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    status: PlanStatus
    rationale: str | None
    items: list[PlanItemRead]
