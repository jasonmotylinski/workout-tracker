from tests.conftest import register_and_login


def setup_workout(client):
    """Helper to create a program with a workout and exercises."""
    c = register_and_login(client)

    ex1 = c.post("/api/exercises", json={"name": "Squat", "type": "strength"}).json
    ex2 = c.post("/api/exercises", json={"name": "Peloton", "type": "cardio"}).json

    w = c.post("/api/workouts", json={"name": "Full Body"}).json
    c.post(f"/api/workouts/{w['id']}/exercises", json={
        "exercise_id": ex1["id"], "default_sets": 3, "default_reps": 5, "default_weight": 135,
    })
    c.post(f"/api/workouts/{w['id']}/exercises", json={
        "exercise_id": ex2["id"], "default_sets": 1, "default_reps": 1, "default_duration_minutes": 30,
    })

    p = c.post("/api/programs", json={"name": "Test Program"}).json
    c.put(f"/api/programs/{p['id']}/order", json={"workout_ids": [w["id"]]})

    return c, p, w, ex1, ex2


def test_start_workout(client):
    c, p, w, ex1, ex2 = setup_workout(client)

    res = c.post("/api/logs", json={"workout_id": w["id"], "program_id": p["id"]})
    assert res.status_code == 201
    log = res.json
    assert log["workout_name"] == "Full Body"

    # Should have 3 strength sets + 1 cardio set = 4 sets
    assert len(log["sets"]) == 4

    strength_sets = [s for s in log["sets"] if s["exercise_type"] == "strength"]
    cardio_sets = [s for s in log["sets"] if s["exercise_type"] == "cardio"]
    assert len(strength_sets) == 3
    assert len(cardio_sets) == 1
    assert strength_sets[0]["planned_reps"] == 5
    assert strength_sets[0]["weight"] == 135
    assert cardio_sets[0]["duration_minutes"] == 30


def test_toggle_set(client):
    c, p, w, ex1, ex2 = setup_workout(client)

    log = c.post("/api/logs", json={"workout_id": w["id"], "program_id": p["id"]}).json
    set_id = log["sets"][0]["id"]

    # Mark complete
    res = c.put(f"/api/logs/{log['id']}/sets/{set_id}", json={
        "completed": True, "actual_reps": 5,
    })
    assert res.status_code == 200
    assert res.json["completed"] is True
    assert res.json["actual_reps"] == 5

    # Partial reps
    res = c.put(f"/api/logs/{log['id']}/sets/{set_id}", json={
        "actual_reps": 3,
    })
    assert res.json["actual_reps"] == 3


def test_complete_workout(client):
    c, p, w, ex1, ex2 = setup_workout(client)

    log = c.post("/api/logs", json={"workout_id": w["id"], "program_id": p["id"]}).json

    res = c.put(f"/api/logs/{log['id']}", json={
        "complete": True, "notes": "Good session", "body_weight": 155.0,
    })
    assert res.status_code == 200
    assert res.json["completed_at"] is not None
    assert res.json["notes"] == "Good session"
    assert res.json["body_weight"] == 155.0


def test_history(client):
    c, p, w, ex1, ex2 = setup_workout(client)

    c.post("/api/logs", json={"workout_id": w["id"], "program_id": p["id"]})

    res = c.get("/api/logs")
    assert res.status_code == 200
    assert len(res.json) == 1


def test_calendar(client):
    c, p, w, ex1, ex2 = setup_workout(client)

    log = c.post("/api/logs", json={"workout_id": w["id"], "program_id": p["id"]}).json

    # Get current month/year from the log
    from datetime import datetime
    dt = datetime.fromisoformat(log["started_at"].replace("Z", "+00:00"))

    res = c.get(f"/api/logs/calendar?month={dt.month}&year={dt.year}")
    assert res.status_code == 200
    assert len(res.json["workout_dates"]) == 1


def test_next_workout(client):
    c, p, w, ex1, ex2 = setup_workout(client)

    res = c.get(f"/api/programs/{p['id']}/next")
    assert res.status_code == 200
    assert res.json["next_workout"]["name"] == "Full Body"
