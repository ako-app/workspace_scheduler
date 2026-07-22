from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.models.booking import Booking
from backend.core.exceptions import BookingConflictError
from backend.database import commit_or_rollback
from backend.schemas.booking import BookingRequest

def get_booking_by_id(
    db: Session,
    booking_id: int,
) -> Booking | None:
    """IDで予約を1件取得"""
    stmt = select(Booking).where(Booking.id == booking_id)
    return db.scalar(stmt)



def get_bookings(
    db: Session, 
    skip: int = 0,
    limit: int = 100,
) -> list[Booking]:
    """予約一覧を取得する"""
    stmt = (
        select(Booking)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()

def has_overlapping_booking(
    db: Session,
    room_id: int,
    start_at: datetime,
    end_at: datetime,
    exclude_booking_id: int | None = None,
) -> bool:
    """指定した部屋・時間帯に重複する予約が存在するか"""
    stmt = select(Booking).where(
        Booking.room_id == room_id,
        Booking.start_at < end_at,
        Booking.end_at > start_at,
    )

    if exclude_booking_id is not None:
        stmt = stmt.where(Booking.id != exclude_booking_id)

    return db.scalar(stmt) is not None


def create_booking(
    db: Session,
    booking: BookingRequest,
    user_id: int,    
) -> Booking:
    """予約登録"""
    if has_overlapping_booking(
        db,
        booking.room_id,
        booking.start_at,
        booking.end_at,
    ):
        raise BookingConflictError()
    
    db_booking = Booking(
        user_id=user_id,
        room_id=booking.room_id,
        start_at=booking.start_at,
        end_at=booking.end_at,
        reserved_num=booking.reserved_num,
    )
    
    db.add(db_booking)
    commit_or_rollback(db)
    db.refresh(db_booking)

    return db_booking

def update_booking(
    db: Session,
    booking_id: int,
    booking: BookingRequest,
) -> Booking | None:
    """予約更新"""
    db_booking = get_booking_by_id(db, booking_id)
    if db_booking is None:
        return None
     
    if has_overlapping_booking(
        db,
        booking.room_id,
        booking.start_at,
        booking.end_at,
        exclude_booking_id=booking_id,
    ):
        raise BookingConflictError()
     
    db_booking.room_id = booking.room_id
    db_booking.start_at = booking.start_at
    db_booking.end_at = booking.end_at
    db_booking.reserved_num = booking.reserved_num

    commit_or_rollback(db)
    db.refresh(db_booking)

    return db_booking

def delete_booking(
    db: Session,
    booking_id: int,
) -> bool:
    """予約削除"""
    db_booking = get_booking_by_id(
        db, 
        booking_id,
    )

    if db_booking is None:
        return False
    
    db.delete(db_booking)
    commit_or_rollback(db)

    return True

