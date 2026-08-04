from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.core.config import DATABASE_URL

# エンジン作成
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

# Session生成クラス
SessionLocal = sessionmaker(
    bind=engine,  # 使用するDB接続
    autocommit=False,
    autoflush=False,
)


# 全Modelの親クラス
class Base(DeclarativeBase):
    pass


def get_db():
    """データベースセッションの取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def commit_or_rollback(db: Session) -> None:
    """commitを実行し、失敗した場合はrollbackして例外を再送出する。"""
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
