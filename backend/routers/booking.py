from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import BookingResponse, BookingRequest
from backend.crud.booking import (
    get_bookings, 
    get_booking_by_id, 
    create_booking, 
    update_booking, 
    delete_booking
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get(
    "/",
    response_model=list[BookingResponse],     
)
def read_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """予約一覧を取得する"""
    return get_bookings(db, skip=skip, limit=limit)

@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def read_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    """IDで予約を1件取得"""
    booking = get_booking_by_id(
        db,
        booking_id,
    )
    if booking is None:
        raise HTTPException(status_code=404, detail="予約情報が見つかりません",)
    return booking

@router.post(
    "/", 
    response_model=BookingResponse, 
    status_code=201
)
def create_booking_endpoint(
    booking: BookingRequest,
    db: Session = Depends(get_db),
):
    """予約を作成する"""
    return create_booking(
        db,
        booking,
    )

@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
)
def update_booking_endpoint(
    booking_id: int,
    booking: BookingRequest,
    db: Session = Depends(get_db),
):
    """予約を更新する"""
    booking_update = update_booking(
        db,
        booking_id,
        booking,
    )
    if booking_update is None:
        raise HTTPException(status_code=404, detail="予約が見つかりません",)
    return booking_update

@router.delete(
    "/{booking_id}",
    status_code=204,
)
def delete_booking_endpoint(
    booking_id: int,
    db: Session = Depends(get_db),
):
    """予約を削除する"""
    booking_delete = delete_booking(
        db,
        booking_id,
    )
    if not booking_delete:
        raise HTTPException(
            status_code=404,
            detail="予約情報が見つかりません",
        )
    return
    



