"""
Handlers for the /commands endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/conda-forge-command/org-hook", deprecated=True)
@router.post("/commands/hook")
async def hook():
    raise NotImplementedError
