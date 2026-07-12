import pytest
from app.domain.models import Rule, Antecedent, Consequent, Species
from app.domain.engine import ForwardChainingEngine

def test_engine_resolves_species_correctly():
    rules = [
        Rule(
            id="R1",
            name="Test Rule 1",
            description="",
            antecedents=[Antecedent(fact="numero_antenas", operator="==", value=2)],
            consequents=[Consequent(fact="subfilo", value="Crustacea")]
        ),
        Rule(
            id="R2",
            name="Test Rule 2",
            description="",
            antecedents=[
                Antecedent(fact="subfilo", operator="==", value="Crustacea"),
                Antecedent(fact="tipo_caparazon", operator="==", value="cefalotorax")
            ],
            consequents=[Consequent(fact="especie_detectada", value="Callinectes sapidus")]
        )
    ]
    species_list = [
        Species(id="Callinectes sapidus", name="Cangrejo Azul", description="", habitat="", image_url="")
    ]
    
    engine = ForwardChainingEngine(rules, species_list, [])
    
    initial_facts = {"numero_antenas": 2, "tipo_caparazon": "cefalotorax"}
    result = engine.infer(initial_facts)
    
    assert result.detected_species is not None
    assert result.detected_species.id == "Callinectes sapidus"
    assert "R1" in result.fired_rules
    assert "R2" in result.fired_rules

def test_engine_recommends_next_fact():
    rules = [
        Rule(
            id="R1",
            name="Test Rule 1",
            description="",
            antecedents=[Antecedent(fact="numero_antenas", operator="==", value=2)],
            consequents=[Consequent(fact="subfilo", value="Crustacea")]
        ),
        Rule(
            id="R2",
            name="Test Rule 2",
            description="",
            antecedents=[
                Antecedent(fact="subfilo", operator="==", value="Crustacea"),
                Antecedent(fact="tipo_caparazon", operator="==", value="cefalotorax")
            ],
            consequents=[Consequent(fact="especie_detectada", value="Callinectes sapidus")]
        )
    ]
    
    engine = ForwardChainingEngine(rules, [], [])
    
    initial_facts = {"numero_antenas": 2}
    result = engine.infer(initial_facts)
    
    assert result.detected_species is None
    assert "R1" in result.fired_rules
    assert "R2" not in result.fired_rules
    assert result.next_recommended_fact == "tipo_caparazon"

def test_engine_detects_porcellana_sayana():
    # Rule R18 from our JSON knowledge base: sin espínulas posteriores
    rules = [
        Rule(
            id="R18",
            name="Sin espínulas posteriores",
            description="Identifica Porcellana sayana.",
            antecedents=[Antecedent(fact="espinas_posteriores", operator="==", value=False)],
            consequents=[Consequent(fact="especie_detectada", value="Porcellana sayana")]
        )
    ]
    species_list = [
        Species(id="Porcellana sayana", name="Porcellana sayana", description="", habitat="", image_url="")
    ]
    engine = ForwardChainingEngine(rules, species_list, [])
    result = engine.infer({"espinas_posteriores": False})
    assert result.detected_species is not None
    assert result.detected_species.id == "Porcellana sayana"
    assert "R18" in result.fired_rules

def test_engine_tuberculado_rule():
    # Rule R12: Frente recta + carpo tuberculado -> Pachycheles ackleianus
    rules = [
        Rule(
            id="R12",
            name="Frente recta + carpo tuberculado",
            description="Identifica Pachycheles ackleianus.",
            antecedents=[
                Antecedent(fact="forma_frente_carpo", operator="==", value="recta"),
                Antecedent(fact="superficie_quelipedo", operator="==", value="tuberculado")
            ],
            consequents=[Consequent(fact="especie_detectada", value="Pachycheles ackleianus")]
        )
    ]
    species_list = [
        Species(id="Pachycheles ackleianus", name="Pachycheles ackleianus", description="", habitat="", image_url="")
    ]
    engine = ForwardChainingEngine(rules, species_list, [])
    result = engine.infer({"forma_frente_carpo": "recta", "superficie_quelipedo": "tuberculado"})
    assert result.detected_species is not None
    assert result.detected_species.id == "Pachycheles ackleianus"
    assert "R12" in result.fired_rules
