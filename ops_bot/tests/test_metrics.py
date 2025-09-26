from fastapi.testclient import TestClient
from ops_bot.app.main import app


client = TestClient(app)


def test_metrics_endpoint():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "ops_bot_requests_total" in r.text
