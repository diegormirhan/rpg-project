
from abc import ABC
from src.application.dtos.auth import DiscordUserDTO

class OAuthPort(ABC):


    # def build_authorization_url(self) -> str:
        # pass

    async def authenticate(
        self,
        code: str,
    ) -> DiscordUserDTO:
        pass