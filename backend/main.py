from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.routers import booking, room
from backend.routers.user import auth_router, user_router
from backend.views.pages import view_router

app = FastAPI(
    title="会議室予約システムAPI",
    description="会議室の予約を管理することにより、管理業務を効率化するためのREST API",
    version="1.0.0",
)
# # CSS・JavaScript・画像などの静的ファイルを配信
app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static",
)


# ルートエンドポイント
@app.get("/api", tags=["Root"])
def read_root():
    """APIのエンドポイント"""
    return {
        "message": "会議室予約システムにようこそ",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# APIルーターと画面表示用ルーターを登録
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(room.router)
app.include_router(booking.router)
app.include_router(view_router)
