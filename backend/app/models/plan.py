from datetime import date, datetime, time

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.base import TimestampMixin, str_enum
from app.models.enums import Outcome, PlanStatus, SkipReason


class Plan(TimestampMixin, Base):
    """One user's plan for one day."""

    __tablename__ = "plans"
    __table_args__ = (UniqueConstraint("user_id", "date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    date: Mapped[date]
    status: Mapped[PlanStatus] = mapped_column(str_enum(PlanStatus), default=PlanStatus.PROPOSED)
    rationale: Mapped[str | None] = mapped_column(Text)  # the agent's overall explanation

    items: Mapped[list["PlanItem"]] = relationship(
        back_populates="plan", cascade="all, delete-orphan", order_by="PlanItem.position"
    )


class PlanItem(Base):
    """A task scheduled into a plan. planned_minutes vs. the completion's actual_minutes
    is the core signal Momentum learns from."""

    __tablename__ = "plan_items"
    __table_args__ = (CheckConstraint("planned_minutes > 0", name="planned_positive"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id", ondelete="CASCADE"), index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True)

    position: Mapped[int]
    scheduled_start: Mapped[time | None]
    planned_minutes: Mapped[int]
    reason: Mapped[str | None] = mapped_column(Text)  # one-line "why this, why now"

    plan: Mapped[Plan] = relationship(back_populates="items")
    task: Mapped["Task"] = relationship()  # noqa: F821
    completion: Mapped["Completion | None"] = relationship(
        back_populates="plan_item", cascade="all, delete-orphan"
    )


class Completion(Base):
    """The user's check-in for a plan item: what actually happened."""

    __tablename__ = "completions"
    __table_args__ = (
        CheckConstraint("actual_minutes >= 0", name="actual_non_negative"),
        CheckConstraint(
            "outcome <> 'skipped' OR skip_reason IS NOT NULL", name="skip_needs_reason"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # unique: one check-in per plan item
    plan_item_id: Mapped[int] = mapped_column(
        ForeignKey("plan_items.id", ondelete="CASCADE"), unique=True
    )

    outcome: Mapped[Outcome] = mapped_column(str_enum(Outcome))
    actual_minutes: Mapped[int] = mapped_column(default=0)
    skip_reason: Mapped[SkipReason | None] = mapped_column(str_enum(SkipReason))
    note: Mapped[str | None] = mapped_column(Text)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    plan_item: Mapped[PlanItem] = relationship(back_populates="completion")
