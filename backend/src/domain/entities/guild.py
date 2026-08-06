from uuid import UUID, uuid4
from dataclasses import dataclass, field
from src.domain.enums.guild_rank import GuildRank

@dataclass(kw_only=True)
class GuildMember:
    player_id: UUID
    rank: GuildRank

@dataclass(kw_only=True)
class Guild:
    id: UUID = field(default_factory=uuid4)
    name: str
    description: str
    members: list[GuildMember] = field(default_factory=list)
    