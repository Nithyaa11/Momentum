"""Test fixtures backed by a real PostgreSQL test database.

- The `momentum_test` database is created if missing and rebuilt with Alembic once per
  run (which also checks that the migrations work).
- Each test runs inside a transaction that is rolled back afterwards, so tests never
  see each other's data.
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.main import app

TEST_DATABASE_URL = get_settings().test_database_url
ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"


def _ensure_database_exists(url: str) -> None:
    target = make_url(url)
    admin = create_engine(target.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        exists = conn.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": target.database}
        )
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{target.database}"'))
    admin.dispose()


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    _ensure_database_exists(TEST_DATABASE_URL)

    config = Config(str(ALEMBIC_INI))
    config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.downgrade(config, "base")
    command.upgrade(config, "head")

    engine = create_engine(TEST_DATABASE_URL)
    yield engine
    engine.dispose()


@pytest.fixture
def db(engine: Engine) -> Iterator[Session]:
    connection = engine.connect()
    transaction = connection.begin()
    # Commits inside the app become savepoints; the outer transaction is rolled back
    session = Session(
        bind=connection, join_transaction_mode="create_savepoint", expire_on_commit=False
    )
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()
