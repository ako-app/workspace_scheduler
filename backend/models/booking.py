from __future__ import annotations

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from backend.database import Base
from backend.models.mixins import TimestampMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.models.user import User
    from backend.models.room import Room


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
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="開始時刻"
    )

    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="終了時刻"
    )

    #  リレーションシップ
    user: Mapped[User] = relationship(
        back_populates="bookings",
    )
    room: Mapped[Room]= relationship(
        back_populates="bookings",
    )


