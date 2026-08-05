from datetime import UTC, datetime, timedelta

from pwdlib import PasswordHash
from sqlalchemy import select

from backend.database import SessionLocal
from backend.models.booking import Booking
from backend.models.room import Room
from backend.models.user import User

password_hash = PasswordHash.recommended()

DEMO_USERNAME = "demo_user"
DEMO_PASSWORD = "demo_password"


def seed_data() -> None:
    """開発・デモ環境へ初期データを投入する。"""
    db = SessionLocal()

    try:
        # 同じデモユーザーが存在する場合は、重複登録を避けて終了する
        existing_user = db.scalar(select(User).where(User.username == DEMO_USERNAME))

        if existing_user is not None:
            print("シードデータはすでに登録されています。")
            return

        # デモ用ユーザー
        demo_user = User(
            username=DEMO_USERNAME,
            hashed_password=password_hash.hash(DEMO_PASSWORD),
        )

        db.add(demo_user)
        db.flush()

        # デモ用会議室
        rooms = [
            Room(
                manager_id=demo_user.id,
                room_name="会議室A",
                capacity=4,
            ),
            Room(
                manager_id=demo_user.id,
                room_name="会議室B",
                capacity=8,
            ),
            Room(
                manager_id=demo_user.id,
                room_name="大会議室",
                capacity=20,
            ),
        ]

        db.add_all(rooms)
        db.flush()

        # 実行日の翌日を基準に予約日時を作成
        tomorrow = datetime.now(UTC) + timedelta(days=1)

        bookings = [
            Booking(
                user_id=demo_user.id,
                room_id=rooms[0].id,
                reserved_num=3,
                start_at=tomorrow.replace(
                    hour=10,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
                end_at=tomorrow.replace(
                    hour=11,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
            ),
            Booking(
                user_id=demo_user.id,
                room_id=rooms[1].id,
                reserved_num=6,
                start_at=tomorrow.replace(
                    hour=13,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
                end_at=tomorrow.replace(
                    hour=14,
                    minute=30,
                    second=0,
                    microsecond=0,
                ),
            ),
        ]

        db.add_all(bookings)
        db.commit()

        print("シードデータを登録しました。")
        print(f"ユーザー名: {DEMO_USERNAME}")
        print(f"パスワード: {DEMO_PASSWORD}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
