import pytest
from src.motor_inferencia import MotorInferencia

@pytest.fixture
def motor():
    return MotorInferencia()

def test_clasificacion_millepora_alcicornis(motor):
    # p1=no (sin coralitos), p2=incrustante -> Millepora alcicornis
    respuestas = {"p1": "no", "p2": "incrustante"}
    resultado = motor.ejecutar(respuestas)
    assert resultado["success"] is True
    assert resultado["especie"] == "Millepora alcicornis"
    assert resultado["familia"] == "Milleporidae"

def test_clasificacion_millepora_complanata(motor):
    # p1=no, p2=aplanado, p3=vertical -> Millepora complanata
    respuestas = {"p1": "no", "p2": "aplanado", "p3": "vertical"}
    resultado = motor.ejecutar(respuestas)
    assert resultado["success"] is True
    assert resultado["especie"] == "Millepora complanata"

def test_clasificacion_incompleta_pide_pregunta(motor):
    # Sin respuestas acumuladas debe solicitar p1
    resultado = motor.ejecutar({})
    assert resultado["estado"] == "pregunta"
    assert resultado["pregunta_id"] == "p1"

def test_clasificacion_paso_dos_pide_pregunta(motor):
    # Con p1=no, debe solicitar p2
    resultado = motor.ejecutar({"p1": "no"})
    assert resultado["estado"] == "pregunta"
    assert resultado["pregunta_id"] == "p2"
