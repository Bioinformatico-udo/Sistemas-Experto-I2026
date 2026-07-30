import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Asegurar que el directorio raíz esté en sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.motor_inferencia import MotorInferencia
from src.preguntas import generar_preguntas
from src.modelo_hibrido import PredictorCorales
from src.motor_ponderacion import PonderadorCaracteristicas
from src.base_conocimiento import BaseConocimiento
from src.api.schemas import (
    InferenciaRequest,
    InferenciaResultadoResponse,
    PreguntaResponse,
    DiagnosticoIARequest,
    DiagnosticoIAResponse,
    EspecieCandidata,
    EspecieCreateRequest
)

app = FastAPI(
    title="Coral Expert System API - Los Roques",
    description="API REST para el Sistema Experto Híbrido de Identificación de Corales del Parque Nacional Archipiélago de Los Roques",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde el frontend en React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancias globales de servicios
motor_inferencia = MotorInferencia()
predictor_corales = PredictorCorales()
base_conocimiento = BaseConocimiento()

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "app": "Coral Expert System API",
        "ia_model_loaded": predictor_corales.esta_cargado(),
        "version": "1.0.0"
    }

@app.get("/api/preguntas", response_model=List[PreguntaResponse])
def obtener_preguntas():
    """Retorna la clave completa de preguntas taxonómicas dicotómicas."""
    preguntas = generar_preguntas()
    return preguntas

@app.post("/api/inferencia/paso", response_model=InferenciaResultadoResponse)
def navegar_inferencia(req: InferenciaRequest):
    """
    Navega un paso en el árbol de decisiones taxonómico.
    Recibe las respuestas acumuladas { "p1": "s", "p6": "ramificado", ... }
    """
    resultado = motor_inferencia.ejecutar(req.respuestas)
    
    if resultado.get("estado") == "pregunta":
        pregunta_id = resultado["pregunta_id"]
        preguntas_lista = generar_preguntas()
        preg_dict = {p["id"]: p for p in preguntas_lista}
        pregunta_info = preg_dict.get(pregunta_id)
        
        if not pregunta_info:
            return InferenciaResultadoResponse(
                estado="resultado",
                success=False,
                especie="Error de Sistema",
                mensaje=f"No se encontró la pregunta con ID: {pregunta_id}"
            )
            
        return InferenciaResultadoResponse(
            estado="pregunta",
            pregunta_id=pregunta_id,
            pregunta_detalle=PreguntaResponse(**pregunta_info)
        )
    else:
        # Es un resultado final
        return InferenciaResultadoResponse(
            estado="resultado",
            success=resultado.get("success", True),
            especie=resultado.get("especie"),
            nombre_comun=resultado.get("nombre_comun"),
            familia=resultado.get("familia"),
            orden=resultado.get("orden", "Scleractinia"),
            mensaje=resultado.get("mensaje"),
            sugerencia=resultado.get("sugerencia")
        )

@app.post("/api/ia/diagnostico", response_model=DiagnosticoIAResponse)
def diagnostico_ia(req: DiagnosticoIARequest):
    """
    Realiza un diagnóstico de texto libre en lenguaje natural mediante el Pipeline Híbrido:
    Deep Learning (TensorFlow) + Motor de Ponderación + Inferencia Reglada.
    """
    if not req.texto or len(req.texto.strip()) < 3:
        raise HTTPException(status_code=400, detail="El texto introducido es demasiado corto.")

    resultado_pred = predictor_corales.predecir_con_ponderacion(req.texto)
    respuestas_red = resultado_pred.get("respuestas_red", {})
    
    # Evaluar con el motor de inferencia usando las respuestas deducidas
    resultado_inferencia = motor_inferencia.ejecutar(respuestas_red)
    
    # Procesar ranking
    ranking_raw = resultado_pred.get("ranking", [])
    top_candidatos = []
    
    for idx, item in enumerate(ranking_raw[:5]):
        esp_info = item.get("especie", {})
        score_val = min(1.0, max(0.0, float(item.get("score", 0.0))))
        
        # Extraer coincidencias clave para la visualización UI
        coincidencias_dict = item.get("coincidencias", {})
        coincidencias_clave = []
        for p_k, c_v in coincidencias_dict.items():
            if c_v.get("match"):
                coincidencias_clave.append(f"Paso {p_k}: {c_v.get('predicho')}")
                
        top_candidatos.append(EspecieCandidata(
            especie=esp_info.get("nombre_cientifico", esp_info.get("especie", "Desconocido")),
            nombre_comun=esp_info.get("nombre_comun", "Desconocido"),
            familia=esp_info.get("familia", "Desconocido"),
            orden=esp_info.get("orden", "Scleractinia"),
            score_final=round(score_val, 4),
            similitud_ponderada=round(score_val * 100, 2),
            coincidencia_arbol=100.0 if (idx == 0 and resultado_inferencia.get("success")) else round(score_val * 100, 2),
            coincidencias_clave=coincidencias_clave
        ))
        
    especie_ganadora = {}
    if top_candidatos:
        top1 = top_candidatos[0]
        especie_ganadora = {
            "especie": top1.especie,
            "nombre_comun": top1.nombre_comun,
            "familia": top1.familia,
            "score": top1.score_final,
            "es_exacto": bool(resultado_inferencia.get("success"))
        }
    else:
        especie_ganadora = {
            "especie": "No identificado",
            "nombre_comun": "Desconocido",
            "familia": "Desconocida",
            "score": 0.0,
            "es_exacto": False
        }

    desglose = {
        "baja_confianza_red": resultado_pred.get("baja_confianza", False),
        "confianza_ponderacion": resultado_pred.get("confianza_ponderacion", "MEDIA"),
        "categorias_detectadas": resultado_pred.get("categorias_detectadas", {}),
        "inferencia_directa": resultado_inferencia
    }

    return DiagnosticoIAResponse(
        exito=True,
        metodo="Pipeline Coexistente (Deep Learning + Motor de Ponderación + Reglas Taxonómicas)",
        especie_ganadora=especie_ganadora,
        top_candidatos=top_candidatos,
        desglose_explicativo=desglose,
        respuestas_deducidas=respuestas_red
    )

@app.get("/api/especies")
def listar_especies():
    """Retorna la lista completa de especies en la base de conocimiento."""
    return base_conocimiento.listar_especies()

@app.post("/api/especies")
def crear_especie(req: EspecieCreateRequest):
    """Crea una nueva especie, valida duplicados, la guarda en especies.json y recarga el Ponderador NLP."""
    try:
        esp_id = req.nombre_cientifico.strip().lower().replace(" ", "_")
        
        # Validación de duplicados
        if base_conocimiento.existe_especie(esp_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La especie '{req.nombre_cientifico.strip()}' ya se encuentra registrada en el sistema."
            )

        nueva_especie = {
            "id": esp_id,
            "nombre_cientifico": req.nombre_cientifico.strip(),
            "nombre_comun": req.nombre_comun.strip(),
            "familia": req.familia.strip(),
            "orden": req.orden.strip() if req.orden else "Scleractinia",
            "tipo": req.tipo.strip() if req.tipo else "Escleractinio",
            "descripcion": req.descripcion.strip() if req.descripcion else "",
            "habitat": req.habitat.strip() if req.habitat else "Los Roques, Venezuela",
            "caracteristicas": req.caracteristicas or {}
        }

        # Guardar imagen codificada en base64 si se proporciona
        if req.imagen_base64:
            try:
                import base64
                img_data = req.imagen_base64
                if "," in img_data:
                    img_data = img_data.split(",", 1)[1]
                decoded = base64.b64decode(img_data)
                img_path = root_dir / "data" / "Imagenes" / f"{esp_id}.jpg"
                img_path.parent.mkdir(parents=True, exist_ok=True)
                with open(img_path, "wb") as f_img:
                    f_img.write(decoded)
            except Exception as img_err:
                print(f"Error guardando imagen de {esp_id}: {img_err}")

        especie_guardada = base_conocimiento.agregar_especie(nueva_especie)
        
        # Hot-reload del Ponderador NLP para actualizar la base de conocimientos en caliente
        if hasattr(predictor_corales, 'ponderador') and predictor_corales.ponderador:
            predictor_corales.ponderador._cargar_especies()

        return {
            "success": True,
            "mensaje": f"Especie '{nueva_especie['nombre_cientifico']}' agregada exitosamente.",
            "especie": especie_guardada
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar especie: {str(e)}"
        )

@app.get("/api/guia")
def obtener_guia():
    """Retorna los datos didácticos para la guía de clasificación taxonómica."""
    return {
        "titulo": "Guía Taxonómica del Atlántico para Los Roques",
        "descripcion": "Clave dicotómica interactiva para identificar especies de corales duros (Escleractinios e Hidrocorales) registrados en el Archipiélago de Los Roques.",
        "pasos_fundamentales": [
            {
                "paso": 1,
                "concepto": "Presencia de Coralitos",
                "detalle": "Los coralitos son la casa calcárea de los pólipos. Si la superficie es lisa con poros diminutos, se trata de un Hidrocoral (Coral de Fuego o Coral Encaje). Si tiene cavidades circulares o valles, es un Escleractinio."
            },
            {
                "paso": 2,
                "concepto": "Forma de la Colonia",
                "detalle": "Identifica si la colonia es masiva (forma de cerebro o rocas), ramificada (forma de arbusto o cuerno), laminar (láminas verticales/horizontales) o incrustante."
            },
            {
                "paso": 3,
                "concepto": "Disposición de los Coralitos",
                "detalle": "Observa si los coralitos están en hoyos independientes (plocoide/cerioide) o unidos en valles continuos tipo meandro (meandroide)."
            },
            {
                "paso": 4,
                "concepto": "Estructura de Septos y Columela",
                "detalle": "En especies cerebrales o masivas, cuenta la cantidad de septos por cm y observa la textura fina o toscamente dentada."
            }
        ]
    }

# Montar carpeta de imágenes de corales
imagenes_path = root_dir / "data" / "Imagenes"
if imagenes_path.exists():
    app.mount("/api/imagenes", StaticFiles(directory=str(imagenes_path)), name="static_imagenes")

# Montar frontend compilado de React si existe
dist_path = root_dir / "frontend" / "dist"
if dist_path.exists():
    app.mount("/", StaticFiles(directory=str(dist_path), html=True), name="static_frontend")
