import os

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
import time
import socket
import hashlib
import base64
import random
from datetime import datetime, timezone
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .middleware.request_id import RequestIdMiddleware
from .middleware.timing import TimingMiddleware
from .routes import chatops, change
from .middleware.security import SecurityHeadersMiddleware
from .middleware.trace import TraceMiddleware
from .utils.logging import get_logger

app = FastAPI(
    title="DriftHawk Ops Bot",
    version=os.getenv("APP_VERSION", "0.1.0"),
    contact={"name": "DriftHawk", "url": "https://github.com/aurelius-in/DriftHawk"},
)
logger = get_logger(__name__)
request_counter = Counter("ops_bot_requests_total", "Total HTTP requests", ["path", "method", "status"])
START_TIME = time.time()

origins = os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Request-Duration-ms"],
)
allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
app.add_middleware(GZipMiddleware, minimum_size=500)

app.include_router(chatops.router, prefix="/chatops")
app.include_router(change.router, prefix="/change")
app.add_middleware(RequestIdMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(TraceMiddleware)


@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "git_sha": os.getenv("GIT_SHA", "unknown"),
        "started_at": int(START_TIME),
        "uptime_seconds": int(time.time() - START_TIME),
    }


@app.get("/livez")
def livez():
    return {"live": True}


@app.get("/readyz")
def readyz():
    return {"ready": True}


@app.get("/alive")
def alive():
    return {"live": True}


@app.head("/alive")
def alive_head():
    return Response(status_code=200)


@app.get("/ready")
def ready():
    return {"ready": True}


@app.head("/ready")
def ready_head():
    return Response(status_code=200)


@app.get("/version")
def version():
    return {"git_sha": os.getenv("GIT_SHA", "unknown")}


@app.get("/")
def root():
    return {
        "service": "DriftHawk Ops Bot",
        "endpoints": ["/chatops", "/change", "/healthz", "/livez", "/readyz", "/version"],
    }


@app.get("/ping")
def ping():
    return {"pong": True}


@app.head("/ping")
def ping_head():
    return Response(status_code=200)


@app.get("/info")
def info():
    return {
        "service": "DriftHawk Ops Bot",
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "git_sha": os.getenv("GIT_SHA", "unknown"),
        "startup_time": int(START_TIME),
    }


@app.get("/statusz")
def statusz():
    return {
        "status": "ok",
        "uptime_seconds": int(time.time() - START_TIME),
        "live": True,
        "ready": True,
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "git_sha": os.getenv("GIT_SHA", "unknown"),
    }


@app.get("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow: /\n", media_type="text/plain; charset=utf-8")


@app.get("/env")
def env():
    return {
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "allowed_hosts": os.getenv("ALLOWED_HOSTS", "*").split(","),
    }


@app.get("/config")
def config():
    return {
        "cors_allowed_origins": origins,
        "expose_headers": ["X-Request-ID", "X-Request-Duration-ms"],
    }


@app.get("/uptime")
def uptime():
    return {"uptime_seconds": int(time.time() - START_TIME)}


@app.head("/healthz")
def healthz_head():
    return Response(status_code=200)


@app.head("/readyz")
def readyz_head():
    return Response(status_code=200)


from pydantic import BaseModel  # noqa: E402
import secrets as _secrets  # noqa: E402
import uuid as _uuid  # noqa: E402


class EchoBody(BaseModel):  # noqa: E402
    message: str


@app.post("/echo")
def echo(body: EchoBody):
    return {"echo": body.message}


@app.get("/time")
def current_time():
    return {"epoch": int(time.time())}


@app.get("/whoami")
def whoami(request: Request):
    client_ip = request.client.host if request.client else "-"
    return {"ip": client_ip}


@app.get("/uuid")
def uuid_v4():
    return {"uuid": str(_uuid.uuid4())}


@app.get("/random")
def random_token(length: int = 16):
    if length < 1 or length > 128:
        # triggers RequestValidationError fallback via manual raise
        raise StarletteHTTPException(status_code=422, detail="length must be between 1 and 128")
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    token = "".join(_secrets.choice(alphabet) for _ in range(length))
    return {"length": length, "token": token}


@app.get("/hostname")
def hostname():
    return {"hostname": socket.gethostname()}


@app.get("/env/{key}")
def env_key(key: str):
    val = os.getenv(key)
    return {"key": key, "value": val}


class SumBody(BaseModel):  # noqa: E402
    numbers: list[float]


@app.post("/sum")
def sum_numbers(body: SumBody):
    total = float(sum(body.numbers[:100]))
    return {"sum": total}


class HashBody(BaseModel):  # noqa: E402
    text: str
    algorithm: str | None = "sha256"


@app.post("/hash")
def hash_text(body: HashBody):
    algo = (body.algorithm or "sha256").lower()
    if algo not in {"sha256", "sha1", "md5"}:
        raise StarletteHTTPException(status_code=422, detail="unsupported algorithm")
    h = hashlib.new(algo)
    h.update(body.text.encode("utf-8"))
    return {"algorithm": algo, "hex": h.hexdigest()}


class TextBody(BaseModel):  # noqa: E402
    text: str


@app.post("/uppercase")
def uppercase(body: TextBody):
    return {"text": body.text.upper()}


@app.post("/lowercase")
def lowercase(body: TextBody):
    return {"text": body.text.lower()}


@app.post("/reverse")
def reverse(body: TextBody):
    return {"text": body.text[::-1]}


class B64Body(BaseModel):  # noqa: E402
    text: str
    mode: str = "encode"


@app.post("/b64")
def b64(body: B64Body):
    if body.mode not in {"encode", "decode"}:
        raise StarletteHTTPException(status_code=422, detail="mode must be encode or decode")
    if body.mode == "encode":
        out = base64.b64encode(body.text.encode("utf-8")).decode("ascii")
    else:
        try:
            out = base64.b64decode(body.text).decode("utf-8")
        except Exception:
            raise StarletteHTTPException(status_code=422, detail="invalid base64 input")
    return {"result": out}


@app.get("/randint")
def randint_route(min: int = 0, max: int = 10):  # noqa: A002 - param name
    if min > max:
        raise StarletteHTTPException(status_code=422, detail="min must be <= max")
    return {"value": random.randint(min, max)}


class SleepBody(BaseModel):  # noqa: E402
    ms: int = 0


@app.post("/sleep")
def sleep_route(body: SleepBody):
    ms = max(0, min(100, body.ms))
    if ms:
        time.sleep(ms / 1000.0)
    return {"slept_ms": ms}


@app.get("/routes")
def routes():
    items: list[dict[str, str]] = []
    for r in app.router.routes:
        path = getattr(r, "path", "")
        methods = ",".join(sorted(getattr(r, "methods", set())))
        if path:
            items.append({"path": path, "methods": methods})
    return {"routes": items}


@app.get("/tz")
def tz():
    now = datetime.now(timezone.utc)
    return {"epoch": int(now.timestamp()), "iso": now.isoformat()}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse({"error": "not_found", "path": request.url.path}, status_code=404)
    if exc.status_code == 405:
        return JSONResponse({"error": "method_not_allowed", "path": request.url.path}, status_code=405)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


from fastapi.exceptions import RequestValidationError  # noqa: E402


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse({"error": "validation_error", "details": exc.errors()}, status_code=422)


@app.get("/request-id")
def request_id_endpoint(request: Request):
    return {"request_id": getattr(request.state, "request_id", "-")}


@app.get("/flags")
def flags():
    return {
        "enable_metrics": True,
        "enable_slack": bool(os.getenv("SLACK_WEBHOOK_URL")),
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/headers")
def headers(request: Request):
    def header_title_case(name: str) -> str:
        parts = name.split("-")
        return "-".join(p[:1].upper() + p[1:].lower() for p in parts if p)

    sanitized: dict[str, str] = {}
    for k, v in request.headers.items():
        lk = k.lower()
        if "authorization" in lk or "cookie" in lk:
            continue
        sanitized[header_title_case(lk)] = v
    return {"headers": sanitized}


@app.middleware("http")
async def count_requests_mw(request: Request, call_next):
    response = await call_next(request)
    try:
        request_counter.labels(path=request.url.path, method=request.method, status=str(response.status_code)).inc()
    except Exception:
        pass
    return response


@app.on_event("startup")
async def on_startup():
    logger.info("app_startup version=%s git_sha=%s", os.getenv("APP_VERSION", "0.1.0"), os.getenv("GIT_SHA", "unknown"))


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("app_shutdown")


@app.exception_handler(Exception)
async def handle_exceptions(request: Request, exc: Exception):
    logger.error(
        "unhandled_exception request_id=%s path=%s err=%s",
        getattr(request.state, "request_id", "-"),
        request.url.path,
        repr(exc),
    )
    return Response(content="Internal Server Error", status_code=500)
