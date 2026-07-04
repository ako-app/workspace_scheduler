from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.auth.jwt import create_access_token
from backend.schemas import UserResponse, UserRequest, UserUpdate, UserLogin, TokenResponse
from backend.crud.user import (
    get_users, 
    get_user_by_id, 
    create_user, 
    update_user, 
    delete_user,
    authenticate_user,
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@user_router.get(
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

@user_router.get(
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

@user_router.post(
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

@user_router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate,
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

@user_router.delete(
    "/{user_id}",
    status_code=204,
    response_model=None,
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
    

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
@auth_router.post(
    "/login",
    status_code=200,
    response_model=TokenResponse,
)
def login_user_endpoint(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    """ユーザーのログイン管理"""
    user_auth = authenticate_user(
        db,
        user.username,
        user.password,

    )
    if user_auth is None:
        raise HTTPException(
            status_code=401,
            detail="ユーザー名またはパスワードが正しくありません"
        )
    access_token = create_access_token(
        data={"sub": user_auth.username}
    )
    return  TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
