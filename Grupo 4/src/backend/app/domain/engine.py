from typing import List, Dict, Any
import os
import logging
from logging.handlers import RotatingFileHandler
from app.domain.models import Rule, InferenceResult, Species

# Configure inference logger with rotation
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("inference")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    os.path.join(log_dir, "inference.log"),
    maxBytes=5 * 1024 * 1024,  # 5 MB per file
    backupCount=5,
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

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
        
        logger.info(f"=== INICIO INFERENCIA | hechos iniciales: {list(initial_facts.keys())} ===")

        # Bucle de inferencia (Forward Chaining)
        changed = True
        while changed:
            changed = False
            for rule in list(rules_to_evaluate):
                if rule.id not in fired_rules and rule.evaluate(working_memory):
                    # Disparar regla: añadir consecuentes a la memoria de trabajo
                    for consequent in rule.consequents:
                        working_memory[consequent.fact] = consequent.value
                    logger.info(f"Regla disparada: [{rule.id}] {rule.name}")
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

        # Calcular certeza para cada especie basada en coincidencia de atributos
        certainties = []
        for species in self.species_list.values():
            total_attrs = len(species.attributes)
            if total_attrs == 0:
                match_ratio = 0.0
                matched = 0
            else:
                matched = sum(
                    1 for attr, val in species.attributes.items()
                    if working_memory.get(attr) == val
                )
                match_ratio = matched / total_attrs
            certainty_percent = round(match_ratio * 100, 2)
            certainties.append({
                "species_id": species.id,
                "species_name": species.name,
                "certainty": certainty_percent,
                "matched_attributes": matched,
                "total_attributes": total_attrs,
            })
            logger.debug(
                f"Species {species.name} ({species.id}): {matched}/{total_attrs} matches => {certainty_percent}%"
            )
        # Ordenar por mayor certeza
        certainties.sort(key=lambda x: x["certainty"], reverse=True)

        logger.info(
            f"=== FIN INFERENCIA | reglas disparadas: {fired_rules} | "
            f"especie: {detected_species.id if detected_species else 'ninguna'} | "
            f"siguiente pregunta: {next_recommended} ==="
        )

        return InferenceResult(
            working_memory=working_memory,
            fired_rules=fired_rules,
            detected_species=detected_species,
            next_recommended_fact=next_recommended,
            species_certainties=certainties,
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
        Prioriza el último hecho añadido en working_memory y utiliza la lógica de reglas parciales.
        """
        # Preguntar número de antenas si aún no se conoce
        if "numero_antenas" not in working_memory:
            return "numero_antenas"

        # Obtener el último hecho registrado
        last_fact = None
        if working_memory:
            last_fact = list(working_memory.keys())[-1]

        # Intentar encontrar una regla cuyo antecedente incluya el último hecho
        if last_fact:
            for rule in self.rules:
                if rule.id in fired_rules:
                    continue
                if not rule.antecedents:
                    continue
                antecedent_facts = [ant.fact for ant in rule.antecedents]
                if last_fact in antecedent_facts:
                    # Verificar viabilidad y obtener el siguiente hecho faltante
                    is_viable = True
                    missing_facts = []
                    for ant in rule.antecedents:
                        if ant.fact in working_memory:
                            if not ant.evaluate(working_memory):
                                is_viable = False
                                break
                        else:
                            missing_facts.append(ant.fact)
                    if is_viable and missing_facts:
                        return missing_facts[0]

        # Si no se encontró una regla basada en el último hecho, buscar cualquier regla viable parcial
        for rule in self.rules:
            if rule.id in fired_rules:
                continue
            if not rule.antecedents:
                continue
            is_viable = True
            missing_facts = []
            for ant in rule.antecedents:
                if ant.fact in working_memory:
                    if not ant.evaluate(working_memory):
                        is_viable = False
                        break
                else:
                    missing_facts.append(ant.fact)
            if is_viable and missing_facts:
                return missing_facts[0]

        # Como último recurso, devolver cualquier hecho no conocido presente en los metadatos de preguntas
        for q in self.facts_metadata:
            fact_name = q.get("fact")
            if fact_name and fact_name not in working_memory:
                return fact_name

        return None
