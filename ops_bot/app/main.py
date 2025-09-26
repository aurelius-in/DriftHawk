import os

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .middleware.request_id import RequestIdMiddleware
from .middleware.timing import TimingMiddleware
from .routes import chatops, change
from .utils.logging import get_logger

app = FastAPI(
  title="DriftHawk Ops Bot",
  version=os.getenv("APP_VERSION", "0.1.0"),
  contact={"name": "DriftHawk", "url": "https://github.com/aurelius-in/DriftHawk"},
)
logger = get_logger(__name__)
request_counter = Counter("ops_bot_requests_total", "Total HTTP requests", ["path", "method", "status"])

origins = os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
app.add_middleware(GZipMiddleware, minimum_size=500)

app.include_router(chatops.router, prefix="/chatops")
app.include_router(change.router, prefix="/change")
app.add_middleware(RequestIdMiddleware)
app.add_middleware(TimingMiddleware)


@app.get("/healthz")
def healthz():
  return {"status": "ok", "version": os.getenv("APP_VERSION", "0.1.0"), "git_sha": os.getenv("GIT_SHA", "unknown")}


@app.get("/livez")
def livez():
  return {"live": True}


@app.get("/readyz")
def readyz():
  return {"ready": True}


@app.get("/version")
def version():
  return {"git_sha": os.getenv("GIT_SHA", "unknown")}


@app.get("/")
def root():
  return {"service": "DriftHawk Ops Bot", "endpoints": ["/chatops", "/change", "/healthz", "/livez", "/readyz", "/version"]}


@app.get("/ping")
def ping():
  return {"pong": True}


@app.get("/metrics")
def metrics():
  return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/headers")
def headers(request: Request):
  sanitized = {}
  for k, v in request.headers.items():
    lk = k.lower()
    if "authorization" in lk or "cookie" in lk:
      continue
    sanitized[k] = v
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
  logger.error("unhandled_exception request_id=%s path=%s err=%s", getattr(request.state, "request_id", "-"), request.url.path, repr(exc))
  return Response(content="Internal Server Error", status_code=500)


