from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas.plan import CheckInIn, PlanIn, PlanRead
from app.services import plan_service

router = APIRouter(tags=["plans"])


# "today" is declared before "/{plan_date}" so it isn't parsed as a date
@router.get("/plans/today", response_model=PlanRead)
def get_today(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Today's plan, using the user's timezone."""
    return plan_service.get_plan(db, user, plan_service.today_for(user))


@router.get("/plans/{plan_date}", response_model=PlanRead)
def get_plan(
    plan_date: date, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return plan_service.get_plan(db, user, plan_date)


@router.put("/plans/{plan_date}", response_model=PlanRead)
def put_plan(
    plan_date: date,
    data: PlanIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create or replace a day's plan. Rejected with 409 once anything is checked in."""
    return plan_service.put_plan(db, user, plan_date, data)


@router.post("/plans/{plan_date}/accept", response_model=PlanRead)
def accept_plan(
    plan_date: date, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return plan_service.accept_plan(db, user, plan_date)


@router.put("/plan-items/{item_id}/checkin", response_model=PlanRead)
def check_in(
    item_id: int,
    data: CheckInIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Record what happened (done / partial / skipped). Sending it again changes it.
    Returns the whole updated plan so the UI can refresh in one go."""
    return plan_service.check_in(db, user, item_id, data)


@router.delete("/plan-items/{item_id}/checkin", response_model=PlanRead)
def undo_check_in(
    item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    """Undo a check-in (powers the Undo toast)."""
    return plan_service.undo_check_in(db, user, item_id)
