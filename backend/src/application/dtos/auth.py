from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AuthenticationResultDTO(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user_id: UUID

class DiscordUserDTO(BaseModel):
    discord_id: str
    username:str
    avatar_url: Optional[str] = None