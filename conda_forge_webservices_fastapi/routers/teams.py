"""
Handlers for the /teams endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/conda-forge-teams/update", deprecated=True)
@router.get("/teams/update")
async def update():
    raise NotImplementedError


@router.get("/conda-forge-teams/hook", deprecated=True)
@router.get("/teams/hook")
async def hook():
    raise NotImplementedError
