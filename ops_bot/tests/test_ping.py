from fastapi.testclient import TestClient
from ops_bot.app.main import app


client = TestClient(app)


def test_ping():
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.json().get("pong") is True
