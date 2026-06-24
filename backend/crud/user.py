from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.user import User
from backend.schemas.user import UserRequest

def get_user_by_id(
        db :Session,
        user_id: int,
) -> User | None:
    """IDでユーザーを1件取得"""
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


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

def update_user(
        db: Session,
        user_id: int,
        user: UserRequest,
) -> User | None:
     """ユーザー更新"""
     db_user = get_user_by_id(db, user_id)
     if db_user is None:
         return None
     
     db_user.username = user.username

     db.commit()

     db.refresh(db_user)

     return db_user

    





