from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.domain.models import Rule, Species

class BaseKnowledgeRepository(ABC):
    @abstractmethod
    def get_rules(self) -> List[Rule]:
        pass

    @abstractmethod
    def get_species(self) -> List[Species]:
        pass

    @abstractmethod
    def get_facts_metadata(self) -> List[Dict[str, Any]]:
        pass
