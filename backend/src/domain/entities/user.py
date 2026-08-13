from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass
class User:
    discord_id: str
    username: str
    avatar_url: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_login: datetime | None = None
    consecutive_login_days: int = 0
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def create(
        cls,
        discord_id: str,
        username: str,
        avatar_url: str | None = None,
    ) -> "User":
        return cls(
            discord_id=discord_id,
            username=username,
            avatar_url=avatar_url,
        )

    def update_profile(
        self,
        username: str,
        avatar_url: str | None,
    ) -> None:
        self.username = username
        self.avatar_url = avatar_url

    def register_login(self) -> None:
        self.last_login = datetime.now(UTC)

        self.consecutive_login_days += 1