from tests.conftest import register_and_login


def test_program_crud(client):
    c = register_and_login(client)

    # Create
    res = c.post("/api/programs", json={"name": "PPL", "schedule_days_per_week": 3})
    assert res.status_code == 201
    pid = res.json["id"]

    # List
    res = c.get("/api/programs")
    assert res.status_code == 200
    assert len(res.json) == 1

    # Get
    res = c.get(f"/api/programs/{pid}")
    assert res.status_code == 200
    assert res.json["name"] == "PPL"

    # Update
    res = c.put(f"/api/programs/{pid}", json={"name": "Push Pull Legs"})
    assert res.status_code == 200
    assert res.json["name"] == "Push Pull Legs"

    # Delete
    res = c.delete(f"/api/programs/{pid}")
    assert res.status_code == 200
    res = c.get("/api/programs")
    assert len(res.json) == 0


def test_workout_crud(client):
    c = register_and_login(client)

    res = c.post("/api/workouts", json={"name": "Workout A"})
    assert res.status_code == 201
    wid = res.json["id"]

    res = c.get(f"/api/workouts/{wid}")
    assert res.json["name"] == "Workout A"

    res = c.put(f"/api/workouts/{wid}", json={"name": "Workout B"})
    assert res.json["name"] == "Workout B"

    res = c.delete(f"/api/workouts/{wid}")
    assert res.status_code == 200


def test_exercise_crud(client):
    c = register_and_login(client)

    res = c.post("/api/exercises", json={"name": "Squat", "type": "strength"})
    assert res.status_code == 201
    eid = res.json["id"]

    res = c.post("/api/exercises", json={"name": "Peloton", "type": "cardio"})
    assert res.status_code == 201

    res = c.get("/api/exercises")
    assert len(res.json) == 2

    res = c.put(f"/api/exercises/{eid}", json={"name": "Back Squat"})
    assert res.json["name"] == "Back Squat"

    res = c.delete(f"/api/exercises/{eid}")
    assert res.status_code == 200


def test_add_exercise_to_workout(client):
    c = register_and_login(client)

    ex = c.post("/api/exercises", json={"name": "Bench", "type": "strength"}).json
    w = c.post("/api/workouts", json={"name": "Push"}).json

    res = c.post(f"/api/workouts/{w['id']}/exercises", json={
        "exercise_id": ex["id"],
        "default_sets": 5,
        "default_reps": 5,
        "default_weight": 135,
    })
    assert res.status_code == 201
    assert len(res.json["exercises"]) == 1
    assert res.json["exercises"][0]["default_weight"] == 135


def test_program_workout_order(client):
    c = register_and_login(client)

    p = c.post("/api/programs", json={"name": "Test"}).json
    w1 = c.post("/api/workouts", json={"name": "A"}).json
    w2 = c.post("/api/workouts", json={"name": "B"}).json

    res = c.put(f"/api/programs/{p['id']}/order", json={
        "workout_ids": [w1["id"], w2["id"]],
    })
    assert res.status_code == 200
    assert len(res.json["workouts"]) == 2
    assert res.json["workouts"][0]["name"] == "A"
