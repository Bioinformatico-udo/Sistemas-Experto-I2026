from typing import Dict, Any, List
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
        metadata = self.get_questions()
        
        engine = ForwardChainingEngine(rules=rules, species_list=species, facts_metadata=metadata)
        return engine.infer(initial_facts)

    def get_questions(self) -> List[Dict[str, Any]]:
        questions = self.repository.get_facts_metadata()
        for q in questions:
            opts = q.setdefault("options", [])
            if not any(opt.get("value") == "no_aplica" for opt in opts):
                opts.append({"label": "No aplica", "value": "no_aplica"})
        return questions

    def get_rules(self) -> List[Dict[str, Any]]:
        rules = self.repository.get_rules()
        return [r.dict() for r in rules]
