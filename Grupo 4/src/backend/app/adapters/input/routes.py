from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.domain.models import InferenceResult
from app.ports.services import InferenceService

router = APIRouter()

# This function will be overridden in main.py during dependency injection setup
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
