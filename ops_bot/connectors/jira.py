from __future__ import annotations
import base64
from typing import Optional
import httpx
from ops_bot.app.settings import settings


def _auth_header(user: Optional[str], token: Optional[str]) -> dict[str, str]:
    if not user or not token:
        return {}
    b = base64.b64encode(f"{user}:{token}".encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {b}"}


def create_change(summary: str, description: str, risk: float, plan_url: Optional[str]) -> str:
    if not settings.jira_base or not settings.jira_user or not settings.jira_token:
        return "CHG-123"
    try:
        url = settings.jira_base.rstrip("/") + "/rest/api/3/issue"
        payload = {
            "fields": {
                "project": {"key": "CHG"},
                "summary": summary,
                "issuetype": {"name": "Change"},
                "description": f"{description}\nRisk: {risk}\nPlan: {plan_url or ''}",
            }
        }
        headers = {"Content-Type": "application/json", **_auth_header(settings.jira_user, settings.jira_token)}
        with httpx.Client(timeout=10) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code // 100 == 2:
                key = resp.json().get("key")
                if isinstance(key, str) and key:
                    return key
    except Exception:
        pass
    return "CHG-123"


