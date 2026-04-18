"""
Example on how to use gidgethub's Router for a cleaner webhook event dispatching
within the same endpoint route. We reuse this pattern in endpoints that
are receiving Github webhook payloads.
"""

import logging

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from gidgethub import routing, sansio
from gidgethub.httpx import GitHubAPI

from conda_forge_webservices import commands

from .._dependencies import get_github_client, verify_github_signature

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(verify_github_signature)])
gh_router = routing.Router()


@gh_router.register("pull_request", action="opened")
@gh_router.register("pull_request", action="synchronize")
async def handle_linting_and_automerge(
    event: sansio.Event, gh: GitHubAPI, *args, **kwargs
):
    repo_name = event.data["repository"]["name"]
    owner = event.data["repository"]["owner"]["login"]
    pr_id = event.data["pull_request"]["number"]

    if owner != "conda-forge" or not (
        repo_name == "staged-recipes" or repo_name.endswith("-feedstock")
    ):
        return

    logger.info(f"Would dispatch linting for {owner}/{repo_name}#{pr_id}")


@gh_router.register("issue_comment", action="created")
async def handle_commands(
    event: sansio.Event,
    gh: GitHubAPI,
    background_tasks: BackgroundTasks,
    *args,
    **kwargs,
):
    repo_name = event.data["repository"]["name"]
    owner = event.data["repository"]["owner"]["login"]
    comment = event.data["comment"]["body"]
    issue_num = event.data["issue"]["number"]

    background_tasks.add_task(
        commands.issue_comment,
        owner,
        repo_name,
        issue_num,
        "",
        comment,
        event.data["comment"]["id"],
    )


@router.post("/org-hook")
async def github_webhook_receiver(
    request: Request,
    background_tasks: BackgroundTasks,
    body: bytes = Depends(verify_github_signature),
    gh: GitHubAPI = Depends(get_github_client),
):
    event = sansio.Event(
        request.headers.get("X-GitHub-Event", "ping"),
        request.headers.get("X-GitHub-Delivery", ""),
        body,
    )

    if event.event == "ping":
        return "pong"

    await gh_router.dispatch(event, gh, background_tasks=background_tasks)
    return {"status": "ok"}
