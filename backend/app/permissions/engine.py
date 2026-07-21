"""Permission engine — the spec's key differentiator. This is a hard gate
in front of every action and every promise the AI makes; the LLM's
proposed action is never trusted directly for compliance-sensitive
decisions (payments, passwords, IDs, contracts). A deny rule always wins
over an allow rule for the same action.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PermissionRule


@dataclass
class PermissionDecision:
    action: str
    allowed: bool
    reason: str


async def check(db: AsyncSession, user_id: uuid.UUID, action: str) -> PermissionDecision:
    result = await db.execute(
        select(PermissionRule).where(PermissionRule.user_id == user_id, PermissionRule.action == action)
    )
    rules = result.scalars().all()

    if any(rule.effect == "deny" for rule in rules):
        return PermissionDecision(action=action, allowed=False, reason=f"user rule denies '{action}'")
    if any(rule.effect == "allow" for rule in rules):
        return PermissionDecision(action=action, allowed=True, reason=f"user rule allows '{action}'")
    return PermissionDecision(action=action, allowed=False, reason=f"no rule for '{action}', default deny")
