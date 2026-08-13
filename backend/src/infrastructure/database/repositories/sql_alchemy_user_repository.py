from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.exceptions import UserNotFound
from src.domain.entities.user import User
from src.domain.ports.repositories.user_repository import UserRepository
from src.infrastructure.database.sql_alchemy.models.user import UserModel


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: Session):
        self._session = session

    def find_by_discord_id(
        self,
        discord_id: str,
    ) -> User | None:

        statement = (
            select(UserModel)
            .where(UserModel.discord_id == discord_id)
        )

        result = self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return model.to_domain()

    def save(
        self,
        user: User,
    ) -> None:

        model = UserModel.from_domain(user)
        self._session.add(model)

        self._session.commit()

    def update(self, user: User) -> None:

        model = self._session.get(UserModel, user.id)

        if model is None:
            raise UserNotFound()

        model.username = user.username
        model.avatar_url = user.avatar_url
        model.discord_id = user.discord_id

        self._session.commit()