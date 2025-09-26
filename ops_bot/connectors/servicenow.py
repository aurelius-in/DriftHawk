from __future__ import annotations
from typing import Optional, Dict
import httpx
from ..app.settings import settings


def mirror_change(key: str, summary: str) -> Dict[str, str]:
  if not settings.snow_instance or not settings.snow_user or not settings.snow_token:
    return {"snow": "CHG0001"}
  try:
    url = f"https://{settings.snow_instance}.service-now.com/api/now/table/change_request"
    payload = {"short_description": f"Mirror {key}: {summary}"}
    with httpx.Client(timeout=10, auth=(settings.snow_user, settings.snow_token)) as client:
      resp = client.post(url, json=payload)
      if resp.status_code // 100 == 2:
        sys_id = resp.json().get("result", {}).get("number", "CHG0001")
        return {"snow": sys_id}
  except Exception:
    pass
  return {"snow": "CHG0001"}


