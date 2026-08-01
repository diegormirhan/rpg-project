from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import TimestampMixin
from src.infrastructure.database.sql_alchemy.base import UUIDMixin


class Zone(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "zones"
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )
    display_name: Mapped[str] = mapped_column(
        String(100),
    )
    minimum_level_suggested: Mapped[int] = mapped_column(
        default=1,
    )
    maximum_level_suggested: Mapped[int] = mapped_column(
        default=100,
    )
    allow_pvp: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    safe_zone: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    respawn_x: Mapped[int] = mapped_column(default=0)
    respawn_y: Mapped[int] = mapped_column(default=0)
    characters = relationship(
        "Character",
        back_populates="current_zone",
    )