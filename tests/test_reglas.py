import pytest
from src.base_conocimiento import BaseConocimiento

def test_cargar_base_conocimiento():
    """Valida que la base de conocimientos se cargue sin errores."""
    bc = BaseConocimiento()
    assert bc.especies is not None
    assert len(bc.especies) > 0

def test_estructura_especies():
    """Valida que todas las especies registradas posean los campos taxonómicos obligatorios."""
    bc = BaseConocimiento()
    especies = bc.listar_especies()
    
    campos_requeridos = ["id", "nombre_cientifico", "nombre_comun", "familia"]
    for esp in especies:
        for campo in campos_requeridos:
            assert campo in esp, f"Falta el campo obligatorio '{campo}' en la especie {esp.get('id')}"

def test_sintetizar_regla_dinamica():
    """Valida que una nueva especie sintetice su regla dicotómica y el motor la identifique."""
    from src.generador_reglas import sintetizar_regla_especie
    from src.motor_inferencia import MotorInferencia
    
    nueva_esp = {
        "id": "acropora_dinamica_test",
        "nombre_cientifico": "Acropora dinamica_test",
        "nombre_comun": "Coral Dinámico",
        "familia": "Acroporidae",
        "caracteristicas": {
            "tiene_coralitos": True,
            "forma": "ramificada_abanico",
            "color": "marrón"
        }
    }
    sintetizar_regla_especie(nueva_esp)
    
    motor = MotorInferencia()
    respuestas = {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "toda", "p10": "cilindricas", "p11": "abanico"}
    res = motor.ejecutar(respuestas)
    assert res["success"] is True
