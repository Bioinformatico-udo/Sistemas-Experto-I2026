# test_ia.py
import sys
import os
import json

# Configurar la codificación de la salida en consola para evitar UnicodeEncodeError en Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar que la raíz del proyecto esté en el path (para que 'src' sea un paquete)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.modelo_hibrido import PredictorCorales
from src.motor_inferencia import MotorInferencia
from src.preguntas import generar_preguntas

# Inicializar predictor e inferencia
predictor = PredictorCorales()
motor = MotorInferencia()

# Obtener preguntas para traducir IDs a textos legibles
preguntas_lista = generar_preguntas()
preguntas_dict = {p["id"]: p for p in preguntas_lista}

casos = [
    ('Caso 1: Ramas aplanadas (Esperado: Acropora palmata)', 
     'Coral con ramas aplanadas como paletas, color marrón claro, zona de oleaje'),
    ('Caso 2: Forma cerebro (Esperado: Diploria labyrinthiformis u otra especie de cerebro)', 
     'Coral grande redondo con surcos profundos como cerebro, color gris, zona profunda'),
    ('Caso 3: Forma hoja (Esperado: Agaricia agaricites u otra Agaricia)', 
     'Coral en forma de hoja o placa delgada, color marrón claro, poca luz'),
    ('Caso 4: Muchos hoyitos (Esperado: Siderastrea u Orbicella)', 
     'Coral redondo con muchos hoyitos pequeños en la superficie, duro como roca'),
    ('Caso 5: Coralitos en puntas (Esperado: Eusmilia fastigiata o Mussa angulosa)', 
     'Coral ramificado con hoyitos solo en las puntas de las ramas'),
]

print("=" * 70)
print("🧪 ANÁLISIS DE DIAGNÓSTICO DEL SISTEMA EXPERTO UNIFICADO")
print("=" * 70)

for nombre, desc in casos:
    print(f'\n📌 {nombre}')
    print(f'   Descripción: "{desc}"')
    
    # 1. Ejecutar predicción combinada (unificada)
    r = predictor.predecir_con_ponderacion(desc)
    if not r.get("success"):
        print(f'   ❌ Error en el predictor: {r.get("error")}')
        continue
        
    respuestas_predichas = r.get("respuestas_red", {})
    filtradas = {k: v for k, v in respuestas_predichas.items() if v != 'desconocido'}
    print(f'   🧠 Características predichas por la IA: {filtradas}')
    
    # 2. Ejecutar motor de inferencia dicotómico
    resultado = motor.ejecutar(filtradas)
    
    if resultado.get('success'):
        print(f'   ⚙️  Motor Inferencia (Éxito Directo): ✅ {resultado["especie"]} ({resultado["nombre_comun"]})')
    elif resultado.get('estado') == 'pregunta':
        pregunta_id = resultado['pregunta_id']
        preg_info = preguntas_dict.get(pregunta_id, {})
        preg_texto = preg_info.get("texto", "Pregunta desconocida")
        print(f'   ⚙️  Motor Inferencia (Incompleto): ℹ️ Se detuvo en {pregunta_id} -> "{preg_texto}"')
    else:
        print(f'   ⚙️  Motor Inferencia (Fallo): ❌ {resultado.get("mensaje", "No hay coincidencia en el árbol")}')
    
    # 3. Obtener ranking unificado (Top 3)
    ranking = r.get("ranking", [])
    if ranking:
        print(f'   🏆 TOP 3 ESPECIES SUGERIDAS (Sistema Unificado):')
        for i, item in enumerate(ranking[:3], 1):
            esp = item["especie"]
            score = item["score"]
            medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            print(f'      {medalla} {esp["nombre_cientifico"]} ({esp["nombre_comun"]}) | Confianza/Puntuación: {score:.4f}')
    else:
        print(f'   ⚠️  No se pudo calcular el ranking de especies.')
    print("-" * 70)

