from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.infrastructure.database.sql_alchemy.base import Base

from sqlalchemy.sql import func

class GuildTerritoryModel(Base):
    __tablename__ = "guild_territories"

    guild_id: Mapped[UUID] = mapped_column(
        ForeignKey("guilds.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tower_floor: Mapped[int] = mapped_column(Integer,
        primary_key=True,
    )
    conquered_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    expires_at: Mapped[datetime]= mapped_column(
        DateTime,
        nullable=False,
    )
    gold_accumulated: Mapped[int] = mapped_column(
        default=0,
    )
    guild = relationship(
        "GuildModel",
        back_populates="territories",
    )