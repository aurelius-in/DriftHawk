from fastapi import APIRouter
from pydantic import BaseModel
from ..connectors import jira, servicenow, slack
from ..settings import settings

router = APIRouter()


class ChangeRequest(BaseModel):
  env: str
  summary: str
  description: str
  risk_score: float = 0.2
  plan_url: str | None = None
  approvers: list[str] = []


@router.post("/submit")
def submit(req: ChangeRequest):
  key = jira.create_change(req.summary, req.description, req.risk_score, req.plan_url)
  snow = servicenow.mirror_change(key, req.summary)
  links = {}
  if settings.jira_base:
    links["jira"] = settings.jira_base.rstrip("/") + "/browse/" + key
  if snow.get("snow"):
    links["servicenow"] = snow["snow"]
  slack.post_message(f"Change submitted: {key} — {req.summary}")
  return {"status": "pending_approval", "change": key, "links": links}


