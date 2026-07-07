from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.user import User
from backend.database import commit_or_rollback
from backend.schemas.user import UserRequest, UserUpdate
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def get_user_by_id(
        db: Session,
        user_id: int,
) -> User | None:
    """IDでユーザーを1件取得"""
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)

def get_user_by_username(
        db: Session,
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
    return password_hash.verify(
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
    hashed_password = password_hash.hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)

    commit_or_rollback(db)

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

     commit_or_rollback(db)

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

    commit_or_rollback(db)

    return True



def authenticate_user(
        db: Session,
        username: str,
        password: str,      
) -> User | None:
    """ログイン時にユーザー名とパスワードを確認する"""
    user = get_user_by_username(
        db,
        username,
    )
    if user is None:
        return None
    
    if not verify_password(
        password,
        user.hashed_password
    ):
        return None
    
    return user
    
    



