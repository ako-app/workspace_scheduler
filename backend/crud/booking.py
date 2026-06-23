from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.booking import Booking
#from backend.schemas.user import UserRequest, UserResponse


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

def get_booking(
        db: Session,
        booking_id: int,     
) -> Booking | None:
    """予約詳細を取得する"""
    stmt = select(Booking).where(
        Booking.id == booking_id
    )

    return db.scalar(stmt)
