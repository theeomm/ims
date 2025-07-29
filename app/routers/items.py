from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.db.db import DbSession
from app.dependencies import templates


router = APIRouter(prefix="/items", default_response_class=HTMLResponse)


# Get all items
@router.get("/", name="items:details")
async def get_item(request: Request, db: DbSession):
    context = {"request": request}
    return templates.TemplateResponse("items/index.html", context)


@router.get("/", name="items:list")
async def get_items(request: Request, db: DbSession):
    context = {"request": request}
    return templates.TemplateResponse("items/index.html", context)
