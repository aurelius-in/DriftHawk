from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict


def load_plan(path: str | Path) -> Dict[str, Any]:
    data: Dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    return data


def summarize_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    resource_changes = plan.get("resource_changes", [])
    adds = sum(1 for r in resource_changes if r.get("change", {}).get("actions") == ["create"])
    updates = sum(1 for r in resource_changes if r.get("change", {}).get("actions") == ["update"])
    destroys = sum(1 for r in resource_changes if r.get("change", {}).get("actions") == ["delete"])
    total = len(resource_changes)
    risk = round(min(1.0, (updates * 0.05 + destroys * 0.1 + adds * 0.02)), 2)
    risk_level = "low" if risk < 0.2 else ("medium" if risk < 0.5 else "high")
    return {
        "adds": adds,
        "updates": updates,
        "destroys": destroys,
        "total_changes": total,
        "risk": risk,
        "risk_level": risk_level,
    }

