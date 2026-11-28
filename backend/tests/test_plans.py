from fastapi.testclient import TestClient

DAY = "2026-12-01"


def _task(client: TestClient, title: str = "JOIN practice", minutes: int = 40) -> dict:
    body = {"title": title, "category": "learning", "estimated_minutes": minutes}
    return client.post("/api/tasks", json=body).json()


def _plan(client: TestClient, *tasks: dict, day: str = DAY) -> dict:
    items = [{"task_id": t["id"], "planned_minutes": t["estimated_minutes"]} for t in tasks]
    response = client.put(f"/api/plans/{day}", json={"items": items, "rationale": "Test plan"})
    assert response.status_code == 200, response.text
    return response.json()


def _checkin(client: TestClient, item_id: int, **body) -> "TestClient":
    return client.put(f"/api/plan-items/{item_id}/checkin", json=body)


# ---------- Plans ----------


def test_create_plan_keeps_item_order_and_starts_proposed(client: TestClient) -> None:
    a, b = _task(client, "A"), _task(client, "B", 25)

    plan = _plan(client, b, a)

    assert plan["date"] == DAY
    assert plan["status"] == "proposed"
    assert plan["rationale"] == "Test plan"
    assert [i["task"]["title"] for i in plan["items"]] == ["B", "A"]
    assert [i["position"] for i in plan["items"]] == [0, 1]
    assert plan["items"][0]["planned_minutes"] == 25
    assert plan["items"][0]["completion"] is None


def test_get_plan_and_missing_plan(client: TestClient) -> None:
    _plan(client, _task(client))

    assert client.get(f"/api/plans/{DAY}").status_code == 200
    assert client.get("/api/plans/2030-01-01").status_code == 404


def test_get_today_uses_users_today(client: TestClient) -> None:
    from datetime import UTC, datetime

    today = datetime.now(UTC).date().isoformat()  # test user's timezone is UTC
    _plan(client, _task(client), day=today)

    response = client.get("/api/plans/today")

    assert response.status_code == 200
    assert response.json()["date"] == today


def test_replace_plan_before_any_checkin(client: TestClient) -> None:
    a, b = _task(client, "A"), _task(client, "B")
    _plan(client, a)

    replaced = _plan(client, b)

    assert [i["task"]["title"] for i in replaced["items"]] == ["B"]


def test_replace_plan_after_checkin_is_rejected(client: TestClient) -> None:
    a, b = _task(client, "A"), _task(client, "B")
    plan = _plan(client, a)
    _checkin(client, plan["items"][0]["id"], outcome="done")

    response = client.put(f"/api/plans/{DAY}", json={"items": [{"task_id": b["id"], "planned_minutes": 10}]})

    assert response.status_code == 409


def test_accept_plan(client: TestClient) -> None:
    _plan(client, _task(client))

    response = client.post(f"/api/plans/{DAY}/accept")

    assert response.json()["status"] == "accepted"


def test_plan_rejects_unknown_closed_and_duplicate_tasks(client: TestClient) -> None:
    task = _task(client)
    done = _task(client, "Done already")
    client.patch(f"/api/tasks/{done['id']}", json={"status": "done"})

    def put(items: list[dict]) -> int:
        return client.put(f"/api/plans/{DAY}", json={"items": items}).status_code

    assert put([{"task_id": 999999, "planned_minutes": 10}]) == 422
    assert put([{"task_id": done["id"], "planned_minutes": 10}]) == 422
    assert put([{"task_id": task["id"], "planned_minutes": 10}] * 2) == 422
    assert put([{"task_id": task["id"], "planned_minutes": 0}]) == 422


# ---------- Check-ins ----------


def test_done_marks_task_done_and_defaults_actual_to_planned(client: TestClient) -> None:
    task = _task(client, minutes=40)
    item_id = _plan(client, task)["items"][0]["id"]

    plan = _checkin(client, item_id, outcome="done").json()

    completion = plan["items"][0]["completion"]
    assert completion["outcome"] == "done"
    assert completion["actual_minutes"] == 40
    assert client.get(f"/api/tasks/{task['id']}").json()["status"] == "done"


def test_partial_records_actual_minutes_and_keeps_task_open(client: TestClient) -> None:
    task = _task(client, minutes=120)
    item_id = _plan(client, task)["items"][0]["id"]

    plan = _checkin(
        client, item_id, outcome="partial", actual_minutes=30, skip_reason="too_tired"
    ).json()

    completion = plan["items"][0]["completion"]
    assert completion["actual_minutes"] == 30
    assert completion["skip_reason"] == "too_tired"
    assert client.get(f"/api/tasks/{task['id']}").json()["status"] == "todo"


def test_skip_counts_skips(client: TestClient) -> None:
    task = _task(client)
    item_id = _plan(client, task)["items"][0]["id"]

    plan = _checkin(client, item_id, outcome="skipped", skip_reason="out_of_time").json()

    assert plan["items"][0]["completion"]["actual_minutes"] == 0
    assert client.get(f"/api/tasks/{task['id']}").json()["times_skipped"] == 1


def test_checkin_validation_rules(client: TestClient) -> None:
    item_id = _plan(client, _task(client))["items"][0]["id"]

    assert _checkin(client, item_id, outcome="skipped").status_code == 422  # no reason
    assert (
        _checkin(client, item_id, outcome="skipped", skip_reason="forgot", actual_minutes=10)
    ).status_code == 422
    assert _checkin(client, item_id, outcome="partial").status_code == 422  # no minutes
    assert _checkin(client, item_id, outcome="done", skip_reason="forgot").status_code == 422
    assert _checkin(client, 999999, outcome="done").status_code == 404


def test_changing_a_checkin_reverses_the_old_effect(client: TestClient) -> None:
    task = _task(client)
    item_id = _plan(client, task)["items"][0]["id"]

    _checkin(client, item_id, outcome="skipped", skip_reason="forgot")
    plan = _checkin(client, item_id, outcome="done").json()

    state = client.get(f"/api/tasks/{task['id']}").json()
    assert plan["items"][0]["completion"]["outcome"] == "done"
    assert state["times_skipped"] == 0
    assert state["status"] == "done"


def test_undo_checkin_restores_task(client: TestClient) -> None:
    task = _task(client)
    item_id = _plan(client, task)["items"][0]["id"]
    _checkin(client, item_id, outcome="done")

    response = client.delete(f"/api/plan-items/{item_id}/checkin")

    assert response.status_code == 200
    assert response.json()["items"][0]["completion"] is None
    assert client.get(f"/api/tasks/{task['id']}").json()["status"] == "todo"
    assert client.delete(f"/api/plan-items/{item_id}/checkin").status_code == 404


def test_plan_can_be_replaced_again_after_undo(client: TestClient) -> None:
    a, b = _task(client, "A"), _task(client, "B")
    item_id = _plan(client, a)["items"][0]["id"]
    _checkin(client, item_id, outcome="done")
    client.delete(f"/api/plan-items/{item_id}/checkin")

    replaced = _plan(client, b)

    assert [i["task"]["title"] for i in replaced["items"]] == ["B"]
