from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


TEST_DATABASE_URL = "sqlite:///./test.db"

# テスト用のエンジンを作成
testing_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# テスト用セッションを生成するクラス
TestingSessionLocal = sessionmaker(
    bind=testing_engine,
    autocommit=False,
    autoflush=False,
)


# 開発用DBへの依存を、テスト用DBへ差し替える
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()