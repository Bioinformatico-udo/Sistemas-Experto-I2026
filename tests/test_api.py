import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "ia_model_loaded" in data

def test_obtener_preguntas():
    response = client.get("/api/preguntas")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == "p1"

def test_navegar_inferencia_paso_inicio():
    response = client.post("/api/inferencia/paso", json={"respuestas": {}})
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "pregunta"
    assert data["pregunta_id"] == "p1"
    assert data["pregunta_detalle"]["id"] == "p1"

def test_navegar_inferencia_paso_completo():
    # p1=no (hidrocoral), p2=incrustante -> Millepora alcicornis
    response = client.post("/api/inferencia/paso", json={"respuestas": {"p1": "no", "p2": "incrustante"}})
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "resultado"
    assert data["success"] is True
    assert data["especie"] == "Millepora alcicornis"

def test_diagnostico_ia():
    response = client.post("/api/ia/diagnostico", json={"texto": "Coral con ramas de color amarillo marrón en zona somera"})
    assert response.status_code == 200
    data = response.json()
    assert data["exito"] is True
    assert "especie_ganadora" in data
    assert isinstance(data["top_candidatos"], list)

def test_listar_especies():
    response = client.get("/api/especies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_obtener_guia():
    response = client.get("/api/guia")
    assert response.status_code == 200
    data = response.json()
    assert "titulo" in data
    assert "pasos_fundamentales" in data

def test_crear_especie():
    payload = {
        "nombre_cientifico": "Acropora test_species",
        "nombre_comun": "Coral Test",
        "familia": "Acroporidae",
        "orden": "Scleractinia",
        "tipo": "Escleractinio",
        "descripcion": "Especie de prueba unitaria",
        "habitat": "Los Roques Test",
        "caracteristicas": {"color": "marrón", "forma": "ramificada"}
    }
    response = client.post("/api/especies", json=payload)
    # Si ya existía de una corrida previa o es nueva
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.json()
        assert data["success"] is True
        assert data["especie"]["id"] == "acropora_test_species"

def test_crear_especie_duplicada():
    payload = {
        "nombre_cientifico": "Acropora palmata",
        "nombre_comun": "Coral Cuerno de Alce Duplicado",
        "familia": "Acroporidae"
    }
    response = client.post("/api/especies", json=payload)
    assert response.status_code == 400
    assert "ya se encuentra registrada" in response.json()["detail"]

def test_insertar_y_verificar_acceso_dicotomico():
    """Crea una nueva especie por la API y verifica que el motor dicotómico responda con éxito."""
    payload = {
        "nombre_cientifico": "Acropora verificacion_dicotomica",
        "nombre_comun": "Coral de Prueba Dicotómica",
        "familia": "Acroporidae",
        "caracteristicas": {
            "tiene_coralitos": True,
            "forma": "ramificada_abanico",
            "color": "marrón"
        }
    }
    res_crear = client.post("/api/especies", json=payload)
    assert res_crear.status_code in [200, 400]

    # Ejecutar inferencia en el motor dicotómico con las respuestas de la especie
    respuestas = {
        "p1": "s",
        "p4": "colonial",
        "p6": "ramificado",
        "p7": "toda",
        "p10": "cilindricas",
        "p11": "abanico"
    }
    res_inferencia = client.post("/api/inferencia/paso", json={"respuestas": respuestas})
    assert res_inferencia.status_code == 200
    data = res_inferencia.json()
    assert data["estado"] == "resultado"
    assert data["success"] is True
    assert "Acropora" in data["especie"]
