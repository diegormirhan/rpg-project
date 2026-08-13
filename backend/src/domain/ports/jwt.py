from uuid import UUID
from abc import ABC

class JwtPort(ABC):

    def generate(self, user_id: UUID) -> str:
        pass

    def verify(self, token: str) -> UUID:
        pass