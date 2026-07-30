import base64
import os
from typing import List, Dict, Any, Optional
from app.domain.models import Rule, Antecedent, Consequent, Species
from app.ports.repositories import BaseKnowledgeRepository
from app.schemas.species_schemas import CreateSpeciesRequest, CreateSpeciesResponse


class KnowledgeBaseService:
    """
    Servicio de capa de aplicación para gestionar y actualizar la Base de Conocimientos:
    - Registro de nuevas especies con sus metadatos e imagen local en assets.
    - Sincronización dinámica de preguntas (questions.json / rules.json) incluyendo la opción 'No aplica'.
    - Generación de reglas intermedias ÚNICAMENTE al agregar una nueva opción de valor a un atributo (excluyendo 'no_aplica').
    """

    def __init__(self, repository: BaseKnowledgeRepository):
        self.repository = repository

    def add_species(self, request: CreateSpeciesRequest) -> CreateSpeciesResponse:
        added_questions: List[str] = []
        added_rules: List[str] = []

        # 1. Cargar datos actuales
        existing_species = self.repository.get_species()
        existing_questions = self.repository.get_facts_metadata()
        existing_rules = self.repository.get_rules()

        # 2. Procesar Especie & Guardado de Imagen
        genus_value = request.genus or request.attributes.get("genus") or request.taxonomy.get("genus") or ""

        species_epithet = ""
        if request.name:
            parts = request.name.strip().split()
            species_epithet = parts[1] if len(parts) >= 2 else parts[0]
        elif "_" in request.id:
            species_epithet = request.id.split("_", 1)[1]

        # Estructura estandarizada de taxonomía para Porcellanidae
        taxonomy = {
            "kingdom": "Animalia",
            "phylum": "Arthropoda",
            "subphylum": "Crustacea",
            "class": "Malacostraca",
            "order": "Decapoda",
            "infraorder": "Anomura",
            "family": "Porcellanidae",
            "genus": genus_value,
            "species": species_epithet,
        }

        # Excluir 'genus' del diccionario de atributos y asignar automáticamente 'numero_antenas' = 2
        clean_attributes = {k: v for k, v in request.attributes.items() if k != "genus"} if request.attributes else {}
        clean_attributes["numero_antenas"] = 2

        image_url = request.image_url
        if request.image_data:
            try:
                ext = "jpg"
                if request.image_filename and "." in request.image_filename:
                    ext = request.image_filename.split(".")[-1].lower()
                elif "data:image/" in request.image_data:
                    mime = request.image_data.split(";")[0].replace("data:image/", "")
                    if mime in ["jpeg", "jpg", "png", "webp", "svg"]:
                        ext = "jpg" if mime == "jpeg" else mime

                id_lowercase = request.id.lower()
                filename = f"{id_lowercase}.{ext}"

                # Ruta a src/frontend/src/assets/
                current_file_dir = os.path.dirname(os.path.abspath(__file__))
                backend_app_dir = os.path.dirname(current_file_dir)
                backend_dir = os.path.dirname(backend_app_dir)
                src_dir = os.path.dirname(backend_dir)
                assets_dir = os.path.join(src_dir, "frontend", "src", "assets")

                os.makedirs(assets_dir, exist_ok=True)
                target_path = os.path.join(assets_dir, filename)

                encoded = request.image_data.split(",", 1)[1] if "," in request.image_data else request.image_data
                data = base64.b64decode(encoded)
                with open(target_path, "wb") as f:
                    f.write(data)

                image_url = f"/assets/{filename}"
            except Exception as exc:
                print(f"Advertencia: No se pudo guardar la imagen local en assets: {exc}")

        new_species = Species(
            id=request.id,
            name=request.name,
            description=request.description,
            habitat=request.habitat,
            field_characteristics=request.field_characteristics,
            image_url=image_url,
            attributes=clean_attributes,
            taxonomy=taxonomy,
        )

        # Actualizar o agregar especie en el listado
        species_dict = {s.id: s for s in existing_species}
        species_dict[new_species.id] = new_species
        updated_species = list(species_dict.values())

        # 3. Sincronización Dinámica de Preguntas & Detección de Nuevas Opciones de Valor
        questions_by_fact: Dict[str, Dict[str, Any]] = {
            q["fact"]: q for q in existing_questions if "fact" in q
        }

        fact_labels = request.fact_labels or {}
        option_labels = request.option_labels or {}
        no_aplica_opt = {"label": "No aplica", "value": "no_aplica"}

        newly_added_fact_values: List[tuple] = []  # Guardar (fact_name, fact_value) verdaderamente nuevos

        for fact_name, fact_value in clean_attributes.items():
            if fact_name in ("genus", "numero_antenas") or str(fact_value) == "no_aplica":
                continue

            opt_label = (
                option_labels.get(fact_name, {}).get(str(fact_value))
                or str(fact_value).capitalize()
            )

            if fact_name not in questions_by_fact:
                # CASO A: Pregunta y atributo completamente nuevo
                q_text = fact_labels.get(
                    fact_name,
                    f"¿Cuál es el estado de {fact_name.replace('_', ' ')}?"
                )
                new_q = {
                    "fact": fact_name,
                    "question": q_text,
                    "options": [
                        {"label": opt_label, "value": fact_value},
                        dict(no_aplica_opt)
                    ],
                    "category": "Morfología Específica"
                }
                questions_by_fact[fact_name] = new_q
                added_questions.append(fact_name)
                newly_added_fact_values.append((fact_name, fact_value))
            else:
                # CASO B: Pregunta existente -> Comprobar si el valor específico es una nueva opción
                q = questions_by_fact[fact_name]
                existing_values = [opt["value"] for opt in q.get("options", [])]
                if fact_value not in existing_values:
                    q.setdefault("options", []).append({
                        "label": opt_label,
                        "value": fact_value
                    })
                    added_questions.append(f"{fact_name}:{fact_value}")
                    newly_added_fact_values.append((fact_name, fact_value))

        # Garantizar que TODAS las preguntas tengan la opción 'No aplica'
        for q in questions_by_fact.values():
            opts = q.setdefault("options", [])
            if not any(opt.get("value") == "no_aplica" for opt in opts):
                opts.append(dict(no_aplica_opt))

        updated_questions = list(questions_by_fact.values())

        # 4. Generación y Vinculación de Reglas (rules.json)
        rules_dict = {r.id: r for r in existing_rules}
        terminal_antecedents: List[Antecedent] = []

        if genus_value:
            terminal_antecedents.append(
                Antecedent(fact="genus", operator="==", value=genus_value)
            )

        for fact_name, fact_value in clean_attributes.items():
            if fact_name in ("genus", "numero_antenas"):
                continue

            # Crear regla intermedia ÚNICAMENTE si es una NUEVA opción de valor agregada y != "no_aplica"
            if (fact_name, fact_value) in newly_added_fact_values and str(fact_value) != "no_aplica":
                int_rule_id = f"R_INT_{fact_name}_{fact_value}"
                group_fact = f"grupo_{fact_name}"

                if int_rule_id not in rules_dict:
                    int_rule = Rule(
                        id=int_rule_id,
                        name=f"Regla intermedia {fact_name.replace('_', ' ')} = {fact_value}",
                        description=f"Inferencia intermedia para agrupación de {fact_name} con nueva opción {fact_value}",
                        antecedents=[
                            Antecedent(fact=fact_name, operator="==", value=fact_value)
                        ],
                        consequents=[
                            Consequent(fact=group_fact, value=str(fact_value))
                        ]
                    )
                    rules_dict[int_rule_id] = int_rule
                    added_rules.append(int_rule_id)

                terminal_antecedents.append(
                    Antecedent(fact=group_fact, operator="==", value=str(fact_value))
                )
            else:
                # Si el hecho/valor ya existía previamente, usar directamente el antecedente crudo
                terminal_antecedents.append(
                    Antecedent(fact=fact_name, operator="==", value=fact_value)
                )

        terminal_antecedents.append(
            Antecedent(fact="numero_antenas", operator="==", value=2)
        )

        consequents = [Consequent(fact="especie_detectada", value=request.id)]
        rule_id = f"R_{request.id}"

        terminal_rule = Rule(
            id=rule_id,
            name=f"Identificación de {request.name}",
            description=f"Regla de inferencia terminal para {request.name}",
            antecedents=terminal_antecedents,
            consequents=consequents
        )

        rules_dict[terminal_rule.id] = terminal_rule
        added_rules.append(terminal_rule.id)

        updated_rules = list(rules_dict.values())

        # 5. Persistencia Atómica en Repositorio
        self.repository.save_species(updated_species)
        self.repository.save_facts_metadata(updated_questions)
        self.repository.save_rules(updated_rules)

        return CreateSpeciesResponse(
            success=True,
            message=f"Especie '{request.name}' ({request.id}) agregada y base de conocimiento actualizada exitosamente.",
            species=new_species,
            added_questions=added_questions,
            added_rules=added_rules,
        )
