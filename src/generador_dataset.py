# src/generador_dataset.py
"""
FASE 1 - Generador de Dataset Sintético para Red Neuronal Híbrida
Usa el Motor de Inferencia como "maestro" para etiquetar automáticamente
todas las especies de Los Roques con sus características taxonómicas.
"""

import sys
from pathlib import Path

# Configurar el paquete y el sys.path si se ejecuta directamente
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

import json
import csv
from .motor_inferencia import MotorInferencia
from .preguntas import generar_preguntas


# ─── CONFIGURACIÓN ───
RUTA_ESPECIES = "data/especies.json"
RUTA_DATASET = "data/dataset_entrenamiento.csv"
RUTA_VOCABULARIO = "data/vocabulario_taxonomico.json"

# ─── MAPEO DE CARACTERÍSTICAS A RESPUESTAS DEL CUESTIONARIO ───

MAPEO_RESPUESTAS_DIRECTAS = {
    # === HIDROCORALES ===
    "millepora_alcicornis": {"p1": "no", "p2": "incrustante"},
    "millepora_complanata": {"p1": "no", "p2": "aplanado", "p3": "vertical"},
    "millepora_squarrosa": {"p1": "no", "p2": "aplanado", "p3": "irregular"},
    
    # === ACROPORIDAE (ramificados cilíndricos) ===
    "acropora_palmata": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "toda", "p10": "cilindricas", "p11": "abanico"},
    "acropora_cervicornis": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "toda", "p10": "cilindricas", "p11": "cilindricas", "p13": "largas"},
    "acropora_prolifera": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "toda", "p10": "cilindricas", "p11": "cilindricas", "p13": "fusionadas"},
    
    # === AGARICIIDAE (laminar con colinas/valles) ===
    "undaria_agaricites": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "laminar", "p20": "colinas", "p22": "con", "p23": "unifacial", "p24": "discontinuos", "p28": "sin"},
    "undaria_humilis": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "poco", "p32": "convexa"},
    "agaricia_fragilis": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "laminar", "p20": "colinas", "p22": "con", "p23": "unifacial", "p24": "continuos", "p25": "5_8", "p27": "2_4"},
    "agaricia_lamarcki": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "laminar", "p20": "colinas", "p22": "con", "p23": "unifacial", "p24": "continuos", "p25": "3_5", "p26": "delgados"},
    "agaricia_tenuifolia": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "laminar", "p20": "colinas", "p22": "con", "p23": "bifacial"},
    "agaricia_undata": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "laminar", "p20": "colinas", "p22": "con", "p23": "unifacial", "p24": "continuos", "p25": "5_8", "p27": "6_7"},
    "leptoseris_cucullata": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "laminar", "p20": "colinas", "p22": "sin"},
    
    # === PORITIDAE ===
    "porites_astreoides": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "poroso", "p50": "12", "p51": "1_2_1_5"},
    "porites_divaricata": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "toda", "p10": "conicas", "p14": "mas_10", "p17": "finas"},
    "porites_furcata": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "toda", "p10": "conicas", "p14": "mas_10", "p17": "gruesas", "p18": "bifurcadas"},
    "porites_porites": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "toda", "p10": "conicas", "p14": "mas_10", "p17": "gruesas", "p18": "hinchadas"},
    
    # === SIDERASTREIDAE ===
    "siderastrea_radians": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "poroso", "p50": "24_48", "p52": "1_5_4_2"},
    "siderastrea_siderea": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "poroso", "p50": "24_48", "p52": "2_6_5_0"},
    
    # === MEANDRINIDAE ===
    "dendrogyra_cylindrus": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "no", "p34": "pilares"},
    "meandrina_meandrites": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "no", "p34": "hemisferica"},
    "eusmilia_fastigiata": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "puntas", "p8": "grandes", "p9": "ovales"},
    
    # === MUSSIDAE ===
    "scolymia_lacera": {"p1": "s", "p4": "solitario", "p5": "toscamente"},
    "scolymia_cubensis": {"p1": "s", "p4": "solitario", "p5": "finamente"},
    "mussa_angulosa": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "puntas", "p8": "grandes", "p9": "circulares"},
    "isophyllia_sinuosa": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "dentados", "p35": "sin", "p42": "mayor_0_5", "p45": "toscas", "p47": "2_5"},
    "isophyllastrea_rigida": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "mayor_1"},
    "mycetophyllia_aliciae": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "dentados", "p35": "con", "p36": "sencilla", "p39": "iguales"},
    "mycetophyllia_ferox": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "dentados", "p35": "con", "p36": "sencilla", "p39": "delgados", "p40": "continuas", "p41": "discontinuos"},
    "mycetophyllia_lamarckiana": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "dentados", "p35": "con", "p36": "sencilla", "p39": "delgados", "p40": "radiales"},
    
    # === FAVIIDAE / MERULINIDAE ===
    "orbicella_annularis": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "compacto", "p53": "no", "p55": "separadas", "p57": "menor_6", "p58": "circulares", "p60": "2_2_5", "p61": "plocoide", "p62": "lisa", "p63": "columnar"},
    "orbicella_faveolata": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "compacto", "p53": "no", "p55": "separadas", "p57": "menor_6", "p58": "circulares", "p60": "2_2_5", "p61": "plocoide", "p62": "lisa", "p63": "costroso_hemisferico"},
    "orbicella_franksi": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "compacto", "p53": "no", "p55": "separadas", "p57": "menor_6", "p58": "circulares", "p60": "2_2_5", "p61": "plocoide", "p62": "desigual"},
    "montastraea_cavernosa": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "compacto", "p53": "no", "p55": "separadas", "p57": "mayor_6"},
    "diploria_labyrinthiformis": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "dentados", "p35": "sin", "p42": "menor_0_5", "p43": "menor_20", "p44": "con"},
    "pseudodiploria_strigosa": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "dentados", "p35": "sin", "p42": "menor_0_5", "p43": "menor_20", "p44": "sin"},
    "colpophyllia_natans": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "dentados", "p35": "con", "p36": "doble", "p37": "largas", "p38": "plana"},
    "favia_fragum": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "compacto", "p53": "no", "p55": "apinadas", "p56": "4_5_6_5"},
    "manicina_areolata": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "valles", "p31": "pronunciados", "p33": "dentados", "p35": "sin", "p42": "mayor_0_5", "p45": "finos", "p46": "central"},
    
    # === POCILLOPORIDAE / ASTROCOENIIDAE ===
    "madracis_decactis": {"p1": "s", "p4": "colonial", "p6": "ramificado", "p7": "toda", "p10": "conicas", "p14": "10", "p15": "nodular"},
    "stephanocoenia_intersepta": {"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva", "p30": "copas", "p48": "menor_1", "p49": "compacto", "p53": "estiliforme", "p54": "2_6_3_0"},
}

# ─── FUNCIONES AUXILIARES ───

def caracteristicas_a_respuestas(especie_id: str, caract: dict) -> dict:
    """
    Convierte el bloque 'caracteristicas' de una especie en un diccionario
    de respuestas que el motor de inferencia puede procesar.
    Primero busca en el mapeo directo; si no existe, usa la lógica genérica.
    """
    if especie_id in MAPEO_RESPUESTAS_DIRECTAS:
        return MAPEO_RESPUESTAS_DIRECTAS[especie_id].copy()

    respuestas = {}
    
    # === PASO 1: ¿Tiene coralitos? ===
    if "tiene_coralitos" in caract:
        respuestas["p1"] = "s" if caract["tiene_coralitos"] else "no"
    
    # === HIDROCORALES (p1=no) ===
    if not caract.get("tiene_coralitos", True):
        forma = caract.get("forma", "")
        if "incrustante" in forma or "ramificada" in forma:
            respuestas["p2"] = "incrustante"
        elif "laminar" in forma or "aplanado" in forma:
            respuestas["p2"] = "aplanado"
            if "vertical" in forma:
                respuestas["p3"] = "vertical"
            elif "irregular" in forma:
                respuestas["p3"] = "irregular"
            else:
                respuestas["p3"] = "vertical"
        return respuestas
    
    # === ESCLERACTINIOS (p1=s) ===
    forma = caract.get("forma", "")
    
    # PASO 4: Solitario vs Colonial
    if "solitario" in forma:
        respuestas["p4"] = "solitario"
        if caract.get("septos") == "toscamente_dentados":
            respuestas["p5"] = "toscamente"
        else:
            respuestas["p5"] = "finamente"
        return respuestas
    
    respuestas["p4"] = "colonial"
    
    # PASO 6: Ramificado o no
    if "ramificada" in forma:
        respuestas["p6"] = "ramificado"
        coralitos_en = caract.get("coralitos_en", "")
        
        if coralitos_en == "puntas":
            respuestas["p7"] = "puntas"
            if caract.get("copas_ovales"):
                respuestas["p8"] = "grandes"
                respuestas["p9"] = "ovales"
            elif caract.get("copas_circulares"):
                respuestas["p8"] = "grandes"
                respuestas["p9"] = "circulares"
            else:
                respuestas["p8"] = "pequenas"
        else:
            respuestas["p7"] = "toda"
            if "cilindrica" in forma or "fusionada" in forma or "abanico" in forma:
                respuestas["p10"] = "cilindricas"
                if "abanico" in forma:
                    respuestas["p11"] = "abanico"
                else:
                    respuestas["p11"] = "cilindricas"
                    ramas = caract.get("ramas_largas_fusionadas", "")
                    if ramas == "largas":
                        respuestas["p13"] = "largas"
                    elif ramas == "fusionadas":
                        respuestas["p13"] = "fusionadas"
            else:
                respuestas["p10"] = "conicas"
                septos = caract.get("numero_septos", 0)
                respuestas["p14"] = "10" if septos == 10 else "mas_10"
    else:
        respuestas["p6"] = "no"
        if "laminar" in forma:
            respuestas["p19"] = "laminar"
            superficie = caract.get("superficie", "")
            if "copas" in superficie:
                respuestas["p20"] = "copas"
            else:
                respuestas["p20"] = "colinas"
                if caract.get("sin_columela"):
                    respuestas["p22"] = "sin"
                else:
                    respuestas["p22"] = "con"
                    if "bifacial" in forma:
                        respuestas["p23"] = "bifacial"
                    else:
                        respuestas["p23"] = "unifacial"
                        respuestas["p24"] = "continuos" if caract.get("valles_continuos") else "discontinuos"
        else:
            respuestas["p19"] = "masiva"
            superficie = caract.get("superficie", "")
            respuestas["p30"] = "valles" if "valles" in superficie else "copas"
    
    return respuestas


# ─── SINÓNIMOS COLOQUIALES ───
SINONIMOS_RAMIFICADO = [
    "coral ramificado", "ramas", "ramificaciones", "crecimiento arbustivo",
    "forma de ramas", "coral de dedos", "estructura ramificada", "ramas coralinas",
    "parece un arbusto", "como dedos que salen", "tiene ramitas", "ramas finas",
    "parece un árbol pequeño", "con muchas ramificaciones", "ramas como cuernos",
    "se extiende como ramas", "brazos que salen", "forma de candelabro"
]

SINONIMOS_ABANICO = [
    "ramas en forma de abanico", "palmeado", "aplanado en abanico", "en abanico",
    "como paleta", "como paletas", "forma de abanico", "ramas aplanadas",
    "parece una mano abierta", "como un abanico", "plano y ancho", "como oreja"
]

SINONIMOS_MASIVO = [
    "coral masivo", "colonias hemisféricas", "forma de domo", "bloque compacto",
    "montículo rocoso", "crecimiento macizo", "estructura globosa", "forma de roca",
    "parece una roca", "como un domo", "como una pelota", "roca redonda",
    "parece una piedra grande", "como un montículo", "roca viva", "roca coralina",
    "como una bola", "esfera rocosa", "parece un balón", "redondo", "redonda", 
    "esférico", "esférica", "forma redonda"
]

SINONIMOS_LAMINAR = [
    "coral laminar", "forma de lámina", "crecimiento en placas", "placas superpuestas",
    "platos aplanados", "láminas delgadas", "forma de disco folioso",
    "como una hoja", "como hojas", "parece una hoja", "como papel",
    "como platos", "como una placa", "fino como una hoja", "como una tortilla",
    "como un disco", "aplanado como un plato", "en capas", "como una laja",
    "en forma de hoja", "hojas delgadas", "placa delgada", "placas delgadas", "aspecto de hoja"
]

SINONIMOS_SOLITARIO = [
    "coral solitario", "disco individual", "un solo pólipo grande", "pólipo solitario",
    "forma de copa individual", "no colonial", "uno solo", "solo hay uno",
    "un único coral", "aislado", "no tiene colonia", "individual", "separado"
]

SINONIMOS_VALLES = [
    "valles y colinas", "superficie cerebroide", "meandros sinuosos",
    "valles sinuosos", "forma de cerebro", "valles profundos", "crestas y valles",
    "surcos profundos", "como un cerebro", "parece un cerebro", "surcos como cerebro",
    "laberinto", "como laberinto", "con surcos", "surcos sinuosos",
    "se ve como un cerebro", "con canales", "con grietas", "como una nuez",
    "surcos profundos", "surcos", "surcos sinuosos", "canales"
]

SINONIMOS_COPAS = [
    "pequeñas copas", "superficie con copas", "coralitos en forma de copa",
    "pequeñas celdas circulares", "poros de coralitos", "aberturas circulares",
    "hoyitos", "huequitos", "como poros", "agujeritos", "pequeños hoyos",
    "puntitos", "como una esponja", "con huecos", "con agujeros", "hoyuelos",
    "como panal", "como una colmena", "con poros", "con hoyitos pequeños"
]

SINONIMOS_COLORES = [
    "color marrón", "color café claro", "tonalidad verdosa", "color marrón claro",
    "color amarillento", "color grisáceo", "color café", "marrón", "café",
    "gris", "amarillento", "verdoso", "beige", "crema", "blanquecino",
    "color arena", "como arena", "color piedra", "color tierra"
]

SINONIMOS_TEXTURA = [
    "textura áspera", "esqueleto calcáreo", "superficie porosa", "colonias densas",
    "áspero al tacto", "rugoso", "duro como roca", "como una roca",
    "superficie rugosa", "superficie lisa", "liso", "poroso", "esponjoso",
    "como esponja", "superficie irregular", "superficie uniforme"
]

# Sinónimos para la posición de los coralitos
SINONIMOS_CORALITOS_PUNTAS = [
    "coralitos en las puntas", "hoyitos solo en las puntas de las ramas", 
    "copas en los extremos de las ramas", "hoyitos en las puntas",
    "coralitos concentrados en los extremos"
]

SINONIMOS_CORALITOS_TODA = [
    "coralitos en toda la superficie", "hoyitos en toda la rama", 
    "copas distribuidas por toda la superficie", "poros por toda la rama",
    "coralitos en toda la rama"
]

# ─── PLANTILLAS DE LENGUAJE NATURAL ───
PLANTILLAS_CON_SUPERFICIE = [
    "Parece {forma} con {superficie}, {color}.",
    "Es como {forma}, tiene {superficie} y es {color}.",
    "Encontré esto: {forma}, se ve {superficie}, color {color}.",
    "Uno {forma} que está {textura}, con {superficie}.",
    "Es un coral {forma}, {textura}, con {superficie} de color {color}.",
    "Vi un coral {forma}, tiene {superficie}, parece {color}.",
    "{forma} con pinta de {superficie}, tono {color}.",
    "Un coral {forma} que tiene {superficie} y es {textura}.",
    "Estaba buceando y vi {forma} con {superficie}, {color}.",
    "Como {forma} pero con {superficie}, {textura}, {color}.",
    "Especie {forma}, presenta {superficie}, tonalidad {color}.",
    "Colonia {forma} con {superficie} característica, {color}.",
    "Coral de tipo {forma}, superficie {superficie}, {textura}.",
    "Observamos {forma} con {superficie} evidente, coloración {color}.",
    "{forma}, {superficie}, {color}.",
    "Tipo: {forma}. Superficie: {superficie}. Color: {color}.",
    "Forma: {forma}. Textura: {superficie}. Tono: {color}."
]

PLANTILLAS_SIN_SUPERFICIE = [
    "Parece {forma}, {color}.",
    "Es como {forma} y es {color}.",
    "Encontré esto: {forma}, color {color}.",
    "Uno {forma} que está {textura}.",
    "Es un coral {forma}, {textura}, de color {color}.",
    "Vi un coral {forma}, parece {color}.",
    "{forma}, tono {color}.",
    "Un coral {forma} que es {textura}.",
    "Estaba buceando y vi {forma}, {color}.",
    "Como {forma}, {textura}, {color}.",
    "Especie {forma}, tonalidad {color}.",
    "Colonia {forma} característica, {color}.",
    "Coral de tipo {forma}, {textura}.",
    "Observamos {forma} con coloración {color}.",
    "{forma}, {color}.",
    "Tipo: {forma}. Color: {color}.",
    "Forma: {forma}. Textura: {textura}. Tono: {color}."
]

def generar_descripciones_entrenamiento(especie: dict) -> list:
    """Genera descripciones con lenguaje coloquial y técnico mezclado"""
    desc = especie.get("descripcion", "")
    caract = especie.get("caracteristicas", {})
    forma = caract.get("forma", "")
    superficie = caract.get("superficie", "")
    
    import random
    rng = random.Random(hash(especie.get("nombre_cientifico", "")) % 10000)
    
    # 1. Seleccionar pool de formas
    if "ramificada" in forma or "ramificado" in forma:
        if "abanico" in forma:
            formas_pool = SINONIMOS_RAMIFICADO + SINONIMOS_ABANICO
        else:
            formas_pool = SINONIMOS_RAMIFICADO
    elif "laminar" in forma:
        formas_pool = SINONIMOS_LAMINAR
    elif "masiva" in forma or "masivo" in forma:
        formas_pool = SINONIMOS_MASIVO
    elif "solitario" in forma:
        formas_pool = SINONIMOS_SOLITARIO
    else:
        formas_pool = ["coral"]
        
    # 2. Seleccionar pool de superficies
    if "valles" in superficie or "colinas" in superficie:
        superf_pool = SINONIMOS_VALLES
    elif "copas" in superficie:
        superf_pool = SINONIMOS_COPAS
    else:
        superf_pool = [""]
        
    # 3. Seleccionar pool de posición de coralitos (p7)
    coralitos_en = caract.get("coralitos_en", "")
    coralitos_en_syn = []
    if coralitos_en == "puntas":
        coralitos_en_syn = SINONIMOS_CORALITOS_PUNTAS
    elif coralitos_en == "toda_la_superficie" or "toda" in coralitos_en:
        coralitos_en_syn = SINONIMOS_CORALITOS_TODA
        
    colores_pool = SINONIMOS_COLORES
    texturas_pool = SINONIMOS_TEXTURA
    
    descripciones = []
    
    # Agregar descripción base
    descripciones.append(desc)
    
    # Generar 15 variaciones basadas en la descripción original + detalles/posición
    for _ in range(15):
        c_col = rng.choice(colores_pool)
        t = rng.choice(texturas_pool)
        c_pos = rng.choice(coralitos_en_syn) if coralitos_en_syn else ""
        txt = f"{desc} Presenta {c_col} y {t}."
        if c_pos:
            txt = f"{txt[:-1]} y {c_pos}."
        descripciones.append(txt)
        
    # Generar 35 variaciones puramente sintéticas mediante plantillas
    for _ in range(35):
        f = rng.choice(formas_pool)
        s = rng.choice(superf_pool) if superf_pool[0] else ""
        c_col = rng.choice(colores_pool)
        t = rng.choice(texturas_pool)
        c_pos = rng.choice(coralitos_en_syn) if coralitos_en_syn else ""
        
        # Elegir plantilla dependiendo de si hay superficie
        if s:
            plantilla = rng.choice(PLANTILLAS_CON_SUPERFICIE)
        else:
            plantilla = rng.choice(PLANTILLAS_SIN_SUPERFICIE)
            
        try:
            txt = plantilla.format(forma=f, superficie=s, color=c_col, textura=t)
            # Integrar posición de coralitos si aplica
            if c_pos:
                txt = f"{txt[:-1]} y {c_pos}." if txt.endswith(".") else f"{txt} y {c_pos}."
            descripciones.append(txt)
        except KeyError:
            # En caso de fallo de formato, versión simple
            txt_partes = [f, s, c_col, t]
            if c_pos:
                txt_partes.append(c_pos)
            txt = ", ".join(p for p in txt_partes if p) + "."
            descripciones.append(txt)
            
    # Eliminar duplicados
    descripciones = list(set([d.strip() for d in descripciones if d.strip()]))
    return descripciones


def generar_dataset():
    """Punto principal: genera el dataset completo para entrenamiento"""
    
    print("=" * 60)
    print("🪸 GENERADOR DE DATASET - CORALES DE LOS ROQUES")
    print("=" * 60)
    
    print("\n🔄 Cargando especies...")
    with open(RUTA_ESPECIES, "r", encoding="utf-8") as f:
        especies = json.load(f)
    
    motor = MotorInferencia()
    preguntas = generar_preguntas()
    
    dataset = []
    vocabulario = set()
    exitos = []
    errores = []
    
    print(f"📋 Procesando {len(especies)} especies...\n")
    
    for especie in especies:
        especied_id = especie["id"]
        caract = especie.get("caracteristicas", {})
        
        # Convertir características a respuestas del motor
        respuestas = caracteristicas_a_respuestas(especied_id, caract)
        
        # Validar con el motor de inferencia
        resultado = motor.ejecutar(respuestas)
        
        if resultado.get("success"):
            exitos.append(especie["nombre_cientifico"])
            print(f"   ✅ {especie['nombre_cientifico']}")
            
            # Generar descripciones textuales para entrenamiento
            descripciones = generar_descripciones_entrenamiento(especie)
            
            for desc in descripciones:
                palabras = desc.lower().replace(",", "").replace(".", "").replace(":", "").replace(";", "").split()
                vocabulario.update(palabras)
                
                dataset.append({
                    "id_especie": especied_id,
                    "nombre_cientifico": especie["nombre_cientifico"],
                    "nombre_comun": especie["nombre_comun"],
                    "familia": especie["familia"],
                    "tipo": especie.get("tipo", "Escleractinio"),
                    "descripcion": desc,
                    "respuestas_cuestionario": json.dumps(respuestas, ensure_ascii=False),
                })
        else:
            errores.append({
                "especie": especie["nombre_cientifico"],
                "error": resultado.get("mensaje", "Error desconocido"),
                "respuestas_intentadas": respuestas
            })
            print(f"   ❌ {especie['nombre_cientifico']}: {resultado.get('mensaje', 'Error')}")
    
    # Guardar dataset
    print(f"\n💾 Guardando dataset ({len(dataset)} registros)...")
    with open(RUTA_DATASET, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id_especie", "nombre_cientifico", "nombre_comun", 
            "familia", "tipo", "descripcion", "respuestas_cuestionario"
        ])
        writer.writeheader()
        writer.writerows(dataset)
    
    # Guardar vocabulario
    with open(RUTA_VOCABULARIO, "w", encoding="utf-8") as f:
        json.dump(sorted(list(vocabulario)), f, ensure_ascii=False, indent=2)
    
    # Reporte final
    print(f"\n{'=' * 60}")
    print(f"✅ DATASET GENERADO EXITOSAMENTE")
    print(f"   📊 Registros totales: {len(dataset)}")
    print(f"   🏷️  Especies cubiertas: {len(set(d['id_especie'] for d in dataset))}")
    print(f"   📝 Palabras en vocabulario: {len(vocabulario)}")
    print(f"   ✅ Éxitos: {len(exitos)}")
    print(f"   ❌ Errores: {len(errores)}")
    
    if errores:
        print(f"\n⚠️  Detalle de errores:")
        for e in errores:
            print(f"   ❌ {e['especie']}: {e['error']}")
    
    print(f"{'=' * 60}")
    return dataset, vocabulario


if __name__ == "__main__":
    generar_dataset()