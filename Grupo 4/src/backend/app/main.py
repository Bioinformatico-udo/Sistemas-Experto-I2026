from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.input.routes import router as inference_router
from app.adapters.input.routes import get_inference_service
from app.adapters.input.auth_router import router as auth_router
from app.adapters.input.species_router import router as species_router
from app.adapters.input.species_router import get_knowledge_base_service
from app.adapters.output.json_repository import JSONKnowledgeRepository
from app.services.inference import InferenceServiceImpl
from app.services.knowledge_base_service import KnowledgeBaseService
from app.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Crustacean Expert System API",
        description="API para la clasificación taxonómica de crustáceos",
        version="1.0.0"
    )

    # Configuración de CORS para permitir al frontend comunicarse con la API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permitir todo para desarrollo
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configuración de Repositorio y Servicios
    repository = JSONKnowledgeRepository(
        rules_filepath=settings.RULES_FILEPATH,
        species_filepath=settings.SPECIES_FILEPATH,
    )
    inference_service = InferenceServiceImpl(repository=repository)
    kb_service = KnowledgeBaseService(repository=repository)

    # Sobreescribir las dependencias de los routers
    app.dependency_overrides[get_inference_service] = lambda: inference_service
    app.dependency_overrides[get_knowledge_base_service] = lambda: kb_service

    # ─── Routers ───────────────────────────────────────────
    # Inferencia
    app.include_router(inference_router, prefix="/api")

    # Autenticación
    app.include_router(auth_router, prefix="/api/v1/auth")

    # Gestión de Especies (Experto)
    app.include_router(species_router, prefix="/api/v1")
    app.include_router(species_router, prefix="/api")

    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "Crustacean Expert System API is running."}
