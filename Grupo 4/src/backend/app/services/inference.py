from typing import Dict, Any
from app.ports.services import InferenceService
from app.ports.repositories import BaseKnowledgeRepository
from app.domain.engine import ForwardChainingEngine
from app.domain.models import InferenceResult

class InferenceServiceImpl(InferenceService):
    def __init__(self, repository: BaseKnowledgeRepository):
        self.repository = repository

    def infer(self, initial_facts: Dict[str, Any]) -> InferenceResult:
        rules = self.repository.get_rules()
        species = self.repository.get_species()
        metadata = self.repository.get_facts_metadata()
        
        engine = ForwardChainingEngine(rules=rules, species_list=species, facts_metadata=metadata)
        return engine.infer(initial_facts)
