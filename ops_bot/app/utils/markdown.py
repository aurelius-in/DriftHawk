from __future__ import annotations

from typing import Any, Dict


def impact_brief_markdown(summary: Dict[str, Any]) -> str:
    risk = summary.get("risk", 0.0)
    risk_level = summary.get("risk_level", "low")
    adds = summary.get("adds", 0)
    updates = summary.get("updates", 0)
    destroys = summary.get("destroys", 0)
    total = summary.get("total_changes", adds + updates + destroys)
    lines = [
        "## Impact Brief",
        f"- Changes: {total} (add: {adds}, update: {updates}, destroy: {destroys})",
        f"- Risk: {risk} ({risk_level})",
    ]
    return "\n".join(lines)


