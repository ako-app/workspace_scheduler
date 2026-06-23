from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.room import Room
#from backend.schemas.user import UserRequest, UserResponse


def get_rooms(
        db: Session, 
        skip: int = 0,
        limit: int = 100,
) ->list[Room]:
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
