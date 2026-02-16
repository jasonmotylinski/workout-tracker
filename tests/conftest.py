import pytest
from app import create_app, db as _db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


def register_and_login(client, email="test@example.com", password="password123"):
    client.post("/api/auth/register", json={"email": email, "password": password})
    return client
