"""
Modelos del dominio para autenticación.
Define roles y estructuras de carga útil (payload) del token utilizadas en las capas.
"""
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class UserRole(str, Enum):
    GUEST = "GUEST"
    EXPERT = "EXPERT"


@dataclass
class TokenPayload:
    """Datos extraídos de un token JWT decodificado."""
    sub: str
    role: UserRole
    exp: Optional[int] = None
    iat: Optional[int] = None


@dataclass
class UserSession:
    """Representa el contexto del usuario activo derivado del token."""
    username: str
    role: UserRole
    authenticated: bool

    @property
    def is_expert(self) -> bool:
        return self.role == UserRole.EXPERT

    @classmethod
    def guest(cls) -> "UserSession":
        return cls(username="guest", role=UserRole.GUEST, authenticated=False)

