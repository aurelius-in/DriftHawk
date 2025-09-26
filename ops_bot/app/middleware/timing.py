import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Request
from ..utils.logging import get_logger


class TimingMiddleware(BaseHTTPMiddleware):
  def __init__(self, app: ASGIApp):
    super().__init__(app)
    self.logger = get_logger(__name__)

  async def dispatch(self, request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    req_id = getattr(request.state, "request_id", "-")
    client_ip = request.client.host if request.client else "-"
    self.logger.info("request_id=%s client_ip=%s duration_ms=%s", req_id, client_ip, duration_ms)
    return response


