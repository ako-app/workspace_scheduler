from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from backend.models.mixins import TimestampMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.models.room import Room
    from backend.models.booking import Booking

#from datetime import datetime, UTC
#from sqlalchemy import DateTime,func


# userモデル
class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        comment="管理者ユーザーID"
    )

    username: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
        comment="管理者のユーザー名"
    )

    #  リレーションシップ
    managed_rooms: Mapped[list[Room]] = relationship(
        back_populates="manager",
    )
    bookings: Mapped[list[Booking]] = relationship(
        back_populates="user",
    )


    #created_at: Mapped[datetime] = mapped_column(
       # DateTime(timezone=True),
       # server_default=func.now(),
        #nullable=False,

    #)

    #updated_at: Mapped[datetime] = mapped_column(
     #   DateTime(timezone=True),
     #   server_default=func.now(),
     #   onupdate=func.now(),
     #   nullable=False,
    #)



