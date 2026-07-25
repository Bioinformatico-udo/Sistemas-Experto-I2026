from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class InferenciaRequest(BaseModel):
    respuestas: Dict[str, str] = Field(default_factory=dict, description="Diccionario de respuestas acumuladas id_pregunta -> valor_opcion")

class OpcionPregunta(BaseModel):
    label: str
    valor: str
    principal: Optional[bool] = False

class PreguntaResponse(BaseModel):
    id: str
    texto: str
    descripcion: str
    opciones: List[OpcionPregunta]

class InferenciaResultadoResponse(BaseModel):
    estado: str  # "pregunta" o "resultado"
    pregunta_id: Optional[str] = None
    pregunta_detalle: Optional[PreguntaResponse] = None
    success: Optional[bool] = None
    especie: Optional[str] = None
    nombre_comun: Optional[str] = None
    familia: Optional[str] = None
    orden: Optional[str] = None
    mensaje: Optional[str] = None
    sugerencia: Optional[str] = None

class DiagnosticoIARequest(BaseModel):
    texto: str = Field(..., min_length=3, description="Descripción textual en lenguaje natural del coral observado")

class EspecieCandidata(BaseModel):
    especie: str
    nombre_comun: str
    familia: str
    orden: Optional[str] = "Scleractinia"
    score_final: float
    similitud_ponderada: float
    coincidencia_arbol: float
    coincidencias_clave: List[str] = []

class DiagnosticoIAResponse(BaseModel):
    exito: bool
    metodo: str
    especie_ganadora: Dict[str, Any]
    top_candidatos: List[EspecieCandidata]
    desglose_explicativo: Dict[str, Any]
    respuestas_deducidas: Dict[str, str]

class EspecieCreateRequest(BaseModel):
    nombre_cientifico: str = Field(..., min_length=3, description="Nombre científico en latín")
    nombre_comun: str = Field(..., min_length=2, description="Nombre común o vernáculo")
    familia: str = Field(..., description="Familia taxonómica")
    orden: Optional[str] = "Scleractinia"
    tipo: Optional[str] = "Escleractinio"
    descripcion: Optional[str] = ""
    habitat: Optional[str] = "Parque Nacional Archipiélago de Los Roques"
    caracteristicas: Optional[Dict[str, Any]] = Field(default_factory=dict)
    imagen_base64: Optional[str] = Field(None, description="Imagen opcional codificada en Base64")
