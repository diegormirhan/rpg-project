from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import TimestampMixin
from src.infrastructure.database.sql_alchemy.base import UUIDMixin

from src.domain.enums.enchantment_type import EnchantmentType


class ItemInstanceModel(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "item_instances"

    __table_args__ = (
        CheckConstraint("quantity >= 1"),
        CheckConstraint("enchantment_level >= 0"),
    )

    item_base_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "base_items.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    owner_character_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "characters.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    enchantment_level: Mapped[int] = mapped_column(Integer, default=0)
    enchantment_type: Mapped[EnchantmentType] = mapped_column(
        Enum(
            EnchantmentType,
            name="enchantment_type",
        ),
        default=EnchantmentType.NONE,
    )
    is_equipped: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    slot_position: Mapped[int | None] =  mapped_column(Integer)
    acquired_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    item_base = relationship(
        "ItemBase",
        back_populates="instances",
    )
    owner = relationship(
        "Character",
        back_populates="inventory",
    )