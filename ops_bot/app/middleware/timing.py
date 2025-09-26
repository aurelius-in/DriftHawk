import time
from prometheus_client import Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Request
from ..utils.logging import get_logger


class TimingMiddleware(BaseHTTPMiddleware):
  def __init__(self, app: ASGIApp):
    super().__init__(app)
    self.logger = get_logger(__name__)
    self.duration_histogram = Histogram(
      "ops_bot_request_duration_ms",
      "HTTP request duration in milliseconds",
      ["path", "method", "status"],
      buckets=[1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000]
    )

  async def dispatch(self, request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    req_id = getattr(request.state, "request_id", "-")
    client_ip = request.client.host if request.client else "-"
    try:
      self.duration_histogram.labels(request.url.path, request.method, str(response.status_code)).observe(duration_ms)
    except Exception:
      pass
    self.logger.info("request_id=%s client_ip=%s duration_ms=%s", req_id, client_ip, duration_ms)
    return response


