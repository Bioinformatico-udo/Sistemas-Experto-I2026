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

    @abstractmethod
    def save_species(self, species_list: List[Species]) -> None:
        pass

    @abstractmethod
    def save_facts_metadata(self, metadata: List[Dict[str, Any]]) -> None:
        pass

    @abstractmethod
    def save_rules(self, rules: List[Rule]) -> None:
        pass
