from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import RoomResponse, RoomRequest
from backend.crud.room import (
    get_rooms, 
    get_room_by_id, 
    create_room, 
    update_room, 
    delete_room
)

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)

@router.get(
    "/",
    response_model=list[RoomResponse],     
)
def read_rooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """会議室一覧を取得する"""
    return get_rooms(db, skip=skip, limit=limit)

@router.get(
    "/{room_id}",
    response_model=RoomResponse,
)
def read_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    """IDで会議室を1件取得"""
    room = get_room_by_id(
        db,
        room_id,
    )
    if room is None:
        raise HTTPException(status_code=404, detail="会議室情報が見つかりません",)
    return room

@router.post(
    "/", 
    response_model=RoomResponse, 
    status_code=201
)
def create_room_endpoint(
    room: RoomRequest,
    db: Session = Depends(get_db),
):
    """会議室を作成する"""
    return create_room(
        db,
        room,

    )

@router.put(
    "/{room_id}",
    response_model=RoomResponse,
)
def update_room_endpoint(
    room_id: int,
    room: RoomRequest,
    db: Session = Depends(get_db),
):
    """会議室を更新する"""
    room_update = update_room(
        db,
        room_id,
        room,
    )
    if room_update is None:
        raise HTTPException(status_code=404, detail="会議室情報が見つかりません",)
    return room_update

@router.delete(
    "/{room_id}",
    status_code=204,
)
def delete_room_endpoint(
    room_id: int,
    db: Session = Depends(get_db),
):
    """会議室を削除する"""
    room_delete = delete_room(
        db,
        room_id,
    )
    if not room_delete:
        raise HTTPException(
            status_code=404,
            detail="会議室情報が見つかりません",
        )
    return
    



