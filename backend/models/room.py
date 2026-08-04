from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base
from backend.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from backend.models.booking import Booking
    from backend.models.user import User


# roomモデル
class Room(TimestampMixin, Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        comment="会議室ID",
    )

    manager_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, comment="管理者ユーザーID"
    )

    room_name: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True, comment="会議室名"
    )

    capacity: Mapped[int] = mapped_column(nullable=False, comment="収容人数")

    #  リレーションシップ
    manager: Mapped[User] = relationship(
        back_populates="managed_rooms",
    )

    bookings: Mapped[list[Booking]] = relationship(
        back_populates="room",
    )
