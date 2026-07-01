from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from backend.core.config import DATABASE_URL


# エンジン作成
engine = create_engine( 
    DATABASE_URL, 
    connect_args={'check_same_thread':False},
    echo=True
)

# Session生成クラス
SessionLocal = sessionmaker(
    bind=engine, # 使用するDB接続
    autocommit=False,
    autoflush= False,
)

# 全Modelの親クラス
class Base(DeclarativeBase):
    pass

# データベースセッションの取得
def get_db():  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
