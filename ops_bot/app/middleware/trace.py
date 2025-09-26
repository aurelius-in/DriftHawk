from __future__ import annotations

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Request


class TraceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        trace_id = getattr(request.state, "request_id", None) or str(uuid.uuid4())
        try:
            request.state.trace_id = trace_id
        except Exception:
            pass
        response = await call_next(request)
        response.headers.setdefault("X-Trace-Id", trace_id)
        return response


