from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import TimestampMixin
from src.infrastructure.database.sql_alchemy.base import UUIDMixin

from src.domain.enums.character_class import CharacterClass
from src.domain.enums.equipment_slot import EquipmentSlot
from src.domain.enums.item_rarity import ItemRarity
from src.domain.enums.item_type import ItemType


class BaseItemModel(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "base_items"

    __table_args__ = (
        CheckConstraint("buy_price >= 0"),
        CheckConstraint("sell_price >= 0"),
        CheckConstraint("level_requirement >= 1"),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(
        String(100),
        nullable=False,
    )
    icon: Mapped[str | None] = mapped_column(
        String(255),
    )
    type: Mapped[ItemType] = mapped_column(
        Enum(ItemType, name="item_type"),
    )
    rarity: Mapped[ItemRarity] = mapped_column(
        Enum(ItemRarity, name="item_rarity"),
    )
    equip_slot: Mapped[EquipmentSlot | None] = mapped_column(
        Enum(EquipmentSlot, name="equipment_slot"),
    )
    class_restriction: Mapped[CharacterClass | None] = mapped_column(
        Enum(CharacterClass, name="character_class"),
    )
    atk_bonus: Mapped[int] = mapped_column(Integer, default=0)
    def_: Mapped[int] = mapped_column(
        "def",
    )
    speed_bonus: Mapped[int] = mapped_column(Integer, default=0)
    hp_bonus: Mapped[int] = mapped_column(Integer, default=0)
    level_requirement: Mapped[int] = mapped_column(Integer, default=1)
    stackable: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    max_stack: Mapped[int] = mapped_column(Integer, default=1)
    buy_price: Mapped[int] = mapped_column(Integer, nullable=False)
    sell_price: Mapped[int] = mapped_column(Integer, nullable=False)
    instances = relationship(
        "ItemInstanceModel",
        back_populates="item_base",
    )