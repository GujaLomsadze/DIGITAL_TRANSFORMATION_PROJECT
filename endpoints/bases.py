from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/")
def homepage():
    return RedirectResponse(url="/docs")
