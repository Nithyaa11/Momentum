from datetime import date, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Completion, Plan, PlanItem, Task, User
from app.models.enums import Outcome, PlanStatus, TaskStatus
from app.schemas.plan import CheckInIn, PlanIn
from app.services.errors import ConflictError, NotFoundError, ValidationError


def today_for(user: User) -> date:
    """The current date in the user's own timezone."""
    try:
        return datetime.now(ZoneInfo(user.timezone)).date()
    except ZoneInfoNotFoundError:
        return datetime.now(ZoneInfo("UTC")).date()


# ---------- Plans ----------


def _load_plan(db: Session, user: User, plan_date: date) -> Plan | None:
    return db.scalar(
        select(Plan)
        .where(Plan.user_id == user.id, Plan.date == plan_date)
        .options(
            selectinload(Plan.items).selectinload(PlanItem.task),
            selectinload(Plan.items).selectinload(PlanItem.completion),
        )
        .execution_options(populate_existing=True)
    )


def get_plan(db: Session, user: User, plan_date: date) -> Plan:
    plan = _load_plan(db, user, plan_date)
    if plan is None:
        raise NotFoundError("Plan for", plan_date.isoformat())
    return plan


def put_plan(db: Session, user: User, plan_date: date, data: PlanIn) -> Plan:
    """Create the day's plan, or replace it if nothing has been checked in yet.
    A new or replaced plan starts as 'proposed' until the user accepts it."""
    plan = _load_plan(db, user, plan_date)
    if plan is not None and any(item.completion for item in plan.items):
        raise ConflictError(
            "this plan already has check-ins; it can't be replaced (use replanning instead)"
        )

    tasks = _owned_open_tasks(db, user, [item.task_id for item in data.items])

    if plan is None:
        plan = Plan(user_id=user.id, date=plan_date)
        db.add(plan)
    else:
        plan.items.clear()
        db.flush()  # delete old items before inserting new ones

    plan.status = PlanStatus.PROPOSED
    plan.rationale = data.rationale
    for position, item in enumerate(data.items):
        plan.items.append(
            PlanItem(
                task=tasks[item.task_id],
                position=position,
                planned_minutes=item.planned_minutes,
                scheduled_start=item.scheduled_start,
                reason=item.reason,
            )
        )
    db.commit()
    return get_plan(db, user, plan_date)


def accept_plan(db: Session, user: User, plan_date: date) -> Plan:
    plan = get_plan(db, user, plan_date)
    plan.status = PlanStatus.ACCEPTED
    db.commit()
    return get_plan(db, user, plan_date)


def _owned_open_tasks(db: Session, user: User, task_ids: list[int]) -> dict[int, Task]:
    if not task_ids:
        return {}
    tasks = {
        t.id: t
        for t in db.scalars(select(Task).where(Task.id.in_(task_ids), Task.user_id == user.id))
    }
    missing = [tid for tid in task_ids if tid not in tasks]
    if missing:
        raise ValidationError(f"unknown task_id(s): {missing}")
    closed = [tid for tid in task_ids if tasks[tid].status != TaskStatus.TODO]
    if closed:
        raise ValidationError(f"task(s) already done or dropped: {closed}")
    return tasks


# ---------- Check-ins ----------


def _get_item(db: Session, user: User, item_id: int) -> PlanItem:
    item = db.get(PlanItem, item_id)
    if item is None or item.plan.user_id != user.id:
        raise NotFoundError("Plan item", item_id)
    return item


def _apply_task_effect(task: Task, outcome: Outcome, sign: int) -> None:
    """Apply (sign=+1) or reverse (sign=-1) what a check-in does to its task."""
    if outcome == Outcome.DONE:
        task.status = TaskStatus.DONE if sign > 0 else TaskStatus.TODO
    elif outcome == Outcome.SKIPPED:
        task.times_skipped = max(0, task.times_skipped + sign)


def check_in(db: Session, user: User, item_id: int, data: CheckInIn) -> Plan:
    """Record (or change) what happened with a plan item."""
    item = _get_item(db, user, item_id)

    if data.outcome == Outcome.DONE:
        actual = data.actual_minutes if data.actual_minutes is not None else item.planned_minutes
    else:
        actual = data.actual_minutes or 0

    if item.completion is not None:  # changing an earlier check-in: undo its effect first
        _apply_task_effect(item.task, item.completion.outcome, -1)
        completion = item.completion
    else:
        completion = Completion()
        item.completion = completion

    completion.outcome = data.outcome
    completion.actual_minutes = actual
    completion.skip_reason = data.skip_reason
    completion.note = data.note
    completion.completed_at = datetime.now(ZoneInfo("UTC"))
    _apply_task_effect(item.task, data.outcome, +1)

    db.commit()
    return get_plan(db, user, item.plan.date)


def undo_check_in(db: Session, user: User, item_id: int) -> Plan:
    item = _get_item(db, user, item_id)
    if item.completion is None:
        raise NotFoundError("Check-in for plan item", item_id)

    _apply_task_effect(item.task, item.completion.outcome, -1)
    item.completion = None  # delete-orphan cascade removes the row
    db.commit()
    return get_plan(db, user, item.plan.date)
