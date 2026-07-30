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
        Inicializa automáticamente numero_antenas = 2 si no se provee.
        Aplica reglas iterativamente hasta que no se disparen más reglas (punto fijo).
        """
        working_memory = dict(initial_facts)
        working_memory.setdefault("numero_antenas", 2)

        fired_rules: List[str] = []
        rules_to_evaluate = list(self.rules)
        
        logger.info(f"=== INICIO INFERENCIA | hechos iniciales: {list(working_memory.keys())} ===")

        # Bucle de inferencia (Forward Chaining)
        changed = True
        while changed:
            changed = False
            for rule in list(rules_to_evaluate):
                if rule.id not in fired_rules and rule.evaluate(working_memory):
                    for consequent in rule.consequents:
                        working_memory[consequent.fact] = consequent.value
                    logger.info(f"Regla disparada: [{rule.id}] {rule.name}")
                    fired_rules.append(rule.id)
                    rules_to_evaluate.remove(rule)
                    changed = True
                    break

        # Determinar especie comprobando la especie viable con 100% de certeza en todos sus atributos o confirmación de regla
        detected_species = self._resolve_species(working_memory, fired_rules)

        # Si se resolvió una especie final (100% certeza), ajustar memoria de trabajo y descarte de reglas no coincidentes
        if detected_species:
            working_memory["especie_detectada"] = detected_species.id

            cleaned_fired_rules = []
            for r_id in fired_rules:
                rule_obj = next((r for r in self.rules if r.id == r_id), None)
                if rule_obj:
                    different_species_consequent = any(
                        c.fact in ("especie_detectada", "clasificacion") and str(c.value) != detected_species.id
                        for c in rule_obj.consequents
                    )
                    if different_species_consequent:
                        logger.info(f"Descartada regla '{r_id}' por haber asignado una especie distinta a '{detected_species.id}'")
                        continue
                cleaned_fired_rules.append(r_id)

            confirming_rule = next(
                (r for r in self.rules if any(
                    c.fact in ("especie_detectada", "clasificacion") and str(c.value) == detected_species.id
                    for c in r.consequents
                )),
                None
            )
            if confirming_rule:
                if confirming_rule.id not in cleaned_fired_rules:
                    cleaned_fired_rules.append(confirming_rule.id)
            else:
                target_rule_id = f"R_{detected_species.id}"
                if target_rule_id not in cleaned_fired_rules:
                    cleaned_fired_rules.append(target_rule_id)

            fired_rules = cleaned_fired_rules

        # Calcular siguiente hecho recomendado si no se ha llegado a una especie final con 100%
        next_recommended = None
        if not detected_species:
            next_recommended = self._get_next_recommended_fact(working_memory, fired_rules)

        # Calcular grado de coincidencia para TODAS las especies (sin importar el valor de los atributos)
        certainties = []
        for species in self.species_list.values():
            if species.id in ("No_Crustáceo", "Especie_no_identificada"):
                continue

            total_attrs = len(species.attributes)
            if total_attrs == 0:
                match_ratio = 1.0 if (detected_species and detected_species.id == species.id) else 0.0
                matched = 0
            else:
                matched = sum(
                    1 for attr, val in species.attributes.items()
                    if working_memory.get(attr) == val
                )
                match_ratio = matched / total_attrs
            certainty_percent = round(match_ratio * 100, 2)

            certainties.append({
                "id": species.id,
                "species_id": species.id,
                "name": species.name,
                "species_name": species.name,
                "certainty": certainty_percent,
                "matched_attributes": matched,
                "total_attributes": total_attrs,
                "description": species.description,
                "habitat": species.habitat,
                "field_characteristics": species.field_characteristics,
                "image_url": species.image_url,
                "attributes": species.attributes,
                "taxonomy": species.taxonomy,
            })

        certainties.sort(key=lambda x: (x["certainty"], x["matched_attributes"]), reverse=True)

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

    def _is_species_viable(self, species: Species, working_memory: Dict[str, Any]) -> bool:
        """
        Comprueba si una especie es viable con la memoria de trabajo actual.
        Evalúa todos los atributos morfológicos de species.attributes.
        Si algún hecho presente en la memoria difiere del de la especie,
        la especie se considera inviable / descartada.
        """
        if not species.attributes:
            return True

        for attr, val in species.attributes.items():
            if attr in working_memory:
                if working_memory[attr] != val:
                    return False

        return True

    def _resolve_species(self, working_memory: Dict[str, Any], fired_rules: List[str] = None) -> Species | None:
        """
        Determina si hay una especie final identificada.
        Retorna la especie ÚNICAMENTE si cumple con el 100% de sus atributos o si una regla terminal
        confirmada la ha establecido sin competidoras con atributos pendientes.
        """
        viable_species = [
            s for s in self.species_list.values()
            if self._is_species_viable(s, working_memory)
        ]

        if not viable_species:
            return None

        species_stats = []
        for s in viable_species:
            attrs = dict(s.attributes) if s.attributes else {}
            matched = sum(1 for a, v in attrs.items() if working_memory.get(a) == v) if attrs else 0
            missing = [a for a in attrs.keys() if a not in working_memory] if attrs else []
            total = len(attrs)
            is_100_percent = (matched == total) and (total > 0)
            species_stats.append({
                "species": s,
                "matched": matched,
                "total": total,
                "missing": missing,
                "is_100": is_100_percent
            })

        species_stats.sort(
            key=lambda x: (x["is_100"], x["matched"], x["total"]),
            reverse=True
        )

        top_candidate = species_stats[0]

        # 1. Comprobar si hay una especie con 100% de sus atributos morfológicos cumplidos
        if top_candidate["is_100"]:
            has_competing_incomplete = any(
                stat["species"].id != top_candidate["species"].id and
                stat["matched"] >= top_candidate["matched"] and
                len(stat["missing"]) > 0
                for stat in species_stats
            )
            if not has_competing_incomplete:
                return top_candidate["species"]

        # 2. Comprobar si una regla terminal estableció `especie_detectada`
        rule_detected_id = working_memory.get("especie_detectada")
        if rule_detected_id and rule_detected_id in self.species_list:
            rule_species = self.species_list[rule_detected_id]
            if self._is_species_viable(rule_species, working_memory):
                rule_stat = next((st for st in species_stats if st["species"].id == rule_species.id), None)
                rule_matched = rule_stat["matched"] if rule_stat else 0

                has_competing_incomplete = any(
                    stat["species"].id != rule_species.id and
                    stat["matched"] >= rule_matched and
                    len(stat["missing"]) > 0
                    for stat in species_stats
                )
                if not has_competing_incomplete:
                    return rule_species

        return None

    def _get_next_recommended_fact(self, working_memory: Dict[str, Any], fired_rules: List[str]) -> str | None:
        """
        Devuelve el siguiente hecho que se debería preguntar al usuario.
        Verifica explícitamente que el hecho a buscar posea una pregunta configurada en self.facts_metadata (questions.json).
        """
        if self.facts_metadata:
            valid_facts = {
                q["fact"] for q in self.facts_metadata
                if q.get("fact") and q.get("fact") not in working_memory
            }
        else:
            valid_facts = None

        if valid_facts is not None and not valid_facts:
            return None

        if self.species_list:
            viable_species = [
                s for s in self.species_list.values()
                if self._is_species_viable(s, working_memory)
            ]

            if not viable_species:
                return None
        else:
            viable_species = []

        if viable_species:
            scored = []
            for s in viable_species:
                matched = sum(1 for a, v in s.attributes.items() if working_memory.get(a) == v)
                missing = [
                    a for a in s.attributes.keys()
                    if a not in working_memory and (valid_facts is None or a in valid_facts)
                ]
                scored.append({
                    "species": s,
                    "matched": matched,
                    "total": len(s.attributes),
                    "missing": missing
                })

            scored.sort(key=lambda x: (x["matched"], x["total"]), reverse=True)

            for item in scored:
                if item["missing"]:
                    return item["missing"][0]

        for rule in self.rules:
            if rule.id in fired_rules or not rule.antecedents:
                continue
            is_viable = True
            missing_facts = []
            for ant in rule.antecedents:
                if ant.fact in working_memory:
                    if not ant.evaluate(working_memory):
                        is_viable = False
                        break
                else:
                    if valid_facts is None or ant.fact in valid_facts:
                        missing_facts.append(ant.fact)
            if is_viable and missing_facts:
                return missing_facts[0]

        for q in self.facts_metadata:
            fact_name = q.get("fact")
            if fact_name and (valid_facts is None or fact_name in valid_facts):
                return fact_name

        return None
