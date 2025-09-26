from fastapi.testclient import TestClient
from ops_bot.app.main import app


client = TestClient(app)


def test_change_submit():
    payload = {"env": "dev", "summary": "Test change", "description": "desc"}
    r = client.post("/change/submit", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "pending_approval"
    assert "change" in data

