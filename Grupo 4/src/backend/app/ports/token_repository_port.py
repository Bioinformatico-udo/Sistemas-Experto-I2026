"""
Puerto (interfaz) para el repositorio de tokens.
Define el contrato para generar y decodificar tokens JWT.
"""
from typing import Protocol
from app.domain.auth_models import TokenPayload


class TokenRepositoryPort(Protocol):
    """Puerto secundario: límite de infraestructura para operaciones de token."""

    def create_access_token(self, payload: TokenPayload) -> str:
        """Codifica un TokenPayload en una cadena JWT firmada."""
        ...

    def decode_token(self, token: str) -> TokenPayload | None:
        """
        Decodifica y valida un token JWT.
        Retorna el TokenPayload en caso de éxito, o None si es inválido o ha expirado.
        """
        ...

