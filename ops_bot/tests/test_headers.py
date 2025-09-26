from fastapi.testclient import TestClient
from ops_bot.app.main import app


client = TestClient(app)


def test_headers_sanitized():
    r = client.get("/headers", headers={"X-Demo": "ok", "Authorization": "secret"})
    assert r.status_code == 200
    data = r.json()["headers"]
    assert "X-Demo" in data
    assert "Authorization" not in data and "authorization" not in data
    # response timing header exists on another endpoint
    r2 = client.get("/ping")
    assert r2.status_code == 200
    assert "X-Request-Duration-ms" in r2.headers
    assert "X-Trace-Id" in r2.headers

