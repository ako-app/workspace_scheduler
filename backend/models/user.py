from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base
from backend.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from backend.models.booking import Booking
    from backend.models.room import Room


# userモデル
class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, comment="ユーザーID")

    username: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True, comment="ユーザー名"
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="ハッシュ化されたパスワード"
    )

    #  リレーションシップ
    managed_rooms: Mapped[list[Room]] = relationship(
        back_populates="manager",
    )
    bookings: Mapped[list[Booking]] = relationship(
        back_populates="user",
    )
