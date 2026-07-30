import pytest
from app.domain.models import Rule, Antecedent, Consequent, Species
from app.domain.engine import ForwardChainingEngine


def test_subset_does_not_interrupt_when_superset_is_viable():
    """
    Especie A (Simple) requiere: {F1: "si", F2: "si"}
    Especie B (Superset) requiere: {F1: "si", F2: "si", F3: "rojo"}

    Dado {F1: "si", F2: "si"}, la regla de Especie A dispara.
    Sin embargo, como Especie B es viable y falta F3 por responder,
    el motor debe diferir la resolución de Especie A (detected_species = None)
    y recomendar F3 como siguiente pregunta.
    """
    rules = [
        Rule(
            id="R_ESPECIE_A",
            name="Identificación Especie A (Subconjunto)",
            description="",
            antecedents=[
                Antecedent(fact="forma_caparazon", operator="==", value="ovalado"),
                Antecedent(fact="numero_patas", operator="==", value="10")
            ],
            consequents=[Consequent(fact="especie_detectada", value="Especie_A")]
        ),
        Rule(
            id="R_ESPECIE_B",
            name="Identificación Especie B (Superconjunto)",
            description="",
            antecedents=[
                Antecedent(fact="forma_caparazon", operator="==", value="ovalado"),
                Antecedent(fact="numero_patas", operator="==", value="10"),
                Antecedent(fact="espinas_dorsales", operator="==", value="presentes")  # Hecho diferenciador
            ],
            consequents=[Consequent(fact="especie_detectada", value="Especie_B")]
        )
    ]

    species_list = [
        Species(id="Especie_A", name="Especie A", description="", habitat="", image_url="", attributes={"forma_caparazon": "ovalado", "numero_patas": "10"}),
        Species(id="Especie_B", name="Especie B", description="", habitat="", image_url="", attributes={"forma_caparazon": "ovalado", "numero_patas": "10", "espinas_dorsales": "presentes"})
    ]

    engine = ForwardChainingEngine(rules, species_list, [])

    # Memoria parcial que satisface Especie A pero aún no ha respondido espinas_dorsales
    working_memory = {
        "numero_antenas": 2,
        "forma_caparazon": "ovalado",
        "numero_patas": "10"
    }

    result = engine.infer(working_memory)

    # 1. Verificar que NO declara Especie_A prematuramente
    assert result.detected_species is None
    # 2. Verificar que recomienda el hecho diferenciador faltante de Especie B
    assert result.next_recommended_fact == "espinas_dorsales"


def test_superset_confirmed_when_differentiating_fact_matches():
    rules = [
        Rule(
            id="R_ESPECIE_A",
            name="Identificación Especie A",
            description="",
            antecedents=[
                Antecedent(fact="forma_caparazon", operator="==", value="ovalado"),
                Antecedent(fact="numero_patas", operator="==", value="10")
            ],
            consequents=[Consequent(fact="especie_detectada", value="Especie_A")]
        ),
        Rule(
            id="R_ESPECIE_B",
            name="Identificación Especie B",
            description="",
            antecedents=[
                Antecedent(fact="forma_caparazon", operator="==", value="ovalado"),
                Antecedent(fact="numero_patas", operator="==", value="10"),
                Antecedent(fact="espinas_dorsales", operator="==", value="presentes")
            ],
            consequents=[Consequent(fact="especie_detectada", value="Especie_B")]
        )
    ]

    species_list = [
        Species(id="Especie_A", name="Especie A", description="", habitat="", image_url=""),
        Species(id="Especie_B", name="Especie B", description="", habitat="", image_url="")
    ]

    engine = ForwardChainingEngine(rules, species_list, [])

    # Al responder espinas_dorsales = "presentes", se confirma Especie B
    working_memory = {
        "numero_antenas": 2,
        "forma_caparazon": "ovalado",
        "numero_patas": "10",
        "espinas_dorsales": "presentes"
    }

    result = engine.infer(working_memory)

    assert result.detected_species is not None
    assert result.detected_species.id == "Especie_B"


def test_subset_resolved_when_superset_becomes_inviable():
    rules = [
        Rule(
            id="R_ESPECIE_A",
            name="Identificación Especie A",
            description="",
            antecedents=[
                Antecedent(fact="forma_caparazon", operator="==", value="ovalado"),
                Antecedent(fact="numero_patas", operator="==", value="10")
            ],
            consequents=[Consequent(fact="especie_detectada", value="Especie_A")]
        ),
        Rule(
            id="R_ESPECIE_B",
            name="Identificación Especie B",
            description="",
            antecedents=[
                Antecedent(fact="forma_caparazon", operator="==", value="ovalado"),
                Antecedent(fact="numero_patas", operator="==", value="10"),
                Antecedent(fact="espinas_dorsales", operator="==", value="presentes")
            ],
            consequents=[Consequent(fact="especie_detectada", value="Especie_B")]
        )
    ]

    species_list = [
        Species(id="Especie_A", name="Especie A", description="", habitat="", image_url=""),
        Species(id="Especie_B", name="Especie B", description="", habitat="", image_url="")
    ]

    engine = ForwardChainingEngine(rules, species_list, [])

    # Si el usuario responde espinas_dorsales = "ausentes", Especie B ya no es viable, por lo que se confirma Especie A
    working_memory = {
        "numero_antenas": 2,
        "forma_caparazon": "ovalado",
        "numero_patas": "10",
        "espinas_dorsales": "ausentes"
    }

    result = engine.infer(working_memory)

    assert result.detected_species is not None
    assert result.detected_species.id == "Especie_A"
