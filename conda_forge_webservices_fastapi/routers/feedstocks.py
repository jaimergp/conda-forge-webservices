"""
Handlers for the /feedstocks endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/conda-forge-feedstocks/org-hook", deprecated=True)
@router.post("/feedstocks/hook")
async def hook():
    raise NotImplementedError
