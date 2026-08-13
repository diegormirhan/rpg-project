from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


# from inventory_service.adapters.outbound.gateways.fake_normalization_gateway import FakeHttpUnitNormalizationGateway
from src.application.use_cases.login_with_discord import LoginWithDiscordUseCase
from src.application.use_cases.authenticate_with_discord import AuthenticateWithDiscordUseCase
from src.infrastructure.jwt.jose_jwt import JoseJwtAdapter
from src.infrastructure.oauth.discord_oauth import DiscordOAuthAdapter
from src.infrastructure.database.repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository


def build_container(settings) -> dict:
    """
    Initializes all infrastructure adapters and returns them in a container.
    """   
    #this need be refactor, maybe use uow
    engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
    session_local: sessionmaker[Session] = sessionmaker(
        bind=engine, class_=Session, expire_on_commit=False
    )
    session = session_local()

    login_with_discord_uc = LoginWithDiscordUseCase()

    discord_oauth_adapter = DiscordOAuthAdapter()
    sql_alchemy_user_repository = SQLAlchemyUserRepository(session)
    jose_jwt_adapter = JoseJwtAdapter()
    authenticate_with_discord_uc = AuthenticateWithDiscordUseCase(
         discord_oauth_adapter,
         sql_alchemy_user_repository,
         jose_jwt_adapter
    )

    return {
        "login_with_discord_uc": login_with_discord_uc,
        "authenticate_with_discord_uc": authenticate_with_discord_uc
    }