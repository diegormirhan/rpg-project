from typing import Any
from uuid import UUID

from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import TimestampMixin
from src.infrastructure.database.sql_alchemy.base import UUIDMixin
from src.domain.enums.character_class import CharacterClass


class Character(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "characters"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    current_zone_id: Mapped[UUID] = mapped_column(
        ForeignKey("zones.id"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100))
    class_type: Mapped[CharacterClass] = mapped_column(
        Enum(CharacterClass, name="character_class"),
    )
    level: Mapped[int] = mapped_column(default=1)
    xp: Mapped[int] = mapped_column(default=0)
    gold: Mapped[int] = mapped_column(default=0)
    hp_current: Mapped[int] = mapped_column(Integer)
    hp_max: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column("def")
    speed: Mapped[int] = mapped_column(Integer)
    buff_current: Mapped[int] = mapped_column(Integer)
    appearance: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
    )
    position_x: Mapped[int] = mapped_column(Integer, default=0)
    position_y: Mapped[int] = mapped_column(Integer, default=0)
    tower_highest_floor: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped["User"] = relationship(
        back_populates="characters",
    )
    current_zone: Mapped["Zone"] = relationship(
        back_populates="characters",
    )
    inventory = relationship(
        "ItemInstance",
        back_populates="owner",
        cascade="all, delete-orphan",
    )