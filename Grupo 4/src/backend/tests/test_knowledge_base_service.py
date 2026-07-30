import pytest
from app.ports.repositories import BaseKnowledgeRepository
from app.domain.models import Species, Rule, Antecedent, Consequent
from app.schemas.species_schemas import CreateSpeciesRequest
from app.services.knowledge_base_service import KnowledgeBaseService


class InMemoryRepository(BaseKnowledgeRepository):
    def __init__(self):
        self.species_list = [
            Species(
                id="Petrolisthes_armatus",
                name="Petrolisthes armatus",
                description="Especie de prueba",
                habitat="Rocoso",
                field_characteristics=["Espinas carpo"],
                image_url="/assets/petrolisthes_armatus.jpg",
                attributes={"segmento_antenal": "corto", "numero_antenas": 2},
                taxonomy={"genus": "Petrolisthes", "family": "Porcellanidae"}
            )
        ]
        self.facts_metadata = [
            {
                "fact": "segmento_antenal",
                "question": "¿Cómo es el segmento basal de la antena?",
                "options": [
                    {"label": "Corto", "value": "corto"},
                    {"label": "Largo", "value": "largo"},
                    {"label": "No aplica", "value": "no_aplica"}
                ],
                "category": "Antenas"
            }
        ]
        self.rules = [
            Rule(
                id="R_Petrolisthes_armatus",
                name="Regla armatus",
                description="",
                antecedents=[Antecedent(fact="segmento_antenal", operator="==", value="corto")],
                consequents=[Consequent(fact="especie_detectada", value="Petrolisthes_armatus")]
            )
        ]

    def get_species(self):
        return list(self.species_list)

    def get_facts_metadata(self):
        return list(self.facts_metadata)

    def get_rules(self):
        return list(self.rules)

    def save_species(self, species_list):
        self.species_list = species_list

    def save_facts_metadata(self, metadata):
        self.facts_metadata = metadata

    def save_rules(self, rules):
        self.rules = rules


def test_add_species_case_a_new_fact_creates_question():
    repo = InMemoryRepository()
    service = KnowledgeBaseService(repository=repo)

    request = CreateSpeciesRequest(
        id="Porcellana_sayana",
        name="Porcellana sayana",
        description="Especie con nuevo atributo",
        habitat="Fondo blando",
        genus="Porcellana",
        attributes={
            "numero_antenas": 2,
            "color_patas": "rojo"
        },
        fact_labels={"color_patas": "¿De qué color son las patas del ejemplar?"},
        option_labels={"color_patas": {"rojo": "Patas de color rojo intenso"}}
    )

    response = service.add_species(request)

    assert response.success is True
    assert "color_patas" in response.added_questions

    metadata = repo.get_facts_metadata()
    color_q = next((q for q in metadata if q["fact"] == "color_patas"), None)
    assert color_q is not None
    assert color_q["question"] == "¿De qué color son las patas del ejemplar?"
    assert len(color_q["options"]) == 2
    option_values = [opt["value"] for opt in color_q["options"]]
    assert "rojo" in option_values
    assert "no_aplica" in option_values


def test_add_species_case_b_existing_fact_new_option():
    repo = InMemoryRepository()
    service = KnowledgeBaseService(repository=repo)

    request = CreateSpeciesRequest(
        id="Petrolisthes_galathinus",
        name="Petrolisthes galathinus",
        description="Especie con nuevo valor para hecho existente",
        habitat="Coralino",
        genus="Petrolisthes",
        attributes={
            "numero_antenas": 2,
            "segmento_antenal": "medio"
        },
        option_labels={"segmento_antenal": {"medio": "Segmento de longitud media"}}
    )

    response = service.add_species(request)

    assert response.success is True
    assert "segmento_antenal:medio" in response.added_questions

    metadata = repo.get_facts_metadata()
    segment_q = next((q for q in metadata if q["fact"] == "segmento_antenal"), None)
    assert segment_q is not None
    values = [opt["value"] for opt in segment_q["options"]]
    assert "medio" in values
    assert "no_aplica" in values
    assert len(segment_q["options"]) == 4


def test_add_species_rule_generation_genus_taxonomy_and_clean_attributes():
    repo = InMemoryRepository()
    service = KnowledgeBaseService(repository=repo)

    request = CreateSpeciesRequest(
        id="Petrolisthes_robustus",
        name="Petrolisthes robustus",
        genus="Petrolisthes",
        attributes={
            "genus": "Petrolisthes",
            "espina_carpo": True
        }
    )

    response = service.add_species(request)

    assert response.success is True
    assert "R_Petrolisthes_robustus" in response.added_rules
    assert "R_INT_espina_carpo_True" in response.added_rules

    created_species = response.species
    assert "genus" not in created_species.attributes
    assert created_species.attributes["numero_antenas"] == 2
    assert "espina_carpo" in created_species.attributes

    assert created_species.taxonomy["kingdom"] == "Animalia"
    assert created_species.taxonomy["phylum"] == "Arthropoda"
    assert created_species.taxonomy["subphylum"] == "Crustacea"
    assert created_species.taxonomy["class"] == "Malacostraca"
    assert created_species.taxonomy["order"] == "Decapoda"
    assert created_species.taxonomy["infraorder"] == "Anomura"
    assert created_species.taxonomy["family"] == "Porcellanidae"
    assert created_species.taxonomy["genus"] == "Petrolisthes"
    assert created_species.taxonomy["species"] == "robustus"

    rules = repo.get_rules()
    rule = next((r for r in rules if r.id == "R_Petrolisthes_robustus"), None)
    assert rule is not None

    facts_in_rule = [a.fact for a in rule.antecedents]
    assert "genus" in facts_in_rule
    assert "hecho_int_espina_carpo_True" in facts_in_rule
    assert rule.consequents[0].fact == "especie_detectada"
    assert rule.consequents[0].value == "Petrolisthes_robustus"


def test_add_species_exact_duplicate_attributes_rejected():
    repo = InMemoryRepository()
    service = KnowledgeBaseService(repository=repo)

    # Intentar agregar una especie con exactamente los mismos atributos que Petrolisthes_armatus
    request = CreateSpeciesRequest(
        id="Petrolisthes_duplicado",
        name="Petrolisthes duplicado",
        description="Especie con atributos duplicados",
        habitat="Rocoso",
        genus="Petrolisthes",
        attributes={
            "segmento_antenal": "corto",
            "numero_antenas": 2
        }
    )

    response = service.add_species(request)

    assert response.success is False
    assert "No se puede agregar la nueva especie porque ya existe otra igual" in response.message
    assert "Petrolisthes armatus" in response.message
    assert "segmento antenal: corto" in response.message
