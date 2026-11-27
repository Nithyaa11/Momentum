from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User


def get_current_user(db: Session = Depends(get_db)) -> User:
    """V1 is single-user: everything belongs to the first user, created on first use.
    Replaced by real authentication in V1.1."""
    user = db.scalar(select(User).order_by(User.id).limit(1))
    if user is None:
        user = User(name="Me", availability={})
        db.add(user)
        db.commit()
    return user
