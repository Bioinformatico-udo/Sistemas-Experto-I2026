from abc import ABC, abstractmethod
from typing import Dict, Any
from app.domain.models import InferenceResult

class InferenceService(ABC):
    @abstractmethod
    def infer(self, initial_facts: Dict[str, Any]) -> InferenceResult:
        pass
