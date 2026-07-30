import json
import os

# Directorio raiz del proyecto (carpeta que contiene main.py), calculado a
# partir de la ubicacion de este archivo. Evita que la aplicacion falle si
# se ejecuta desde otro directorio de trabajo.
DIR_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_JSON_USUARIO = os.path.join(DIR_PROYECTO, "especies_usuario.json")


def rutaRecurso(rutaRelativa):
    """Convierte una ruta guardada en la base de conocimientos en ruta absoluta."""
    if not rutaRelativa:
        return ""
    if os.path.isabs(rutaRelativa):
        return rutaRelativa
    return os.path.join(DIR_PROYECTO, rutaRelativa)

ESPECIES = {
    "Paguristes angustitheca": {
        "autor": "McLaughlin y Provenzano, 1974",
        "genero": "Paguristes",
        "imagen": "recursos/Paguristes_angustitheca/Paguristes angustitheca.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": True,
            "flageloSetasLargas": True,
            "quelipedosIguales": True,
            "quelipedoIzquierdoMayor": False,
            "dedosCuchara": True,
            "caparazonReticulado": False,
            "dactiloMayorPropodo": False,
            "bandaLongitudinalClara": False,
            "bandasTransversasRojas": False,
            "quelipedoDerechoLigeramenteMayor": False,
            "quelipedoIzqMuchoMayor": False,
            "quelipedoLiso": False,
            "hacesSetasPalma": False,
        },
        "tallaMm": {"LE_min": 1.45, "LE_max": 7.00, "AE_min": 1.45, "AE_max": 4.80},
        "sustratos": ["rocas", "praderas de Thalassia", "sustrato arenoso"],
        "profundidadM": (1.5, 4.0),
        "estaciones": ["E1", "E3", "E5"],
        "distribucion": "Venezuela hasta Guayana Francesa",
        "descripcion": (
            "Escudo más largo que ancho en ejemplares grandes, tan ancho como largo en pequeños. "
            "Superficie anterolateral armada con espínulas. Rostro agudo, más avanzado que las "
            "proyecciones laterales. Flagelo antenal con setas > 6 veces la longitud de un artejo. "
            "Quelípedos iguales. Carpo con 5-7 espinas fuertes. Telson con espinas fuertes en "
            "margen posterior y posterolaterales. Pertenece al complejo Paguristes tortugae."
        ),
        "color": "#2196F3",
        "notaIdentificacion": "Única del complejo tortugae con setas antenales tan largas (> 6× la longitud de un artejo).",
    },
    "Paguristes perplexus": {
        "autor": "McLaughlin y Provenzano, 1974",
        "genero": "Paguristes",
        "imagen": "recursos/Paguristes perplexus/Paguristes perplexus.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": True,
            "flageloSetasLargas": False,
            "quelipedosIguales": True,
            "quelipedoIzquierdoMayor": False,
            "dedosCuchara": True,
            "caparazonReticulado": False,
            "dactiloMayorPropodo": False,
            "bandaLongitudinalClara": False,
            "bandasTransversasRojas": False,
            "quelipedoDerechoLigeramenteMayor": False,
            "quelipedoIzqMuchoMayor": False,
            "quelipedoLiso": False,
            "hacesSetasPalma": False,
        },
        "tallaMm": {"LE_min": 1.75, "LE_max": 4.70, "AE_min": 1.40, "AE_max": 3.40},
        "sustratos": ["rocas sobre Thalassia", "coral muerto", "sustrato areno-fangoso"],
        "profundidadM": (1.5, 3.5),
        "estaciones": ["E1", "E2"],
        "distribucion": "Venezuela y Guayana Francesa hasta Brasil",
        "descripcion": (
            "Escudo más largo que ancho, márgenes laterales casi rectos y divergentes distalmente. "
            "Flagelo antenal corto con setas ≤ longitud de 1 artejo. Quelípedos subiguales, "
            "superficie dorsal setosa con gránulos espinosos. Segundo par de patas caminadoras "
            "setoso; mero desarmado. Primer registro para Isla de Margarita."
        ),
        "color": "#1976D2",
        "notaIdentificacion": "Se diferencia de P. tortugae por ausencia de espinas en margen extensor del mero del 2° par.",
    },
    "Isocheles wurdemanni": {
        "autor": "Stimpson, 1859",
        "genero": "Isocheles",
        "imagen": "recursos/Isocheles wurdemanni/Isocheles wurdemanni.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": False,
            "flageloSetasLargas": True,
            "quelipedosIguales": True,
            "quelipedoIzquierdoMayor": True,
            "dedosCuchara": False,
            "caparazonReticulado": True,
            "dactiloMayorPropodo": False,
            "bandaLongitudinalClara": False,
            "bandasTransversasRojas": False,
            "quelipedoDerechoLigeramenteMayor": False,
            "quelipedoIzqMuchoMayor": False,
            "quelipedoLiso": False,
            "hacesSetasPalma": False,
        },
        "tallaMm": {"LE_min": 3.55, "LE_max": 6.80, "AE_min": 3.50, "AE_max": 6.75},
        "sustratos": ["sustrato arenoso"],
        "profundidadM": (0.4, 1.5),
        "estaciones": ["E6", "E14"],
        "distribucion": "Texas (EE.UU.) hasta Venezuela",
        "descripcion": (
            "Escudo casi tan ancho como largo. Caparazón posterior con celdas calcificadas "
            "de apariencia reticulada — carácter diagnóstico único en la familia. Quelípedos "
            "subiguales con izquierdo ligeramente mayor. Dedos de ápice aguzado (no en cuchara). "
            "Pedúnculos oculares cortos con bandas longitudinales oscuras. Única representante "
            "del género en Venezuela."
        ),
        "color": "#00897B",
        "notaIdentificacion": "Caparazón posterior reticulado (celdas calcificadas) = diagnóstico definitivo.",
    },
    "Clibanarius cubensis": {
        "autor": "(Saussure, 1858)",
        "genero": "Clibanarius",
        "imagen": "recursos/Clibanarius cubensis/Clibanarius cubensis.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": False,
            "flageloSetasLargas": False,
            "quelipedosIguales": True,
            "quelipedoIzquierdoMayor": False,
            "dedosCuchara": True,
            "caparazonReticulado": False,
            "dactiloMayorPropodo": True,
            "bandaLongitudinalClara": True,
            "bandasTransversasRojas": False,
            "quelipedoDerechoLigeramenteMayor": False,
            "quelipedoIzqMuchoMayor": False,
            "quelipedoLiso": False,
            "hacesSetasPalma": False,
        },
        "tallaMm": {"LE_min": 8.25, "LE_max": 8.25, "AE_min": 6.00, "AE_max": 6.00},
        "sustratos": ["sustrato rocoso intermareal"],
        "profundidadM": (0.0, 0.5),
        "estaciones": ["E3"],
        "distribucion": "Florida (EE.UU.) hasta Venezuela",
        "descripcion": (
            "Escudo más largo que ancho. Primer y segundo par de patas caminadoras con tubérculos "
            "hialinos y DOS BANDAS CLARAS separadas por tres bandas oscuras longitudinales. "
            "Dactilo más largo que el propodo (carácter clave). Quelípedos subiguales con "
            "dedos en forma de cuchara. Primer registro para aguas costeras de la Península de Macanao."
        ),
        "color": "#F57C00",
        "notaIdentificacion": "Dactilo > propodo en patas caminadoras + DOS bandas claras anchas en las patas.",
    },
    "Clibanarius antillensis": {
        "autor": "Stimpson, 1859",
        "genero": "Clibanarius",
        "imagen": "recursos/Clibanarius antillensis/Clibanarius antillensis.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": False,
            "flageloSetasLargas": False,
            "quelipedosIguales": True,
            "quelipedoIzquierdoMayor": False,
            "dedosCuchara": True,
            "caparazonReticulado": False,
            "dactiloMayorPropodo": False,
            "bandaLongitudinalClara": True,
            "bandasTransversasRojas": False,
            "quelipedoDerechoLigeramenteMayor": False,
            "quelipedoIzqMuchoMayor": False,
            "quelipedoLiso": False,
            "hacesSetasPalma": False,
        },
        "tallaMm": {"LE_min": 1.20, "LE_max": 4.45, "AE_min": 1.00, "AE_max": 3.45},
        "sustratos": ["rocas", "praderas de Thalassia", "esponjas"],
        "profundidadM": (0.1, 1.0),
        "estaciones": ["E3", "E4", "E11", "E12", "E13"],
        "distribucion": "Florida (EE.UU.) hasta Brasil",
        "descripcion": (
            "Escudo más largo que ancho, subrectangular, con surcos pilosos en márgenes "
            "laterales anteriores. Dactilo de patas caminadoras MENOR que el propodo con "
            "UNA banda longitudinal clara. Telson desarmado (margen distal sin espinas). "
            "Primer señalamiento para aguas litorales de la Península de Macanao."
        ),
        "color": "#FB8C00",
        "notaIdentificacion": "UNA banda longitudinal clara en patas + dactilo < propodo + telson desarmado.",
    },
    "Clibanarius tricolor": {
        "autor": "(Gibbes, 1850)",
        "genero": "Clibanarius",
        "imagen": "recursos/Clibanarius tricolor/Clibanarius tricolor.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": False,
            "flageloSetasLargas": False,
            "quelipedosIguales": True,
            "quelipedoIzquierdoMayor": False,
            "dedosCuchara": True,
            "caparazonReticulado": False,
            "dactiloMayorPropodo": False,
            "bandaLongitudinalClara": False,
            "bandasTransversasRojas": True,
            "quelipedoDerechoLigeramenteMayor": False,
            "quelipedoIzqMuchoMayor": False,
            "quelipedoLiso": False,
            "hacesSetasPalma": False,
        },
        "tallaMm": {"LE_min": 2.15, "LE_max": 2.75, "AE_min": 1.75, "AE_max": 2.15},
        "sustratos": ["rocas sobre Thalassia"],
        "profundidadM": (0.1, 0.5),
        "estaciones": ["E11"],
        "distribucion": "Bermuda, Florida, Antillas, Colombia, Venezuela hasta Brasil",
        "descripcion": (
            "Caparazón anterior subrectangular con gránulos y setas dispersas. Escamas oculares "
            "con CINCO espinas agudas (vs. C. antillensis sin espinas en escama). Patas caminadoras "
            "con BANDAS TRANSVERSALES y lunares de color ROJO. Dactilo más corto que el propodo. "
            "Telson con espinas en margen posterior, más abundantes en lóbulo derecho."
        ),
        "color": "#E53935",
        "notaIdentificacion": "Bandas transversas rojas + lunares en patas + 5 espinas en escama ocular.",
    },
    "Petrochirus diogenes": {
        "autor": "(Linnaeus, 1758)",
        "genero": "Petrochirus",
        "imagen": "recursos/Petrochirus diogenes/Petrochirus_diogenes.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": False,
            "flageloSetasLargas": False,
            "quelipedosIguales": False,
            "quelipedoIzquierdoMayor": False,
            "dedosCuchara": False,
            "caparazonReticulado": False,
            "dactiloMayorPropodo": False,
            "bandaLongitudinalClara": False,
            "bandasTransversasRojas": False,
            "quelipedoDerechoLigeramenteMayor": True,
            "quelipedoIzqMuchoMayor": False,
            "quelipedoLiso": False,
            "hacesSetasPalma": False,
        },
        "tallaMm": {"LE_min": 8.85, "LE_max": 25.50, "AE_min": 8.95, "AE_max": 22.15},
        "sustratos": ["sustrato arenoso", "praderas de Thalassia"],
        "profundidadM": (0.5, 4.5),
        "estaciones": ["E2", "E3", "E5"],
        "distribucion": "Carolina del Norte (EE.UU.) hasta Brasil",
        "descripcion": (
            "La especie más grande de la familia en el área (hasta 25 mm LE). Quelípedos "
            "desiguales con DERECHO ligeramente mayor (único en Diogenidae local). Flagelos "
            "antenales desarmados (sin setas). Carpo y propodo ornamentados con rosetas de "
            "gránulos. Crista dentata con ocho dientes cónicos fuertes."
        ),
        "color": "#6D4C41",
        "notaIdentificacion": "Mayor tamaño de todos + quelípedo DERECHO mayor + rosetas en carpo/propodo.",
    },
    "Calcinus tibicen": {
        "autor": "(Herbst, 1791)",
        "genero": "Calcinus",
        "imagen": "recursos/Calcinus tibicen/Calcinus tibicen.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": False,
            "flageloSetasLargas": False,
            "quelipedosIguales": False,
            "quelipedoIzquierdoMayor": True,
            "dedosCuchara": False,
            "caparazonReticulado": False,
            "dactiloMayorPropodo": False,
            "bandaLongitudinalClara": False,
            "bandasTransversasRojas": False,
            "quelipedoDerechoLigeramenteMayor": False,
            "quelipedoIzqMuchoMayor": True,
            "quelipedoLiso": True,
            "hacesSetasPalma": False,
        },
        "tallaMm": {"LE_min": 1.00, "LE_max": 9.00, "AE_min": 0.85, "AE_max": 7.40},
        "sustratos": ["sustrato rocoso", "coral muerto", "praderas de Thalassia", "coral de fuego (Millepora)"],
        "profundidadM": (0.0, 2.0),
        "estaciones": ["E5", "E7", "E9", "E10", "E11", "E12", "E13"],
        "distribucion": "Florida, Bahamas, Antillas, Venezuela, Brasil",
        "descripcion": (
            "Quelípedo izquierdo mucho mayor que el derecho. Superficie del quelípedo izquierdo "
            "LISA, sin setas (salvo superficie interna de los dedos). Ápice de los dedos de "
            "apariencia CALCÁREA. Especie con mayor distribución en el área de estudio (presente "
            "en 7 de 14 estaciones). Habita sustrato rocoso, coral muerto y Millepora sp."
        ),
        "color": "#8E24AA",
        "notaIdentificacion": "Quelípedo izquierdo LISO (sin setas en superficie exterior) + ápice calcáreo.",
    },
    "Dardanus fucosus": {
        "autor": "Biffar y Provenzano, 1972",
        "genero": "Dardanus",
        "imagen": "recursos/Dardanus fucosus/Dardanus fucosus.jpg",
        "caracteres": {
            "pleopodosPrimerSomito": False,
            "flageloSetasLargas": False,
            "quelipedosIguales": False,
            "quelipedoIzquierdoMayor": True,
            "dedosCuchara": False,
            "caparazonReticulado": False,
            "dactiloMayorPropodo": False,
            "bandaLongitudinalClara": False,
            "bandasTransversasRojas": False,
            "quelipedoDerechoLigeramenteMayor": False,
            "quelipedoIzqMuchoMayor": True,
            "quelipedoLiso": False,
            "hacesSetasPalma": True,
        },
        "tallaMm": {"LE_min": 11.00, "LE_max": 11.00, "AE_min": 9.60, "AE_max": 9.60},
        "sustratos": ["sustrato rocoso-arenoso"],
        "profundidadM": (2.0, 2.0),
        "estaciones": ["E5"],
        "distribucion": "Carolina del Norte hasta Venezuela y Brasil",
        "descripcion": (
            "Quelípedo izquierdo mucho mayor que el derecho con HACES DE SETAS, "
            "particularmente sobre la palma. Ápice de los dedos de apariencia CÓRNEA "
            "(no calcárea, a diferencia de Calcinus). Escudo casi tan largo como ancho "
            "con superficie irregular. Especie poco frecuente en la Península de Macanao."
        ),
        "color": "#43A047",
        "notaIdentificacion": "Quelípedo izquierdo con HACES DE SETAS en palma + ápice córneo (no calcáreo).",
    },
}

CLAVES_CARACTERES = [
    "pleopodosPrimerSomito",
    "flageloSetasLargas",
    "quelipedosIguales",
    "quelipedoIzquierdoMayor",
    "dedosCuchara",
    "caparazonReticulado",
    "dactiloMayorPropodo",
    "bandaLongitudinalClara",
    "bandasTransversasRojas",
    "quelipedoDerechoLigeramenteMayor",
    "quelipedoIzqMuchoMayor",
    "quelipedoLiso",
    "hacesSetasPalma",
]

_especiesUsuario = {}


def cargarEspeciesUsuario():
    global _especiesUsuario
    if os.path.exists(RUTA_JSON_USUARIO):
        try:
            with open(RUTA_JSON_USUARIO, "r", encoding="utf-8") as f:
                data = json.load(f)
                for nombre, info in data.items():
                    if "profundidadM" in info and isinstance(info["profundidadM"], list):
                        info["profundidadM"] = tuple(info["profundidadM"])
                _especiesUsuario = data
        except (json.JSONDecodeError, IOError):
            _especiesUsuario = {}
    else:
        _especiesUsuario = {}


def guardarEspeciesUsuario():
    global _especiesUsuario
    data = {}
    for nombre, info in _especiesUsuario.items():
        d = dict(info)
        if isinstance(d.get("profundidadM"), tuple):
            d["profundidadM"] = list(d["profundidadM"])
        data[nombre] = d
    try:
        with open(RUTA_JSON_USUARIO, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def obtenerTodasLasEspecies():
    especies = dict(ESPECIES)
    especies.update(_especiesUsuario)
    return especies


def agregarEspecieUsuario(nombre, datos):
    global _especiesUsuario
    _especiesUsuario[nombre] = datos
    guardarEspeciesUsuario()


def eliminarEspecieUsuario(nombre):
    global _especiesUsuario
    if nombre in _especiesUsuario:
        del _especiesUsuario[nombre]
        guardarEspeciesUsuario()


def esEspecieUsuario(nombre):
    return nombre in _especiesUsuario


def exportarEspeciesAJson(ruta):
    todas = obtenerTodasLasEspecies()
    data = {}
    for nombre, info in todas.items():
        d = dict(info)
        if isinstance(d.get("profundidadM"), tuple):
            d["profundidadM"] = list(d["profundidadM"])
        data[nombre] = d
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def importarEspeciesDeJson(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    for nombre, info in data.items():
        if "profundidadM" in info and isinstance(info["profundidadM"], list):
            info["profundidadM"] = tuple(info["profundidadM"])
        if nombre not in ESPECIES:
            agregarEspecieUsuario(nombre, info)
