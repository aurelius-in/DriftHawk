from fastapi.testclient import TestClient
from ops_bot.app.main import app


client = TestClient(app, raise_server_exceptions=False)


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
    # config and request id
    r = client.get("/config")
    assert r.status_code == 200 and "expose_headers" in r.json()
    r = client.get("/request-id")
    assert r.status_code == 200 and "request_id" in r.json()
    # time and whoami
    r = client.get("/time")
    assert r.status_code == 200 and r.json()["epoch"] > 0
    r = client.get("/whoami")
    assert r.status_code == 200 and "ip" in r.json()
    # JSON 404
    r = client.get("/this-does-not-exist")
    assert r.status_code == 404 and r.json().get("error") == "not_found"
    # statusz and alive/ready
    r = client.get("/statusz")
    assert r.status_code == 200 and r.json().get("status") == "ok"
    r = client.head("/alive")
    assert r.status_code == 200
    r = client.head("/ready")
    assert r.status_code == 200
    # uuid and random
    r = client.get("/uuid")
    assert r.status_code == 200 and len(r.json().get("uuid", "")) > 0
    r = client.get("/random", params={"length": 8})
    assert r.status_code == 200 and r.json().get("length") == 8
    r = client.get("/random", params={"length": 1024})
    assert r.status_code == 422
    # hostname and env key
    r = client.get("/hostname")
    assert r.status_code == 200 and "hostname" in r.json()
    r = client.get("/env/LOG_LEVEL")
    assert r.status_code == 200 and "key" in r.json()
    # sum
    r = client.post("/sum", json={"numbers": [1, 2, 3.5]})
    assert r.status_code == 200 and r.json().get("sum") == 6.5
    # hash
    r = client.post("/hash", json={"text": "abc", "algorithm": "sha256"})
    assert r.status_code == 200 and len(r.json().get("hex", "")) == 64
    r = client.get("/hash", params={"text": "abc", "algorithm": "sha512"})
    assert r.status_code == 200 and len(r.json().get("hex", "")) == 128
    # case and reverse
    assert client.post("/uppercase", json={"text": "a"}).json()["text"] == "A"
    assert client.post("/lowercase", json={"text": "A"}).json()["text"] == "a"
    assert client.post("/reverse", json={"text": "ab"}).json()["text"] == "ba"
    # b64
    enc = client.post("/b64", json={"text": "hi", "mode": "encode"}).json()["result"]
    dec = client.post("/b64", json={"text": enc, "mode": "decode"}).json()["result"]
    assert dec == "hi"
    # urlsafe b64
    enc2 = client.post("/b64", json={"text": "/+a=", "mode": "encode", "urlsafe": True}).json()["result"]
    dec2 = client.post("/b64", json={"text": enc2, "mode": "decode", "urlsafe": True}).json()["result"]
    assert dec2 == "/+a="
    # hex encode/decode
    hx = client.post("/hex", json={"text": "hi", "mode": "encode"}).json()["result"]
    assert client.post("/hex", json={"text": hx, "mode": "decode"}).json()["result"] == "hi"
    # randint
    r = client.get("/randint", params={"min": 1, "max": 2})
    assert r.status_code == 200 and r.json()["value"] in (1, 2)
    # randbool
    r = client.get("/randbool")
    assert r.status_code == 200 and isinstance(r.json()["value"], bool)
    # sleep
    r = client.post("/sleep", json={"ms": 5})
    assert r.status_code == 200 and r.json()["slept_ms"] == 5
    # routes and tz
    r = client.get("/routes")
    assert r.status_code == 200 and "routes" in r.json()
    r = client.get("/tz")
    assert r.status_code == 200 and "iso" in r.json()
    r = client.get("/weekday")
    assert r.status_code == 200 and "weekday" in r.json()
    # json echo
    r = client.post("/json/echo", json={"a": 1})
    assert r.status_code == 200 and r.json()["json"]["a"] == 1
    # math
    assert client.post("/math/add", json={"a": 2, "b": 3}).json()["result"] == 5.0
    assert client.post("/math/mul", json={"a": 2, "b": 3}).json()["result"] == 6.0
    assert client.post("/math/sub", json={"a": 5, "b": 3}).json()["result"] == 2.0
    assert client.post("/math/div", json={"a": 6, "b": 3}).json()["result"] == 2.0
    # text helpers
    assert client.post("/palindrome", json={"text": "Level"}).json()["is_palindrome"] is True
    assert client.post("/length", json={"text": "abc"}).json()["length"] == 3
    assert client.post("/trim", json={"text": "  hi  "}).json()["text"] == "hi"
    # string helpers
    assert client.post("/string/count", json={"text": "banana", "substr": "na"}).json()["count"] == 2
    assert client.post("/string/slug", json={"text": "Hello, World!"}).json()["slug"] == "hello-world"
    # echo/query
    assert client.get("/echo/query", params={"message": "yo"}).json()["message"] == "yo"
    # now/env/all/headers/plain
    assert client.get("/now").status_code == 200
    assert client.get("/env/all").status_code == 200
    rp = client.get("/headers/plain", headers={"X-Demo": "ok"})
    assert rp.status_code == 200 and "X-Demo: ok" in rp.text
    # datetime, uuids, randfloat, GET uppercase, routes filter
    r = client.get("/datetime")
    assert r.status_code == 200 and "epoch_ms" in r.json()
    r = client.get("/uuids", params={"count": 3})
    assert r.status_code == 200 and len(r.json().get("uuids", [])) == 3
    r = client.get("/randfloat", params={"min": 0.1, "max": 0.2})
    assert r.status_code == 200 and 0.1 <= r.json()["value"] <= 0.2
    r = client.get("/uppercase", params={"text": "abc"})
    assert r.status_code == 200 and r.json()["text"] == "ABC"
    r = client.get("/routes", params={"prefix": "/health"})
    assert r.status_code == 200 and "routes" in r.json()
    # error endpoint
    r = client.get("/error")
    assert r.status_code == 500

