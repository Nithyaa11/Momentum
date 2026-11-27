from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.base import TimestampMixin, str_enum
from app.models.enums import TaskStatus


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("estimated_minutes > 0", name="estimate_positive"),
        CheckConstraint("times_skipped >= 0", name="skips_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    # Optional: some tasks ("renew passport") don't belong to a goal
    goal_id: Mapped[int | None] = mapped_column(
        ForeignKey("goals.id", ondelete="SET NULL"), index=True
    )

    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(50))  # used for per-category estimate accuracy
    estimated_minutes: Mapped[int]
    status: Mapped[TaskStatus] = mapped_column(str_enum(TaskStatus), default=TaskStatus.TODO)
    # Drives the "Is this still important?" prompt after repeated skips
    times_skipped: Mapped[int] = mapped_column(default=0)

    goal: Mapped["Goal | None"] = relationship(back_populates="tasks")  # noqa: F821
