"""
Handlers for the /outputs endpoint
"""

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from ..utils.workers import run_in_process

router = APIRouter()


class CopyRequest(BaseModel):
    feedstock: str
    outputs: dict[str, str]
    channel: str
    git_sha: str | None = None
    hash_type: str = "md5"
    provider: str | None = None
    comment_on_error: bool | None = None


def _do_copy_legacy_wrapper(feedstock, outputs, channel, git_sha):
    pass


@router.post("/feedstock-outputs/copy", deprecated=True)
@router.post("/outputs/copy")
async def copy_output(req: CopyRequest, background_tasks: BackgroundTasks):
    _ = await run_in_process(
        _do_copy_legacy_wrapper, req.feedstock, req.outputs, req.channel, req.git_sha
    )

    raise NotImplementedError


@router.post("/feedstock-outputs/validate", deprecated=True)
@router.post("/outputs/validate")
async def validate_output():
    raise NotImplementedError
