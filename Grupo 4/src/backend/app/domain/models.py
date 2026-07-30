from typing import Any, List, Dict
from pydantic import BaseModel, Field

class Fact(BaseModel):
    name: str
    value: Any

class Antecedent(BaseModel):
    fact: str
    operator: str  # "==", "!=", ">", "<", "in", etc.
    value: Any

    def evaluate(self, working_memory: Dict[str, Any]) -> bool:
        """Evalúa si el antecedente se cumple en la memoria de trabajo."""
        if self.fact not in working_memory:
            return False
        
        current_value = working_memory[self.fact]
        
        if self.operator == "==":
            return current_value == self.value
        elif self.operator == "!=":
            return current_value != self.value
        elif self.operator == ">":
            return current_value > self.value
        elif self.operator == "<":
            return current_value < self.value
        elif self.operator == "in":
            return current_value in self.value
        return False

class Consequent(BaseModel):
    fact: str
    value: Any

class Rule(BaseModel):
    id: str
    name: str
    description: str
    antecedents: List[Antecedent]
    consequents: List[Consequent]

    def evaluate(self, working_memory: Dict[str, Any]) -> bool:
        """Evalúa si todos los antecedentes de la regla se cumplen."""
        if not self.antecedents:
            return False
        return all(antecedent.evaluate(working_memory) for antecedent in self.antecedents)

class Species(BaseModel):
    id: str
    name: str
    description: str = ""
    habitat: str = ""
    field_characteristics: List[str] = Field(default_factory=list)
    image_url: str = ""
    attributes: Dict[str, Any] = Field(default_factory=dict)
    taxonomy: Dict[str, str] = Field(default_factory=dict)

class InferenceResult(BaseModel):
    working_memory: Dict[str, Any]
    fired_rules: List[str]
    detected_species: Species | None
    next_recommended_fact: str | None
    species_certainties: List[Dict[str, Any]] = Field(default_factory=list)
