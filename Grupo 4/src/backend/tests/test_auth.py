import pytest
from app.services.auth_service import AuthService
from app.domain.auth_models import UserRole
from app.config import settings

def test_auth_service_in_code_credentials():
    auth_service = AuthService()
    
    # Credenciales almacenadas directamente en código
    token = auth_service.login(settings.EXPERT_USERNAME, settings.EXPERT_PASSWORD)
    assert token is not None
    assert isinstance(token, str)
    
    # Sesión activa para token válido
    session = auth_service.get_current_session(token)
    assert session.authenticated is True
    assert session.username == settings.EXPERT_USERNAME
    assert session.role == UserRole.EXPERT

def test_auth_service_invalid_credentials():
    auth_service = AuthService()
    
    with pytest.raises(ValueError, match="Credenciales inválidas"):
        auth_service.login(settings.EXPERT_USERNAME, "contraseña_incorrecta")
        
    with pytest.raises(ValueError, match="Credenciales inválidas"):
        auth_service.login("usuario_inexistente", settings.EXPERT_PASSWORD)
