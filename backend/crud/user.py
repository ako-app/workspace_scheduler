from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.user import User
from backend.schemas.user import UserRequest


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

def create_user(
        db: Session,
        user: UserRequest,
       
) -> User:  
    """ユーザー登録"""
    db_user = User(
        username = user.username,
    )
    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user



    





