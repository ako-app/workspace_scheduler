from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.room import Room
from backend.schemas.room import RoomRequest


def get_rooms(
        db: Session, 
        skip: int = 0,
        limit: int = 100,
) -> list[Room]:
    """会議室一覧を取得する"""
    stmt = (
        select(Room)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(stmt).all()

def get_room(
        db: Session,
        room_id: int,     
) -> Room | None:
    """会議室詳細を取得する"""
    stmt = select(Room).where(
        Room.id == room_id
    )

    return db.scalar(stmt)

def create_room(
        db: Session,
        room: RoomRequest,
       
) -> Room:  
    """会議室登録"""
    db_room = Room(
        room_name = room.room_name,
        capacity = room.capacity,
        # TODO: JWT認証実装後に current_user.id を設定
     )
    
    db.add(db_room)

    db.commit()

    db.refresh(db_room)

    return db_room
