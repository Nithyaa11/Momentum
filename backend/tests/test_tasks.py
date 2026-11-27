from fastapi.testclient import TestClient


def _goal(client: TestClient) -> dict:
    return client.post("/api/goals", json={"title": "Learn SQL", "category": "learning"}).json()


def _task(client: TestClient, **overrides) -> dict:
    body = {"title": "JOIN practice", "category": "learning", "estimated_minutes": 40} | overrides
    response = client.post("/api/tasks", json=body)
    assert response.status_code == 201, response.text
    return response.json()


def test_create_task_under_goal(client: TestClient) -> None:
    goal = _goal(client)

    task = _task(client, goal_id=goal["id"])

    assert task["goal_id"] == goal["id"]
    assert task["status"] == "todo"
    assert task["times_skipped"] == 0


def test_create_task_without_goal(client: TestClient) -> None:
    task = _task(client, title="Renew passport", category="admin")

    assert task["goal_id"] is None


def test_create_task_with_unknown_goal_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/tasks",
        json={"title": "X", "category": "y", "estimated_minutes": 10, "goal_id": 999999},
    )

    assert response.status_code == 422
    assert "goal_id 999999" in response.json()["detail"]


def test_estimated_minutes_must_be_between_1_and_240(client: TestClient) -> None:
    for minutes in (0, -5, 241):
        response = client.post(
            "/api/tasks", json={"title": "X", "category": "y", "estimated_minutes": minutes}
        )
        assert response.status_code == 422, minutes


def test_list_tasks_filters(client: TestClient) -> None:
    goal = _goal(client)
    in_goal = _task(client, goal_id=goal["id"])
    done = _task(client, title="Other")
    client.patch(f"/api/tasks/{done['id']}", json={"status": "done"})

    by_goal = client.get("/api/tasks", params={"goal_id": goal["id"]}).json()
    by_status = client.get("/api/tasks", params={"status": "done"}).json()

    assert [t["id"] for t in by_goal] == [in_goal["id"]]
    assert [t["id"] for t in by_status] == [done["id"]]


def test_patch_task(client: TestClient) -> None:
    task = _task(client)

    response = client.patch(f"/api/tasks/{task['id']}", json={"estimated_minutes": 25})

    assert response.status_code == 200
    assert response.json()["estimated_minutes"] == 25
    assert response.json()["title"] == "JOIN practice"


def test_patch_task_to_unknown_goal_is_rejected(client: TestClient) -> None:
    task = _task(client)

    response = client.patch(f"/api/tasks/{task['id']}", json={"goal_id": 999999})

    assert response.status_code == 422


def test_patch_task_rejects_null_minutes_but_allows_detaching_goal(client: TestClient) -> None:
    goal = _goal(client)
    task = _task(client, goal_id=goal["id"])

    bad = client.patch(f"/api/tasks/{task['id']}", json={"estimated_minutes": None})
    detach = client.patch(f"/api/tasks/{task['id']}", json={"goal_id": None})

    assert bad.status_code == 422
    assert detach.status_code == 200
    assert detach.json()["goal_id"] is None


def test_get_missing_task_returns_404(client: TestClient) -> None:
    assert client.get("/api/tasks/999999").status_code == 404
