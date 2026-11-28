"""Fill the dev database with realistic sample data so every screen has something to show.

Usage (from backend/):
    uv run python -m scripts.seed            # only if the database has no goals yet
    uv run python -m scripts.seed --reset    # wipe everything first, then seed

Inside Docker:
    docker compose exec backend python -m scripts.seed --reset

Creates: one user, 3 goals, a handful of tasks, accepted plans with check-ins for the
past 6 days (a mix of done / partial / skipped, so behavior stats have real gaps between
planned and actual), and an accepted plan for today with nothing checked in yet.
"""

import argparse
import sys
from datetime import date, time, timedelta

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import Base, SessionLocal
from app.models import Completion, Goal, Plan, PlanItem, Task, User
from app.models.enums import Outcome, PlanStatus, SkipReason, TaskStatus, TimeOfDay
from app.services.plan_service import today_for

# (title, category, priority, days until target) → tasks: (title, estimated minutes)
GOALS = [
    (
        "Get comfortable with SQL",
        "learning",
        1,
        45,
        [
            ("SQL JOIN practice", 40),
            ("Window functions chapter", 45),
            ("Solve 3 LeetCode SQL problems", 30),
            ("Indexes and EXPLAIN basics", 35),
            ("Write a query cheat sheet", 25),
        ],
    ),
    (
        "Run a 5K without stopping",
        "fitness",
        2,
        60,
        [
            ("Easy run, 20 minutes", 30),
            ("Interval run", 35),
            ("Stretching routine", 15),
        ],
    ),
    (
        "Ship a side project",
        "project",
        1,
        40,
        [
            ("Sketch the main screens", 30),
            ("Set up the repo and CI", 45),
            ("Build the first API endpoint", 60),
            ("Write the README", 25),
        ],
    ),
]

# Past days, oldest first. Each entry: (task title, planned minutes, outcome, actual, reason).
# Estimates are a bit optimistic on purpose: learning tasks tend to run long.
HISTORY = [
    [
        ("SQL JOIN practice", 40, Outcome.PARTIAL, 25, None),
        ("Stretching routine", 15, Outcome.DONE, 15, None),
    ],
    [
        ("Sketch the main screens", 30, Outcome.DONE, 40, None),
        ("Easy run, 20 minutes", 30, Outcome.SKIPPED, 0, SkipReason.TOO_TIRED),
    ],
    [
        ("Window functions chapter", 45, Outcome.DONE, 60, None),
    ],
    [
        ("Set up the repo and CI", 45, Outcome.SKIPPED, 0, SkipReason.OUT_OF_TIME),
        ("Easy run, 20 minutes", 30, Outcome.DONE, 30, None),
    ],
    [
        ("Set up the repo and CI", 45, Outcome.DONE, 55, None),
        ("Interval run", 35, Outcome.SKIPPED, 0, SkipReason.FORGOT),
    ],
    [
        ("Solve 3 LeetCode SQL problems", 30, Outcome.PARTIAL, 20, None),
    ],
]

TODAY = [
    ("SQL JOIN practice", 40, time(19, 0), "You got halfway last time; finish it while it's fresh."),
    ("Write a query cheat sheet", 25, time(19, 50), "Short and easy, a good way to close the session."),
]


def reset(db: Session) -> None:
    tables = ", ".join(t.name for t in Base.metadata.sorted_tables)
    db.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))


def seed(db: Session) -> None:
    # Reuse the auto-created "Me" user if the app already made one
    user = db.scalar(select(User).order_by(User.id).limit(1))
    if user is None:
        user = User(name="Me")
        db.add(user)
    user.availability = {
        "mon": 45, "tue": 45, "wed": 60, "thu": 45, "fri": 30, "sat": 90, "sun": 60
    }
    user.best_time_of_day = TimeOfDay.EVENING
    db.flush()

    today = today_for(user)
    tasks: dict[str, Task] = {}
    for title, category, priority, days, task_specs in GOALS:
        goal = Goal(
            user_id=user.id,
            title=title,
            category=category,
            priority=priority,
            target_date=today + timedelta(days=days),
        )
        db.add(goal)
        db.flush()
        for task_title, minutes in task_specs:
            task = Task(
                user_id=user.id,
                goal_id=goal.id,
                title=task_title,
                category=category,
                estimated_minutes=minutes,
            )
            db.add(task)
            tasks[task_title] = task
    db.flush()

    for days_ago, entries in zip(range(len(HISTORY), 0, -1), HISTORY):
        day = today - timedelta(days=days_ago)
        plan = Plan(user_id=user.id, date=day, status=PlanStatus.ACCEPTED)
        for position, (title, planned, outcome, actual, skip_reason) in enumerate(entries):
            task = tasks[title]
            item = PlanItem(task=task, position=position, planned_minutes=planned)
            item.completion = Completion(
                outcome=outcome, actual_minutes=actual, skip_reason=skip_reason
            )
            plan.items.append(item)
            # Same side effects a real check-in has
            if outcome is Outcome.DONE:
                task.status = TaskStatus.DONE
            elif outcome is Outcome.SKIPPED:
                task.times_skipped += 1
        db.add(plan)

    today_plan = Plan(
        user_id=user.id,
        date=today,
        status=PlanStatus.ACCEPTED,
        rationale="One focused SQL block in the evening, when you get the most done, then a short wrap-up.",
    )
    for position, (title, planned, start, reason) in enumerate(TODAY):
        today_plan.items.append(
            PlanItem(
                task=tasks[title],
                position=position,
                planned_minutes=planned,
                scheduled_start=start,
                reason=reason,
            )
        )
    db.add(today_plan)


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the dev database with sample data.")
    parser.add_argument("--reset", action="store_true", help="delete ALL existing data first")
    args = parser.parse_args()

    if get_settings().environment == "production":
        sys.exit("Refusing to seed a production database.")

    with SessionLocal() as db:
        if args.reset:
            reset(db)
        elif db.scalar(select(func.count()).select_from(Goal)):
            sys.exit("The database already has goals. Run with --reset to wipe it and seed again.")
        seed(db)
        db.commit()

    task_count = sum(len(goal[4]) for goal in GOALS)
    print(
        f"Seeded {len(GOALS)} goals, {task_count} tasks, "
        f"{len(HISTORY)} past days of check-ins, and today's plan."
    )


if __name__ == "__main__":
    main()
