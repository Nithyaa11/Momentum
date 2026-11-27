from datetime import date

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base import TimestampMixin, str_enum
from app.models.enums import WinSource


class Win(TimestampMixin, Base):
    __tablename__ = "wins"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    goal_id: Mapped[int | None] = mapped_column(ForeignKey("goals.id", ondelete="SET NULL"))

    source: Mapped[WinSource] = mapped_column(str_enum(WinSource))
    kind: Mapped[str] = mapped_column(String(50))  # e.g. "session", "streak", "milestone", "custom"
    description: Mapped[str] = mapped_column(String(300))
    date: Mapped[date]


class BehaviorSnapshot(TimestampMixin, Base):
    """Nightly summary of how the user actually behaves. Computed with plain
    statistics (no LLM) and fed to the planner as compact context."""

    __tablename__ = "behavior_snapshots"
    __table_args__ = (UniqueConstraint("user_id", "date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    date: Mapped[date]

    # {"coding": {"ratio": 1.6, "n": 9}, ...}: median actual / planned per category
    estimate_ratio_by_category: Mapped[dict] = mapped_column(JSONB, default=dict)
    # {"morning": 0.81, "evening": 0.28, ...}
    completion_rate_by_time_of_day: Mapped[dict] = mapped_column(JSONB, default=dict)
    # {"mon": 0.7, ..., "fri": 0.4}
    completion_rate_by_weekday: Mapped[dict] = mapped_column(JSONB, default=dict)
    # {"under_60": 0.82, "over_60": 0.35}
    completion_rate_by_session_length: Mapped[dict] = mapped_column(JSONB, default=dict)
    # {"too_tired": 4, "out_of_time": 2}
    skip_reason_counts: Mapped[dict] = mapped_column(JSONB, default=dict)
    # sum(actual) / sum(planned) over the window
    overall_completion_rate: Mapped[float | None]
