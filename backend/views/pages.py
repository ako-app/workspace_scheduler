from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

view_router = APIRouter()

templates = Jinja2Templates(
    directory="frontend/templates",
)

# Jinja2テンプレートを使ってHTML画面を表示
@view_router.get("/register", include_in_schema=False)
def show_register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )