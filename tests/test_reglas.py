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
