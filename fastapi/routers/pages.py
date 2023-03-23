from fastapi import APIRouter, Request, Response
from starlette import status
from starlette.templating import Jinja2Templates


router = APIRouter()


templates = Jinja2Templates(directory="templates")

@router.get("/")
@router.get("/create")
async def create_page(request: Request):
    return templates.TemplateResponse(
        "create_post.html", {"request": request}
    )

@router.get("/list")
async def create_page(request: Request):
    return templates.TemplateResponse(
        "list_posts.html", {"request": request}
    )

@router.get("/calendar/{_id}/")
async def create_page(request: Request, _id: str):
    #print(_id)
    return templates.TemplateResponse(
        "post_timetable.html", {"request": request, "_id":_id}
    )
