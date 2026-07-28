from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

view_router = APIRouter()

templates = Jinja2Templates(
    directory="frontend/templates",
)
# TOPページを表示
@view_router.get("/", include_in_schema=False)
def show_top_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )

# ユーザー登録画面を表示
@view_router.get("/register", include_in_schema=False)
def show_register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={},
    )

# ログイン画面を表示
@view_router.get("/login", include_in_schema=False)
def show_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )
# Room画面を表示
@view_router.get("/room", include_in_schema=False)
def show_room_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="room.html",
        context={},
    )
# 会議室登録画面を表示
@view_router.get("/room/new", include_in_schema=False)
def show_room_registration_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="room-registration.html",
        context={},
    )
# 会議室編集画面を表示
@view_router.get("/room/{room_id}/edit", include_in_schema=False)
def show_room_edit_page(
    request: Request,
    room_id: int,
    ):
    return templates.TemplateResponse(
        request=request,
        name="room-edit.html",
        context={"room_id": room_id}
    )