from datetime import date
from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import UUIDMixin


class DailyLoginModel(UUIDMixin, Base):
    __tablename__ = "daily_logins"

    __table_args__ = (
        UniqueConstraint(
            "character_id",
            "login_date",
            name="uq_character_login_date",
        ),
    )

    character_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "characters.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    login_date: Mapped[date] = mapped_column(Date)
    streak_day: Mapped[int] = mapped_column(Integer)
    reward_claimed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    character = relationship("Character")