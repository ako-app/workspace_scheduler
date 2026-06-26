from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import UserResponse, UserRequest
from backend.crud.user import (
    get_users, 
    get_user_by_id, 
    create_user, 
    update_user, 
    delete_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "/",
    response_model=list[UserResponse],     
)
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """ユーザー一覧を取得する"""
    return get_users(db, skip=skip, limit=limit)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """IDでユーザーを1件取得"""
    user = get_user_by_id(
        db,
        user_id,
    )
    if user is None:
        raise HTTPException(status_code=404, detail="ユーザー情報が見つかりません",)
    return user

@router.post(
    "/", 
    response_model=UserResponse, 
    status_code=201
)
def create_user_endpoint(
    user: UserRequest,
    db: Session = Depends(get_db),
):
    """ユーザーを作成する"""
    return create_user(
        db,
        user,
    )

@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user_endpoint(
    user_id: int,
    user: UserRequest,
    db: Session = Depends(get_db),
):
    """ユーザーを更新する"""
    user_update = update_user(
        db,
        user_id,
        user,
    )
    if user_update is None:
        raise HTTPException(status_code=404, detail="ユーザー情報が見つかりません",)
    return user_update

@router.delete(
    "/{user_id}",
    status_code=204,
)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    """ユーザーを削除する"""
    user_delete = delete_user(
        db,
        user_id,
    )
    if not user_delete:
        raise HTTPException(
            status_code=404,
            detail="ユーザー情報が見つかりません",
        )
    
    return
    


