from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from app.domain.models import InferenceResult
from app.ports.services import InferenceService

router = APIRouter()


def get_inference_service() -> InferenceService:
    raise NotImplementedError()

@router.post("/infer", response_model=InferenceResult)
def run_inference(
    initial_facts: Dict[str, Any],
    service: InferenceService = Depends(get_inference_service)
):
    """
    Ejecuta el motor de inferencia basándose en los hechos iniciales proporcionados.
    """
    return service.infer(initial_facts)

@router.get("/questions", response_model=List[Dict[str, Any]])
def get_questions(
    service: InferenceService = Depends(get_inference_service)
):
    """
    Obtiene la lista de preguntas y metadatos para el diagnóstico.
    """
    return service.get_questions()

@router.get("/rules", response_model=List[Dict[str, Any]])
def get_rules(
    service: InferenceService = Depends(get_inference_service)
):
    """
    Obtiene la lista completa de reglas del motor.
    """
    return service.get_rules()
