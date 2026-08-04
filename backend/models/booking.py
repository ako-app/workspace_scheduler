from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base
from backend.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from backend.models.room import Room
    from backend.models.user import User


# bookingモデル
class Booking(TimestampMixin, Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        comment="予約ID",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        comment="予約ユーザーID",
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
        nullable=False,
        index=True,
        comment="会議室ID",
    )

    reserved_num: Mapped[int] = mapped_column(
        nullable=False,
        comment="参加人数",
    )
    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True, comment="開始時刻"
    )

    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True, comment="終了時刻"
    )

    #  リレーションシップ
    user: Mapped[User] = relationship(
        back_populates="bookings",
    )
    room: Mapped[Room] = relationship(
        back_populates="bookings",
    )
