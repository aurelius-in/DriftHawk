from fastapi.testclient import TestClient
from ops_bot.app.main import app


client = TestClient(app)


def test_healthz_details():
  r = client.get("/healthz")
  assert r.status_code == 200
  data = r.json()
  assert data.get("status") == "ok"
  assert "version" in data and "git_sha" in data

