from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import TimestampMixin
from src.infrastructure.database.sql_alchemy.base import UUIDMixin


class GuildModel(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "guilds"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    leader_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "characters.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    leader = relationship(
        "CharacterModel",
    )
    members = relationship(
        "GuildMemberModel",
        back_populates="guild",
        cascade="all, delete-orphan",
    )
    territories = relationship(
        "GuildTerritoryModel",
        back_populates="guild",
        cascade="all, delete-orphan",
    )