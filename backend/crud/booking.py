from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.booking import Booking
from backend.schemas.booking import BookingRequest


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

def create_booking(
        db: Session,
        booking: BookingRequest,
       
) -> Booking:  
    """予約登録"""
    db_booking= Booking(
        room_id= booking.room_id,
        start_at = booking.start_at,
        end_at = booking.end_at,
        reserved_num = booking.reserved_num,
        # TODO: JWT認証実装後に id を設定
     )
    
    db.add(db_booking)

    db.commit()

    db.refresh(db_booking)

    return db_booking

