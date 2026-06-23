from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.user import User
#from backend.schemas.user import UserRequest, UserResponse


def get_users(
        db: Session, 
        skip: int = 0,
        limit: int = 100,
) -> list[User]:
    """ユーザー一覧を取得する"""
    stmt = (
        select(User)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(stmt).all()



