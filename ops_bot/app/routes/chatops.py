from fastapi import APIRouter
from pydantic import BaseModel
from ops_bot.connectors import slack
from ..utils.plan import load_plan, summarize_plan

router = APIRouter()


class PlanBriefReq(BaseModel):
  env: str = "dev"
  plan_url: str | None = None


@router.post("/plan-brief")
def plan_brief(req: PlanBriefReq):
  brief = {"impact": "low", "blast_radius": "ipam->lb->proxy", "cost_delta": "$12/mo", "risk": 0.12}
  try:
    plan = load_plan("artifacts/plan.json")
    s = summarize_plan(plan)
    brief |= {"risk": s["risk"], "total_changes": s["total_changes"], "adds": s["adds"], "updates": s["updates"], "destroys": s["destroys"]}
  except Exception:
    pass
  return brief


class PromoteReq(BaseModel):
  env: str
  rollout: str | None = None


@router.post("/promote")
def promote(req: PromoteReq):
  slack.post_message(f"Starting promotion to {req.env}")
  return {"status": "started", "env": req.env, "rollout_id": "rl-123"}


@router.get("/status/{rid}")
def status(rid: str):
  return {"rollout_id": rid, "health": "healthy", "rollback": "available"}


