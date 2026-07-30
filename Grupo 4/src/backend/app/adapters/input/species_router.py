from fastapi import APIRouter, Depends, status
from app.schemas.species_schemas import CreateSpeciesRequest, CreateSpeciesResponse
from app.services.knowledge_base_service import KnowledgeBaseService
from app.adapters.input.dependencies import require_expert_role
from app.domain.auth_models import UserSession

router = APIRouter(tags=["species"])


# Inyección de dependencia del servicio que puede ser sobrescrita en main.py / tests
def get_knowledge_base_service() -> KnowledgeBaseService:
    raise NotImplementedError()


@router.post("/species", response_model=CreateSpeciesResponse, status_code=status.HTTP_201_CREATED)
def create_species(
    request: CreateSpeciesRequest,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
    expert_user: UserSession = Depends(require_expert_role),
):
    """
    Agrega una nueva especie a la Base de Conocimientos (requiere rol de Experto).
    Sincroniza automáticamente las preguntas y reglas de inferencia del sistema.
    """
    return kb_service.add_species(request)
