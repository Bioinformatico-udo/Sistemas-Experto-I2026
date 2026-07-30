"""
Adaptador de Tokens JWT (adaptador de salida).
Implementación concreta de TokenRepositoryPort usando python-jose.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.domain.auth_models import TokenPayload, UserRole
from app.config import settings


class JWTTokenAdapter:
    """Genera y decodifica tokens JWT utilizando python-jose."""

    def create_access_token(self, payload: TokenPayload) -> str:
        """Codifica un TokenPayload en una cadena JWT firmada."""
        now = datetime.now(tz=timezone.utc)
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        data = {
            "sub": payload.sub,
            "role": payload.role.value,
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
        }

        return jwt.encode(
            data,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def decode_token(self, token: str) -> Optional[TokenPayload]:
        """
        Decodifica un JWT y retorna el TokenPayload.
        Retorna None si el token es inválido o ha expirado.
        """
        try:
            data = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return TokenPayload(
                sub=data["sub"],
                role=UserRole(data.get("role", UserRole.EXPERT)),
                exp=data.get("exp"),
                iat=data.get("iat"),
            )
        except (JWTError, KeyError, ValueError):
            return None

