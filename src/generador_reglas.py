# src/generador_reglas.py
"""
Sintetizador Dinámico de Reglas para el Motor Dicotómico de CoraAI.
Permite registrar y sintetizar reglas dicotómicas para nuevas especies agregadas al sistema.
"""

import json
import os
from pathlib import Path

def _get_ruta_reglas_dinamicas():
    root_dir = Path(__file__).resolve().parent.parent
    return root_dir / "data" / "reglas_dinamicas.json"

def cargar_reglas_dinamicas() -> dict:
    """Carga el registro de reglas dicotómicas dinámicas desde data/reglas_dinamicas.json."""
    ruta = _get_ruta_reglas_dinamicas()
    if not ruta.exists():
        return {}
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar reglas dinámicas: {e}")
        return {}

def sintetizar_regla_especie(especie_dict: dict) -> dict:
    """
    Toma los datos de una nueva especie, convierte sus atributos morfológicos en
    respuestas del cuestionario y la guarda en data/reglas_dinamicas.json.
    """
    try:
        from src.generador_dataset import caracteristicas_a_respuestas
    except ImportError:
        try:
            from .generador_dataset import caracteristicas_a_respuestas
        except ImportError:
            return {}

    esp_id = especie_dict.get("id")
    if not esp_id:
        esp_id = especie_dict.get("nombre_cientifico", "").strip().lower().replace(" ", "_")

    caract = especie_dict.get("caracteristicas", {})
    respuestas_mapeadas = caracteristicas_a_respuestas(esp_id, caract)

    reglas = cargar_reglas_dinamicas()

    reglas[esp_id] = {
        "id": esp_id,
        "nombre_cientifico": especie_dict.get("nombre_cientifico", ""),
        "nombre_comun": especie_dict.get("nombre_comun", ""),
        "familia": especie_dict.get("familia", ""),
        "orden": especie_dict.get("orden", "Scleractinia"),
        "respuestas": respuestas_mapeadas
    }

    ruta = _get_ruta_reglas_dinamicas()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reglas, f, ensure_ascii=False, indent=2)

    return reglas[esp_id]
