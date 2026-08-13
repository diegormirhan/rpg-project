from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import TimestampMixin
from src.infrastructure.database.sql_alchemy.base import UUIDMixin

from src.domain.enums.transaction_status import TransactionStatus
from src.domain.enums.transaction_type import TransactionType


class TransactionModel(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "transactions"

    __table_args__ = (
        CheckConstraint("gold_amount >= 0"),
    )

    from_character_id: Mapped[UUID] = mapped_column(
        ForeignKey("characters.id"),
        index=True,
    )
    to_character_id: Mapped[UUID] = mapped_column(
        ForeignKey("characters.id"),
        index=True,
    )
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type"),
    )
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, name="transaction_status"),
        default=TransactionStatus.PENDING,
    )
    gold_amount: Mapped[int] = mapped_column(Integer,
        default=0,
    )
    items: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        default=list,
    )
    from_character = relationship(
        "CharacterModel",
        foreign_keys=[from_character_id],
    )
    to_character = relationship(
        "CharacterModel",
        foreign_keys=[to_character_id],
    )