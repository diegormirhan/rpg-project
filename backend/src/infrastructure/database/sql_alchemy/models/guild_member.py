from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from src.infrastructure.database.sql_alchemy.base import Base

from src.domain.enums.guild_rank import GuildRank


class GuildMemberModel(Base):
    __tablename__ = "guild_members"

    guild_id: Mapped[UUID] = mapped_column(
        ForeignKey("guilds.id", ondelete="CASCADE"),
        primary_key=True,
    )
    character_id: Mapped[UUID] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
    )
    rank: Mapped[GuildRank] = mapped_column(
        Enum(GuildRank, name="guild_rank"),
        default=GuildRank.MEMBER,
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    guild = relationship(
        "Guild",
        back_populates="members",
    )
    character = relationship(
        "Character",
    )