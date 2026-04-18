"""
Handlers for the /status-monitor endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/status-monitor")
async def get_status_monitor():
    raise NotImplementedError


@router.get("/status-monitor/azure")
async def azure():
    raise NotImplementedError


@router.get("/status-monitor/db")
async def db():
    raise NotImplementedError


@router.get("/status-monitor/docker")
async def docker():
    raise NotImplementedError


@router.get("/status-monitor/payload")
async def payload():
    raise NotImplementedError


@router.get("/status-monitor/report/{name}")
async def report(name: str):
    raise NotImplementedError
