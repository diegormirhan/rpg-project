from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import UUIDMixin


class PvpRecord(UUIDMixin, Base):
    __tablename__ = "pvp_records"

    killer_character_id: Mapped[UUID] = mapped_column(
        ForeignKey("characters.id"),
        index=True,
    )
    victim_character_id: Mapped[UUID] = mapped_column(
        ForeignKey("characters.id"),
        index=True,
    )
    zone_id: Mapped[UUID] = mapped_column(
        ForeignKey("zones.id"),
        index=True,
    )
    killed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    killer = relationship(
        "Character",
        foreign_keys=[killer_character_id],
    )
    victim = relationship(
        "Character",
        foreign_keys=[victim_character_id],
    )
    zone = relationship("Zone")
