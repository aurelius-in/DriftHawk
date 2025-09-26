from __future__ import annotations
from typing import Optional
import httpx
from ..app.settings import settings


def post_message(text: str) -> bool:
  if not settings.slack_webhook_url:
    return False
  try:
    with httpx.Client(timeout=10) as client:
      resp = client.post(settings.slack_webhook_url, json={"text": text})
      return resp.status_code // 100 == 2
  except Exception:
    return False


