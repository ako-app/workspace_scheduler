from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.crud.room import (
    create_room,
    delete_room,
    get_room_by_id,
    get_rooms,
    update_room,
)
from backend.database import get_db
from backend.models.user import User
from backend.schemas import RoomRequest, RoomResponse

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.get(
    "/",
    response_model=list[RoomResponse],
)
def read_rooms(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """会議室一覧を取得する"""
    return get_rooms(db, skip=skip, limit=limit)


@router.get(
    "/{room_id}",
    response_model=RoomResponse,
)
def read_room(
    room_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    """IDで会議室を1件取得"""
    room = get_room_by_id(
        db,
        room_id,
    )
    if room is None:
        raise HTTPException(
            status_code=404,
            detail="会議室情報が見つかりません",
        )
    return room


@router.post("/", response_model=RoomResponse, status_code=201)
def create_room_endpoint(
    room: RoomRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """会議室を作成する"""
    return create_room(
        db,
        room,
        manager_id=current_user.id,
    )


@router.put(
    "/{room_id}",
    response_model=RoomResponse,
)
def update_room_endpoint(
    room_id: int,
    room: RoomRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """会議室を更新する(管理者本人のみ)"""
    db_room = get_room_by_id(db, room_id)

    if db_room is None:
        raise HTTPException(
            status_code=404,
            detail="会議室情報が見つかりません",
        )
    if db_room.manager_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="この操作を行う権限がありません",
        )

    room_update = update_room(
        db,
        room_id,
        room,
    )
    return room_update


@router.delete(
    "/{room_id}",
    status_code=204,
    response_model=None,
)
def delete_room_endpoint(
    room_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """会議室を削除する(本人のみ)"""
    db_room = get_room_by_id(db, room_id)
    if db_room is None:
        raise HTTPException(
            status_code=404,
            detail="会議室情報が見つかりません",
        )
    if db_room.manager_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="この操作を行う権限がありません",
        )
    if db_room.bookings:
        raise HTTPException(
            status_code=409,
            detail="この会議室には予約が存在するため削除できません",
        )
    room_delete = delete_room(
        db,
        room_id,
    )
    if not room_delete:
        raise HTTPException(
            status_code=404,
            detail="会議室情報が見つかりません",
        )
