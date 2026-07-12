import json
import os
from typing import List, Dict, Any
from app.ports.repositories import BaseKnowledgeRepository
from app.domain.models import Rule, Species

class JSONKnowledgeRepository(BaseKnowledgeRepository):
    def __init__(self, rules_filepath: str, species_filepath: str):
        self.rules_filepath = rules_filepath
        self.species_filepath = species_filepath

    def _load_json(self, filepath: str) -> Any:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_rules(self) -> List[Rule]:
        data = self._load_json(self.rules_filepath)
        return [Rule(**r) for r in data.get("rules", [])]

    def get_species(self) -> List[Species]:
        data = self._load_json(self.species_filepath)
        return [Species(**s) for s in data]

    def get_facts_metadata(self) -> List[Dict[str, Any]]:
        data = self._load_json(self.rules_filepath)
        return data.get("questions", [])
