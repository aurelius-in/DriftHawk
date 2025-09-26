from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chatops, change

app = FastAPI(title="DriftHawk Ops Bot")

# CORS
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


