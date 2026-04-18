"""
Handlers for the /linter endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/conda-linting/org-hook", deprecated=True)
@router.post("/linter/hook")
async def hook():
    raise NotImplementedError
