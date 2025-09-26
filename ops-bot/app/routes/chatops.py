from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class PlanBriefReq(BaseModel):
  env: str = "dev"
  plan_url: str | None = None


@router.post("/plan-brief")
def plan_brief(req: PlanBriefReq):
  return {"impact": "low", "blast_radius": "ipam->lb->proxy", "cost_delta": "$12/mo", "risk": 0.12}


class PromoteReq(BaseModel):
  env: str
  rollout: str | None = None


@router.post("/promote")
def promote(req: PromoteReq):
  return {"status": "started", "env": req.env, "rollout_id": "rl-123"}


@router.get("/status/{rid}")
def status(rid: str):
  return {"rollout_id": rid, "health": "healthy", "rollback": "available"}


