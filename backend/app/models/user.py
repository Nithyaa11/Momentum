from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.base import TimestampMixin, str_enum
from app.models.enums import TimeOfDay


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")

    # Free minutes per weekday, e.g. {"mon": 60, "tue": 45, ..., "sun": 120}
    availability: Mapped[dict[str, int]] = mapped_column(JSONB, default=dict)
    best_time_of_day: Mapped[TimeOfDay | None] = mapped_column(str_enum(TimeOfDay))

    goals: Mapped[list["Goal"]] = relationship(back_populates="user")  # noqa: F821
