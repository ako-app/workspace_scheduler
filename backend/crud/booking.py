from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.booking import Booking
from backend.schemas.booking import BookingRequest

def get_booking_by_id(
        db :Session,
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

def create_booking(
        db: Session,
        booking: BookingRequest,
        user_id : int,
       
) -> Booking:  
    """予約登録"""
    db_booking= Booking(
        user_id=user_id,
        room_id= booking.room_id,
        start_at = booking.start_at,
        end_at = booking.end_at,
        reserved_num = booking.reserved_num,
     )
    
    db.add(db_booking)

    db.commit()

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
     
     db_booking.room_id = booking.room_id
     db_booking.start_at = booking.start_at
     db_booking.end_at = booking.end_at
     db_booking.reserved_num = booking.reserved_num

     db.commit()

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

    db.commit()

    return True
