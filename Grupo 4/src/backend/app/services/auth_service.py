"""
Servicio de Autenticación (capa de aplicación).
Implementa los casos de uso de autenticación utilizando credenciales fijas integradas directamente en el código.
"""
from app.config import settings
from app.domain.auth_models import TokenPayload, UserRole, UserSession
from app.adapters.output.security.jwt_token_adapter import JWTTokenAdapter


class AuthService:
    """
    Valida las credenciales del experto almacenadas directamente en código y emite tokens JWT.
    Las credenciales son fijas para el usuario experto único ('experto' / 'experto123').
    """

    def __init__(self):
        self._token_adapter = JWTTokenAdapter()

    # ─────────────────────────────────────────────
    # Métodos públicos
    # ─────────────────────────────────────────────

    def login(self, username: str, password: str) -> str:
        """
        Valida las credenciales contra el usuario experto integrado en código.
        Retorna un token de acceso JWT firmado en caso de éxito.
        Lanza ValueError si las credenciales son inválidas.
        """
        if not self._verify_credentials(username, password):
            raise ValueError("Credenciales inválidas. Verifique el nombre de usuario y la contraseña.")

        payload = TokenPayload(sub=username, role=UserRole.EXPERT)
        return self._token_adapter.create_access_token(payload)

    def get_current_session(self, token: str | None) -> UserSession:
        """
        Retorna la UserSession activa para el token dado.
        Recae en una sesión de invitado si el token es None, inválido o ha expirado.
        """
        if not token:
            return UserSession.guest()

        payload = self._token_adapter.decode_token(token)
        if not payload:
            return UserSession.guest()

        return UserSession(
            username=payload.sub,
            role=payload.role,
            authenticated=True,
        )

    # ─────────────────────────────────────────────
    # Métodos auxiliares privados
    # ─────────────────────────────────────────────

    def _verify_credentials(self, username: str, password: str) -> bool:
        """Verifica el usuario y la contraseña almacenados directamente en código."""
        return username == settings.EXPERT_USERNAME and password == settings.EXPERT_PASSWORD

