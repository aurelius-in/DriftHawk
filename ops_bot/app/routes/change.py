from fastapi import APIRouter
from pydantic import BaseModel
from ..connectors import jira, servicenow

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
  servicenow.mirror_change(key, req.summary)
  return {"status": "pending_approval", "change": key}


