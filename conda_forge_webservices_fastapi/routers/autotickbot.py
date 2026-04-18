"""
Handlers for the /autotickbot endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/autotickbot/payload", deprecated=True)
@router.post("/autotickbot/hook")
async def hook():
    raise NotImplementedError
