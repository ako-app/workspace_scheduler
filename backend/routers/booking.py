from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.auth.dependencies import get_current_user
from backend.core.exceptions import BookingConflictError
from backend.models.user import User
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """予約一覧を取得する"""
    return get_bookings(
        db, 
        skip=skip, 
        limit=limit,
    )

@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def read_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """IDで予約を1件取得"""
    booking = get_booking_by_id(
        db,
        booking_id,
    )
    if booking is None:
        raise HTTPException(
            status_code=404, 
            detail="予約情報が見つかりません",
        )
    return booking

@router.post(
    "/", 
    response_model=BookingResponse, 
    status_code=201
)
def create_booking_endpoint(
    booking: BookingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """予約を作成する"""
    try:
        return create_booking(
            db,
            booking,
            user_id = current_user.id
        )
    except BookingConflictError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
)
def update_booking_endpoint(
    booking_id: int,
    booking: BookingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """予約を更新する(本人のみ)"""
    db_booking = get_booking_by_id(db, booking_id)
    if db_booking is None:
        raise HTTPException(
            status_code=404, 
            detail="予約情報が見つかりません",
        )
    if db_booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="この操作を行う権限がありません",
        )
    try:
        booking_update = update_booking(
            db,
            booking_id,
            booking,
       )
    except BookingConflictError as e:
        raise HTTPException(
            status_code=409, 
            detail=str(e),
        )
    
    return booking_update

@router.delete(
    "/{booking_id}",
    status_code=204,
    response_model=None,
)
def delete_booking_endpoint(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """予約を削除する"""
    db_booking = get_booking_by_id(db, booking_id)
    if db_booking is None:
        raise HTTPException(
            status_code=404, 
            detail="予約情報が見つかりません",

        )
    if db_booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="この操作を行う権限がありません",
        )
    
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
    



