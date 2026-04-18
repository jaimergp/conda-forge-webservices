"""
Handlers for the /staged-recipes endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/staged-recipes/labeler-hook",
    deprecated=True,
    # - and / both get cleaned up as _ in the generated name,
    # causing a name clash
    generate_unique_id_function=lambda *a: "deprecated_labeler_hook",
)
@router.post("/staged-recipes/labeler/hook")
async def labeler_hook():
    raise NotImplementedError
