"""
Router de Autenticación – Controlador FastAPI para los endpoints de autenticación.
Endpoints:
  POST /api/v1/auth/login  – Valida credenciales, retorna JWT
  POST /api/v1/auth/logout – Eliminación del token en el cliente (confirmación)
  GET  /api/v1/auth/me     – Verifica la sesión activa y retorna el rol
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

from app.domain.auth_models import UserSession
from app.services.auth_service import AuthService
from app.adapters.input.dependencies import get_auth_service, get_current_user

router = APIRouter(tags=["auth"])


# ─────────────────────────────────────────────
# Esquemas de Petición / Respuesta
# ─────────────────────────────────────────────

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 480 * 60  # segundos
    user: dict


class MeResponse(BaseModel):
    authenticated: bool
    username: Optional[str]
    role: str


class LogoutResponse(BaseModel):
    message: str


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Valida el nombre de usuario y la contraseña contra el usuario experto configurado.
    Retorna un token de acceso JWT en caso de éxito (HTTP 200).
    Lanza HTTP 401 si las credenciales son inválidas.
    """
    try:
        token = auth_service.login(
            username=form_data.username,
            password=form_data.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return LoginResponse(
        access_token=token,
        user={
            "username": form_data.username,
            "role": "EXPERT",
            "display_name": "Experto Taxónomo",
        },
    )


@router.get("/me", response_model=MeResponse)
def get_me(current_user: UserSession = Depends(get_current_user)):
    """
    Retorna el rol y el estado de autenticación de la sesión actual.
    Nunca lanza un error – las peticiones no autenticadas obtienen rol=GUEST.
    """
    return MeResponse(
        authenticated=current_user.authenticated,
        username=current_user.username if current_user.authenticated else None,
        role=current_user.role.value,
    )


@router.post("/logout", response_model=LogoutResponse)
def logout():
    """
    Confirma el cierre de sesión. La invalidación del token es manejada en el cliente
    eliminando el token del localStorage.
    """
    return LogoutResponse(message="Sesión cerrada exitosamente.")

