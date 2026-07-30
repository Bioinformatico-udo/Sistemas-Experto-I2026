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

    def _save_json(self, filepath: str, data: Any) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_rules(self) -> List[Rule]:
        data = self._load_json(self.rules_filepath)
        return [Rule(**r) for r in data.get("rules", [])]

    def get_species(self) -> List[Species]:
        data = self._load_json(self.species_filepath)
        return [Species(**s) for s in data]

    def get_facts_metadata(self) -> List[Dict[str, Any]]:
        data = self._load_json(self.rules_filepath)
        return data.get("questions", [])

    def save_species(self, species_list: List[Species]) -> None:
        data = [s.dict() for s in species_list]
        self._save_json(self.species_filepath, data)

    def save_facts_metadata(self, metadata: List[Dict[str, Any]]) -> None:
        data = self._load_json(self.rules_filepath) if os.path.exists(self.rules_filepath) else {"questions": [], "rules": []}
        data["questions"] = metadata
        self._save_json(self.rules_filepath, data)

    def save_rules(self, rules: List[Rule]) -> None:
        data = self._load_json(self.rules_filepath) if os.path.exists(self.rules_filepath) else {"questions": [], "rules": []}
        data["rules"] = [r.dict() for r in rules]
        self._save_json(self.rules_filepath, data)
