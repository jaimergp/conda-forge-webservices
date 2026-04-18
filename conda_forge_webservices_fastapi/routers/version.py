"""
Handlers for the /version endpoint
"""

import sys
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()


@router.get("/conda-webservice-update/versions", deprecated=True)
@router.get("/version")
async def get_version():
    return get_package_versions("conda-smithy")


def get_package_versions(*packages: str) -> dict[str, str]:
    """
    Reports versions for all or selected packages.

    This is done by scanning {sys.prefix}/conda-meta for CEP 32
    JSON documents. Note they are not loaded; only the filenames
    are parsed to obtain the version.
    """
    prefix = Path(sys.prefix)
    if not (prefix / "conda-meta").is_dir():
        raise RuntimeError("Bad installation")

    result = {}
    for json_file in (prefix / "conda-meta").glob("*.json"):
        try:
            package, version, _ = json_file.stem.rsplit("-", 2)
        except ValueError:
            continue
        if not packages or package in packages:
            result[package] = version

    if not result:
        if packages:
            raise ValueError("Requested package(s) not installed")
        raise RuntimeError("No installed packages")

    return result
