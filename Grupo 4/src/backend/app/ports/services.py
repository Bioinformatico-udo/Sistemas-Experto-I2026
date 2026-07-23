from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.domain.models import InferenceResult

class InferenceService(ABC):
    @abstractmethod
    def infer(self, initial_facts: Dict[str, Any]) -> InferenceResult:
        pass

    @abstractmethod
    def get_questions(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_rules(self) -> List[Dict[str, Any]]:
        pass
