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

def test_engine_skips_recommended_fact_when_no_aplica():
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
    
    initial_facts = {"numero_antenas": 2, "tipo_caparazon": "no_aplica"}
    result = engine.infer(initial_facts)
    
    assert result.working_memory["tipo_caparazon"] == "no_aplica"
    assert result.next_recommended_fact != "tipo_caparazon"

def test_engine_detects_porcellana_sayana():
    rules = [
        Rule(
            id="R_sayana",
            name="Identificación de porcellana sayana",
            description="",
            antecedents=[
                Antecedent(fact="genus", operator="==", value="Porcellana"),
                Antecedent(fact="margin_carapace", operator="==", value="spined")
            ],
            consequents=[Consequent(fact="especie_detectada", value="porcellana_sayana")]
        )
    ]
    species_list = [
        Species(
            id="porcellana_sayana",
            name="porcellana sayana",
            attributes={"genus": "Porcellana", "margin_carapace": "spined", "numero_antenas": 2}
        )
    ]
    engine = ForwardChainingEngine(rules, species_list, [])
    
    working_memory = {"genus": "Porcellana", "margin_carapace": "spined", "numero_antenas": 2}
    result = engine.infer(working_memory)
    
    assert result.detected_species is not None
    assert result.detected_species.id == "porcellana_sayana"

def test_engine_tuberculado_rule():
    rules = [
        Rule(
            id="R_tub",
            name="Regla Tuberculado",
            description="",
            antecedents=[
                Antecedent(fact="superficie_cheliped", operator="==", value="tuberculado")
            ],
            consequents=[Consequent(fact="especie_detectada", value="especie_tuberculada")]
        )
    ]
    species_list = [
        Species(
            id="especie_tuberculada",
            name="Especie Tuberculada",
            attributes={"superficie_cheliped": "tuberculado", "numero_antenas": 2}
        )
    ]
    engine = ForwardChainingEngine(rules, species_list, [])
    
    working_memory = {"superficie_cheliped": "tuberculado", "numero_antenas": 2}
    result = engine.infer(working_memory)
    
    assert result.detected_species is not None
    assert result.detected_species.id == "especie_tuberculada"

def test_engine_fallback_when_no_species_reaches_100_percent():
    rules = []
    species_list = [
        Species(
            id="Pet_1",
            name="Petrolisthes 1",
            description="Especie 1",
            attributes={"segmento": "corto", "paredes": "enteras"}
        ),
        Species(
            id="Pet_2",
            name="Petrolisthes 2",
            description="Especie 2",
            attributes={"segmento": "corto", "paredes": "incompletas"}
        )
    ]
    engine = ForwardChainingEngine(rules, species_list, [])
    
    # Usuario respondió segmento = corto, pero paredes = no_aplica
    working_memory = {"numero_antenas": 2, "segmento": "corto", "paredes": "no_aplica"}
    result = engine.infer(working_memory)
    
    # Al estar "paredes" marcada como no_aplica, Pet_1 y Pet_2 difieren en paredes y quedan inviables
    assert result.detected_species is None
    assert result.next_recommended_fact is None
