from fastapi.testclient import TestClient


def _create(client: TestClient, **overrides) -> dict:
    body = {"title": "Learn SQL", "category": "learning"} | overrides
    response = client.post("/api/goals", json=body)
    assert response.status_code == 201, response.text
    return response.json()


def test_create_goal_with_defaults(client: TestClient) -> None:
    goal = _create(client)

    assert goal["id"] > 0
    assert goal["title"] == "Learn SQL"
    assert goal["priority"] == 2
    assert goal["status"] == "active"
    assert goal["target_date"] is None


def test_list_goals_sorted_by_priority(client: TestClient) -> None:
    _create(client, title="Low", priority=3)
    _create(client, title="High", priority=1)

    titles = [g["title"] for g in client.get("/api/goals").json()]

    assert titles == ["High", "Low"]


def test_list_goals_filters_by_status(client: TestClient) -> None:
    keep = _create(client, title="Keep")
    archived = _create(client, title="Old")
    client.patch(f"/api/goals/{archived['id']}", json={"status": "archived"})

    active = client.get("/api/goals", params={"status": "active"}).json()

    assert [g["id"] for g in active] == [keep["id"]]


def test_get_goal(client: TestClient) -> None:
    goal = _create(client)

    response = client.get(f"/api/goals/{goal['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Learn SQL"


def test_get_missing_goal_returns_404(client: TestClient) -> None:
    response = client.get("/api/goals/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Goal 999999 not found"}


def test_patch_only_changes_sent_fields(client: TestClient) -> None:
    goal = _create(client, description="Joins and indexes", priority=1)

    response = client.patch(f"/api/goals/{goal['id']}", json={"title": "Master SQL"})

    updated = response.json()
    assert response.status_code == 200
    assert updated["title"] == "Master SQL"
    assert updated["description"] == "Joins and indexes"
    assert updated["priority"] == 1


def test_patch_rejects_null_for_required_fields(client: TestClient) -> None:
    goal = _create(client)

    response = client.patch(f"/api/goals/{goal['id']}", json={"title": None})

    assert response.status_code == 422
    assert client.get(f"/api/goals/{goal['id']}").json()["title"] == "Learn SQL"


def test_patch_can_clear_optional_fields(client: TestClient) -> None:
    goal = _create(client, target_date="2027-01-31")

    response = client.patch(f"/api/goals/{goal['id']}", json={"target_date": None})

    assert response.status_code == 200
    assert response.json()["target_date"] is None


def test_create_goal_rejects_invalid_input(client: TestClient) -> None:
    assert client.post("/api/goals", json={"title": "", "category": "x"}).status_code == 422
    assert (
        client.post("/api/goals", json={"title": "A", "category": "x", "priority": 5}).status_code
        == 422
    )
    assert client.post("/api/goals", json={"category": "x"}).status_code == 422
