from tests.conftest import register_and_login


def test_register(client):
    res = client.post("/api/auth/register", json={
        "email": "new@test.com",
        "password": "password123",
    })
    assert res.status_code == 201
    assert res.json["email"] == "new@test.com"


def test_register_duplicate(client):
    client.post("/api/auth/register", json={"email": "a@b.com", "password": "password123"})
    res = client.post("/api/auth/register", json={"email": "a@b.com", "password": "password123"})
    assert res.status_code == 409


def test_register_short_password(client):
    res = client.post("/api/auth/register", json={"email": "a@b.com", "password": "12345"})
    assert res.status_code == 400


def test_login(client):
    register_and_login(client)
    client.post("/api/auth/logout")
    res = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123",
    })
    assert res.status_code == 200


def test_login_wrong_password(client):
    register_and_login(client)
    client.post("/api/auth/logout")
    res = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "wrong",
    })
    assert res.status_code == 401


def test_me(client):
    register_and_login(client)
    res = client.get("/api/auth/me")
    assert res.status_code == 200
    assert res.json["email"] == "test@example.com"


def test_me_unauthenticated(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401


def test_logout(client):
    register_and_login(client)
    res = client.post("/api/auth/logout")
    assert res.status_code == 200
    res = client.get("/api/auth/me")
    assert res.status_code == 401
