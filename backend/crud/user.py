from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.user import User
from backend.schemas.user import UserRequest, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(
        db :Session,
        user_id: int,
) -> User | None:
    """IDでユーザーを1件取得"""
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)

def get_user_by_username(
        db :Session,
        username: str,
) -> User | None:
    """ユーザー名でユーザーを1件取得"""
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)


def verify_password(
        plain_password: str,
        hashed_password: str,
) -> bool:
    """入力されたパスワードとハッシュ化済みパスワードを照合する"""
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )

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
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user

def update_user(
        db: Session,
        user_id: int,
        user: UserUpdate,
) -> User | None:
     """ユーザー更新"""
     db_user = get_user_by_id(
         db, 
         user_id,
     )

     if db_user is None:
         return None
     
     db_user.username = user.username

     #if user.password is not None:
        # db_user.hashed_password = pwd_context.hash(user.password)

     db.commit()

     db.refresh(db_user)

     return db_user

def delete_user(
        db: Session,
        user_id: int,
) -> bool:
    """ユーザー削除"""
    db_user = get_user_by_id(
        db, 
        user_id,
    )

    if db_user is None:
        return False
    
    db.delete(db_user)

    db.commit()

    return True









