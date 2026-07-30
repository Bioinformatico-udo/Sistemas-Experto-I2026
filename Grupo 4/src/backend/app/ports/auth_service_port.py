"""
Puerto (interfaz) para el servicio de autenticación.
Define el contrato que la capa de aplicación debe implementar.
"""
from typing import Protocol
from app.domain.auth_models import TokenPayload, UserSession


class AuthServicePort(Protocol):
    """Puerto primario: define los casos de uso disponibles para la autenticación."""

    def login(self, username: str, password: str) -> str:
        """
        Valida las credenciales proporcionadas contra el usuario experto configurado.
        Retorna un token de acceso JWT firmado en caso de éxito.
        Lanza ValueError si las credenciales son inválidas.
        """
        ...

    def verify_token(self, token: str) -> UserSession:
        """
        Decodifica y valida un token JWT.
        Retorna la UserSession para un token válido.
        Retorna una sesión de invitado si el token falta, es inválido o ha expirado.
        """
        ...

    def get_current_session(self, token: str | None) -> UserSession:
        """
        Retorna la UserSession activa para el token dado (o invitado si es None).
        """
        ...

