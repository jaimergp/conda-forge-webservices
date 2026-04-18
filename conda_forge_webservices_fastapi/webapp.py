"""
The FastAPI app powering the conda-forge-webservices deployment.

This module only initializes the app and defines what happens with the
root endpoint. All other routes are defined in the .routers module
and registered here.

To run the app, use `python -m conda_forge_webservices_fastapi`,
or simply `fastapi run conda_forge_webservices/webapp.py`.
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse

from .routers import (
    alive,
    autotickbot,
    commands,
    feedstocks,
    linter,
    outputs,
    staged_recipes,
    status_monitor,
    teams,
    version,
)
from .utils.workers import init_pools, shutdown_pools


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pools()
    yield
    shutdown_pools()


def _is_dev() -> bool:
    """
    Check whether we are in local development mode.

    Only valid for `fastapi dev ...`.
    """
    return Path(sys.argv[0]).name == "fastapi" and sys.argv[1] == "dev"


app = FastAPI(
    title="conda-forge webservices",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs" if _is_dev() else None,  # disable online help in production
    redoc_url="/redoc" if _is_dev() else None,  # disable online help in production
)


@app.exception_handler(NotImplementedError)
async def not_implemented_handler(request: Request, exc: NotImplementedError):
    """
    Catches NotImplementedError and turns them into a 405 response while we
    are porting endpoints from Tornado.
    """
    return JSONResponse(
        status_code=405,
        content={
            "error": exc.__class__.__name__,
            "message": f"Endpoint '{request.url.path}' is not implemented yet.",
        },
    )


@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("https://conda-forge.org")


# These are all the API routes we offer
# Each module in .routers represents a path component
app.include_router(alive.router)
app.include_router(autotickbot.router)
app.include_router(commands.router)
app.include_router(feedstocks.router)
app.include_router(linter.router)
app.include_router(outputs.router)
app.include_router(staged_recipes.router)
app.include_router(status_monitor.router)
app.include_router(teams.router)
app.include_router(version.router)
