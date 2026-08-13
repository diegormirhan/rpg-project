from urllib.parse import urlencode

import httpx

from src.application.dtos.auth import DiscordUserDTO
from src.domain.ports.oauth import OAuthPort
from src.core.settings import settings


class DiscordOAuthAdapter(OAuthPort):

    BASE_URL = "https://discord.com/api"

    # def build_authorization_url(self) -> str:
    #     params = {
    #         "client_id": settings.client_id,
    #         "redirect_uri": settings.redirect_uri,
    #         "response_type": "code",
    #         "scope": "identify",
    #     }

    #     return f"{self.BASE_URL}/oauth2/authorize?{urlencode(params)}"

    async def authenticate(
        self,
        code: str,
    ) -> DiscordUserDTO:

        async with httpx.AsyncClient() as client:

            token_response = await client.post(
                f"{self.BASE_URL}/oauth2/token",
                data={
                    "client_id": settings.client_id,
                    "client_secret": settings.client_secret,
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": settings.redirect_uri,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
            )

            token_response.raise_for_status()

            access_token = token_response.json()["access_token"]

            user_response = await client.get(
                f"{self.BASE_URL}/users/@me",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
            )

            user_response.raise_for_status()

            user = user_response.json()

            avatar = None

            if user["avatar"]:
                avatar = (
                    f"https://cdn.discordapp.com/avatars/"
                    f"{user['id']}/{user['avatar']}.png"
                )

            return DiscordUserDTO(
                discord_id=user["id"],
                username=user["username"],
                avatar_url=avatar,
            )