from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import commit_or_rollback
from backend.models.room import Room
from backend.schemas.room import RoomRequest


def get_room_by_id(
    db: Session,
    room_id: int,
) -> Room | None:
    """IDで会議室を1件取得"""
    stmt = select(Room).where(Room.id == room_id)
    return db.scalar(stmt)


def get_room_by_name(
    db: Session,
    room_name: str,
) -> Room | None:
    """会議室名を1件取得"""
    stmt = select(Room).where(Room.room_name == room_name)
    return db.scalar(stmt)


def get_rooms(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Room]:
    """会議室一覧を取得する"""
    stmt = select(Room).offset(skip).limit(limit)

    return db.scalars(stmt).all()


def create_room(db: Session, room: RoomRequest, manager_id: int) -> Room:
    """会議室登録"""
    db_room = Room(
        manager_id=manager_id,
        room_name=room.room_name,
        capacity=room.capacity,
    )

    db.add(db_room)

    commit_or_rollback(db)

    db.refresh(db_room)

    return db_room


def update_room(
    db: Session,
    room_id: int,
    room: RoomRequest,
) -> Room | None:
    """会議室更新"""
    db_room = get_room_by_id(db, room_id)
    if db_room is None:
        return None

    db_room.room_name = room.room_name
    db_room.capacity = room.capacity

    commit_or_rollback(db)

    db.refresh(db_room)

    return db_room


def delete_room(
    db: Session,
    room_id: int,
) -> bool:
    """会議室削除"""
    db_room = get_room_by_id(
        db,
        room_id,
    )

    if db_room is None:
        return False

    db.delete(db_room)

    commit_or_rollback(db)

    return True
