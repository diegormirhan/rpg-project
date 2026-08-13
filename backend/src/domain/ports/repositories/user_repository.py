from src.domain.entities.user import User
from abc import ABC

class UserRepository(ABC):
    def find_by_discord_id(
        self,
        discord_id: str,
    ) -> User | None:
       pass

    def save(
        self,
        user: User,
    ) -> None:
        pass

    def update(self, user: User) -> None:
        pass