"""
Handlers for the /alive endpoint
"""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Status(BaseModel):
    status: Literal["operational"] = "operational"


@router.get("/alive")
async def alive() -> Status:
    """
    Heartbeat endpoint to check whether server is running.
    """
    return Status()
