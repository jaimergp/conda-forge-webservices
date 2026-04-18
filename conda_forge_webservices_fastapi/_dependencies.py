"""
Used by the routers._webhooks example for the "Depends" args in the router.
"""

import hashlib
import hmac
import os

import httpx
from fastapi import Header, HTTPException, Request
from gidgethub.httpx import GitHubAPI


async def verify_github_signature(
    request: Request, x_hub_signature: str = Header(None)
):
    if not x_hub_signature:
        raise HTTPException(status_code=403, detail="Missing signature")

    body = await request.body()
    secret = os.environ.get("CF_WEBSERVICES_TOKEN", "").encode("utf-8")

    our_hash = hmac.new(secret, body, hashlib.sha1).hexdigest()
    their_hash = x_hub_signature.split("=")[-1]

    if not hmac.compare_digest(our_hash, their_hash):
        raise HTTPException(status_code=403, detail="Invalid signature")

    return body


async def get_github_client() -> GitHubAPI:
    token = os.environ.get("GH_TOKEN", "")
    async with httpx.AsyncClient() as client:
        return GitHubAPI(client, "conda-forge-webservices", oauth_token=token)
