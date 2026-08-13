from datetime import UTC, datetime, timedelta

from jose import jwt

from src.domain.ports.jwt import JwtPort
from src.core.settings import settings


class JoseJwtAdapter(JwtPort):

    def generate(self, user_id):
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(UTC) + timedelta(days=30),
        }

        return jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm="HS256",
        )

    def verify(self, token):
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
        )

        return payload["sub"]