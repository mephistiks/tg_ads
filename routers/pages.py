from pathlib import Path

from fastapi import APIRouter, Request, status, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter()


templates = Jinja2Templates(directory="templates")

@router.get("/")
async def index():
    return Response("ok", status_code = status.HTTP_200_OK)

@router.get("/create")
async def create_page(request: Request):
    return templates.TemplateResponse(
        "create_post.html", {"request": request}
    )


