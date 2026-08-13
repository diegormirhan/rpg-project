from src.domain.entities.user import User
from src.domain.ports.oauth import OAuthPort
from src.domain.ports.repositories.user_repository import UserRepository
from src.application.dtos.auth import AuthenticationResultDTO
from src.domain.ports.jwt import JwtPort


class AuthenticateWithDiscordUseCase:

    def __init__(
        self,
        oauth_provider: OAuthPort,
        user_repository: UserRepository,
        jwt_provider: JwtPort,
    ):
        self._oauth_provider = oauth_provider
        self._user_repository = user_repository
        self._jwt_provider = jwt_provider

    async def execute(self, code: str) -> AuthenticationResultDTO:

        discord_user = await self._oauth_provider.authenticate(code)

        user = self._user_repository.find_by_discord_id(
            discord_user.discord_id
        )

        if user is None:
            user = User.create(
                discord_id=discord_user.discord_id,
                username=discord_user.username,
                avatar_url=discord_user.avatar_url,
            )

            self._user_repository.save(user)

        else:
            user.update_profile(
                username=discord_user.username,
                avatar_url=discord_user.avatar_url,
            )

            self._user_repository.update(user)

        access_token = self._jwt_provider.generate(user.id)

        return AuthenticationResultDTO(
            access_token=access_token,
            token_type="Bearer",
            user_id=user.id,
        )