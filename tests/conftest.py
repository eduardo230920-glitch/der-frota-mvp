import pytest
from app import app, init_db

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    app.config.update(TESTING=True, DATABASE=str(db_path), SECRET_KEY="test-secret")
    init_db()
    with app.test_client() as client:
        yield client

def login(client):
    with client.session_transaction() as sess:
        sess["_csrf_token"] = "test-token"
    return client.post("/login", data={
        "_csrf_token": "test-token",
        "username": "servidor.der",
        "password": "Der@12345",
    }, follow_redirects=True)
