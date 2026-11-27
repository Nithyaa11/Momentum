from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.db import get_db
from app.main import app


def _client_with_db(db: MagicMock) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app)


def teardown_function() -> None:
    app.dependency_overrides.clear()


def test_health_ok_when_database_reachable() -> None:
    client = _client_with_db(MagicMock())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_503_when_database_down() -> None:
    db = MagicMock()
    db.execute.side_effect = OperationalError("SELECT 1", {}, Exception("down"))
    client = _client_with_db(db)

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "unavailable"}
