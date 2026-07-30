from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.domain.models import Species


class CreateSpeciesRequest(BaseModel):
    """
    Payload de entrada para registrar una nueva especie y actualizar la base de conocimientos.
    """
    id: str = Field(..., description="ID único de la especie (ej. Petrolisthes_armatus)")
    name: str = Field(..., description="Nombre científico o común (ej. Petrolisthes armatus)")
    description: str = Field("", description="Descripción taxonómica de la especie")
    habitat: str = Field("", description="Hábitat natural")
    field_characteristics: List[str] = Field(default_factory=list, description="Características de campo")
    image_url: str = Field("", description="URL o ruta de la imagen representativa")
    image_data: Optional[str] = Field(None, description="Cadena Base64 de la imagen para guardado local en assets")
    image_filename: Optional[str] = Field(None, description="Nombre de archivo original o extensión de la imagen")
    genus: Optional[str] = Field(None, description="Género taxonómico al que pertenece")
    taxonomy: Dict[str, str] = Field(default_factory=dict, description="Diccionario taxonómico opcional")
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Atributos morfológicos de la especie (ej. {'numero_antenas': 2, 'segmento_antenal': 'corto'})"
    )
    fact_labels: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Etiquetas legibles para preguntas de nuevos hechos (ej. {'color_patas': '¿De qué color son las patas?'})"
    )
    option_labels: Optional[Dict[str, Dict[str, str]]] = Field(
        default_factory=dict,
        description="Etiquetas legibles para valores de opciones por hecho (ej. {'color_patas': {'rojo': 'Patas rojas'}})"
    )


class CreateSpeciesResponse(BaseModel):
    """
    Respuesta del servicio al crear una especie.
    """
    success: bool
    message: str
    species: Species
    added_questions: List[str] = Field(default_factory=list)
    added_rules: List[str] = Field(default_factory=list)
