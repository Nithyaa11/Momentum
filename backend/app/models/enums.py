from enum import StrEnum


class TimeOfDay(StrEnum):
    MORNING = "morning"  # 05:00–12:00
    AFTERNOON = "afternoon"  # 12:00–17:00
    EVENING = "evening"  # 17:00–21:00
    NIGHT = "night"  # 21:00–05:00


class GoalStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskStatus(StrEnum):
    TODO = "todo"
    DONE = "done"
    DROPPED = "dropped"


class PlanStatus(StrEnum):
    PROPOSED = "proposed"  # written by the agent, waiting for the user
    ACCEPTED = "accepted"  # the user approved (possibly after editing)


class Outcome(StrEnum):
    DONE = "done"
    PARTIAL = "partial"
    SKIPPED = "skipped"


class SkipReason(StrEnum):
    TOO_TIRED = "too_tired"
    OUT_OF_TIME = "out_of_time"
    FORGOT = "forgot"
    NOT_IMPORTANT = "not_important"
    OTHER = "other"


class WinSource(StrEnum):
    AUTO = "auto"  # detected by the system (session done, streak, milestone)
    MANUAL = "manual"  # logged by the user ("hit my protein goal")
