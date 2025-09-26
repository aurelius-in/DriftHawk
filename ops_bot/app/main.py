from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from .routes import chatops, change
from .utils.logging import get_logger

app = FastAPI(title="DriftHawk Ops Bot")
logger = get_logger(__name__)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(chatops.router, prefix="/chatops")
app.include_router(change.router, prefix="/change")


@app.get("/healthz")
def healthz():
  return {"status": "ok"}


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


