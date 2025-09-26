from fastapi import FastAPI
from .routes import chatops, change

app = FastAPI(title="DriftHawk Ops Bot")
app.include_router(chatops.router, prefix="/chatops")
app.include_router(change.router, prefix="/change")


