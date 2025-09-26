from fastapi.testclient import TestClient
from ops_bot.app.main import app


client = TestClient(app)


def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_version():
    resp = client.get("/version")
    assert resp.status_code == 200
    assert "git_sha" in resp.json()


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("service") == "DriftHawk Ops Bot"
    resp = client.post("/chatops/plan-brief", json={"env": "dev"})
    assert resp.status_code == 200
    body = resp.json()
    assert "brief" in body and "markdown" in body


def test_info_and_security_headers():
    r = client.get("/info")
    assert r.status_code == 200
    data = r.json()
    assert "version" in data and "git_sha" in data
    # security headers present
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    r = client.get("/robots.txt")
    assert r.status_code == 200 and "Disallow: /" in r.text
    r = client.get("/env")
    assert r.status_code == 200 and "log_level" in r.json()
    r = client.get("/flags")
    assert r.status_code == 200
    data = r.json()
    assert "enable_metrics" in data and "enable_slack" in data
    # uptime and HEAD handlers
    r = client.get("/uptime")
    assert r.status_code == 200 and r.json()["uptime_seconds"] >= 0
    r = client.head("/ping")
    assert r.status_code == 200
    r = client.head("/healthz")
    assert r.status_code == 200
    r = client.head("/readyz")
    assert r.status_code == 200
    # echo
    r = client.post("/echo", json={"message": "hi"})
    assert r.status_code == 200 and r.json()["echo"] == "hi"

