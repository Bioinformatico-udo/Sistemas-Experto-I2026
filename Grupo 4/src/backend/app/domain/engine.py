from typing import List, Dict, Any
from app.domain.models import Rule, InferenceResult, Species

class ForwardChainingEngine:
    def __init__(self, rules: List[Rule], species_list: List[Species], facts_metadata: List[Dict[str, Any]]):
        self.rules = rules
        self.species_list = {s.id: s for s in species_list}
        self.facts_metadata = facts_metadata

    def infer(self, initial_facts: Dict[str, Any]) -> InferenceResult:
        """
        Ejecuta el motor de encadenamiento hacia adelante.
        Aplica reglas iterativamente hasta que no se disparen más reglas (punto fijo).
        """
        working_memory = dict(initial_facts)
        fired_rules: List[str] = []
        rules_to_evaluate = list(self.rules)
        
        # Bucle de inferencia (Forward Chaining)
        changed = True
        while changed:
            changed = False
            for rule in list(rules_to_evaluate):
                if rule.id not in fired_rules and rule.evaluate(working_memory):
                    # Disparar regla: añadir consecuentes a la memoria de trabajo
                    for consequent in rule.consequents:
                        working_memory[consequent.fact] = consequent.value
                    
                    fired_rules.append(rule.id)
                    rules_to_evaluate.remove(rule)
                    changed = True
                    break  # Romper para reiniciar el ciclo en orden de prioridad

        # Determinar especie
        detected_species = self._resolve_species(working_memory)
        
        # Calcular siguiente hecho recomendado si no se ha llegado a una especie final
        next_recommended = None
        if not detected_species:
            next_recommended = self._get_next_recommended_fact(working_memory, fired_rules)

        return InferenceResult(
            working_memory=working_memory,
            fired_rules=fired_rules,
            detected_species=detected_species,
            next_recommended_fact=next_recommended
        )

    def _resolve_species(self, working_memory: Dict[str, Any]) -> Species | None:
        """Determina si hay una especie identificada según la memoria de trabajo."""
        # Se puede identificar mediante "especie_detectada" o "clasificacion"
        species_id = working_memory.get("especie_detectada") or working_memory.get("clasificacion")
        if species_id and species_id in self.species_list:
            return self.species_list[species_id]
        return None

    def _get_next_recommended_fact(self, working_memory: Dict[str, Any], fired_rules: List[str]) -> str | None:
        """
        Devuelve el siguiente hecho que se debería preguntar al usuario.
        Busca en las reglas activas (que aún no se han disparado pero cuyos antecedentes no se han evaluado completamente).
        """
        # Dar prioridad a descartar el subfilo mediante antenas si no está definido
        if "numero_antenas" not in working_memory:
            return "numero_antenas"

        # Buscar reglas que tengan antecedentes parcialmente conocidos
        for rule in self.rules:
            if rule.id in fired_rules:
                continue
            
            # Ver si todos los hechos conocidos en sus antecedentes coinciden
            is_viable = True
            missing_facts = []
            
            for ant in rule.antecedents:
                if ant.fact in working_memory:
                    # Si el hecho ya se conoce pero no cumple la condición, esta regla no es viable
                    if not ant.evaluate(working_memory):
                        is_viable = False
                        break
                else:
                    missing_facts.append(ant.fact)
            
            # Si la regla sigue siendo viable y le faltan hechos, el primero de ellos es la recomendación
            if is_viable and missing_facts:
                return missing_facts[0]
                
        # Si no hay reglas viables parciales, devolver cualquier hecho faltante de los metadatos de preguntas
        for q in self.facts_metadata:
            fact_name = q.get("fact")
            if fact_name and fact_name not in working_memory:
                return fact_name

        return None
