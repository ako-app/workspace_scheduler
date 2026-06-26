from fastapi import FastAPI
from backend.routers import user, room, booking

app = FastAPI(
    title="会議室予約システムAPI",
    description="会議室の予約を管理することにより、管理業務を効率化するためのREST API",
    version="1.0.0",
)
# ルートエンドポイント
@app.get(
    "/",
    tags=["Root"]
)
def read_root():
    """APIのエンドポイント"""
    return {
        "message": "会議室予約システムにようこそ",
        "version": "1.0.0",
        "docs" : "/docs",
        "redoc" : "/redoc",
         }
# Router
app.include_router(user.router)
app.include_router(room.router)
app.include_router(booking.router)

