from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.base import TimestampMixin, str_enum
from app.models.enums import GoalStatus


class Goal(TimestampMixin, Base):
    __tablename__ = "goals"
    __table_args__ = (CheckConstraint("priority BETWEEN 1 AND 3", name="priority_range"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50))  # e.g. "learning", "fitness", "project"
    target_date: Mapped[date | None]
    priority: Mapped[int] = mapped_column(SmallInteger, default=2)  # 1 = high, 3 = low
    status: Mapped[GoalStatus] = mapped_column(str_enum(GoalStatus), default=GoalStatus.ACTIVE)

    user: Mapped["User"] = relationship(back_populates="goals")  # noqa: F821
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")  # noqa: F821
