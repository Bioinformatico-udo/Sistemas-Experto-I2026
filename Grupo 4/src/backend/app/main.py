from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.input.routes import router as inference_router
from app.adapters.input.routes import get_inference_service
from app.adapters.output.json_repository import JSONKnowledgeRepository
from app.services.inference import InferenceServiceImpl
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
        allow_origins=["*"], # Permitir todo para desarrollo
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configuración de Inyección de Dependencias
    repository = JSONKnowledgeRepository(
        rules_filepath=settings.RULES_FILEPATH,
        species_filepath=settings.SPECIES_FILEPATH
    )
    inference_service = InferenceServiceImpl(repository=repository)

    # Sobreescribir la dependencia del router
    app.dependency_overrides[get_inference_service] = lambda: inference_service

    # Incluir las rutas
    app.include_router(inference_router, prefix="/api")

    return app

app = create_app()

@app.get("/")
def root():
    return {"message": "Crustacean Expert System API is running."}
