"""
Dependencias de seguridad de FastAPI.
Proporciona get_current_user (flexible - retorna GUEST si no hay un token válido)
y require_expert_role (estricto - lanza 403 si no es EXPERT).
"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.domain.auth_models import UserSession
from app.services.auth_service import AuthService

# Esquema OAuth2 - auto_error=False para que los invitados no reciban 401 en cada petición
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)

# Instancia singleton del servicio (podría inyectarse mediante contenedor de DI en aplicaciones más grandes)
_auth_service = AuthService()


def get_auth_service() -> AuthService:
    """Proveedor de dependencia para AuthService."""
    return _auth_service


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserSession:
    """
    Protección flexible: siempre retorna una UserSession.
    Si el token falta o es inválido → sesión GUEST.
    Si el token es válido → sesión EXPERT.
    """
    return auth_service.get_current_session(token)


def require_expert_role(
    current_user: UserSession = Depends(get_current_user),
) -> UserSession:
    """
    Protección estricta: lanza HTTP 403 si el usuario no es un EXPERT autenticado.
    Se utiliza como dependencia de FastAPI en endpoints protegidos.
    """
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de Experto para esta acción.",
        )
    return current_user

