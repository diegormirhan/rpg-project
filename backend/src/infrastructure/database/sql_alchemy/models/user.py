from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.domain.entities.user import User
from src.infrastructure.database.sql_alchemy.base import Base
from src.infrastructure.database.sql_alchemy.base import TimestampMixin
from src.infrastructure.database.sql_alchemy.base import UUIDMixin


class UserModel(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    discord_id: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )
    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    consecutive_login_days: Mapped[int] = mapped_column(
        default=0,
    )
    characters = relationship(
        "CharacterModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            discord_id=user.discord_id,
            username=user.username,
            avatar_url=user.avatar_url,
        )

    def to_domain(self) -> User:
        return User(
            id=self.id,
            discord_id=self.discord_id,
            username=self.username,
            avatar_url=self.avatar_url,
        )