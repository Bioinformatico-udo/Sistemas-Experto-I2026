import streamlit as st
import os
import json
import difflib
import base64
import mimetypes
import shutil
from datetime import datetime

# Cargar catálogo desde JSON para facilidad de mantenimiento
catalogo_path = os.path.join(os.path.dirname(__file__), "diccionario.json")
if os.path.exists(catalogo_path):
    with open(catalogo_path, "r", encoding="utf-8") as f:
        CATALOGO_CORALES = json.load(f)
else:
    CATALOGO_CORALES = {}

# Normalizar la estructura de imágenes
for datos in CATALOGO_CORALES.values():
    if isinstance(datos.get("img"), str):
        datos["img"] = [datos["img"]]
    elif datos.get("img") is None:
        datos["img"] = []
    elif not isinstance(datos.get("img"), list):
        datos["img"] = [str(datos.get("img"))]
    datos["img_extra"] = datos["img"][2:]

# --- FUNCIONES DE RESPALDO Y GUARDADO ---
def hacer_respaldo():
    """Crea una copia de seguridad del diccionario antes de modificarlo."""
    if os.path.exists(catalogo_path):
        backup_dir = os.path.join(os.path.dirname(__file__), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"diccionario_backup_{timestamp}.json")
        shutil.copy2(catalogo_path, backup_path)

def guardar_catalogo():
    """Guarda los cambios en el JSON creando un respaldo previo."""
    hacer_respaldo()
    with open(catalogo_path, "w", encoding="utf-8") as f:
        json.dump(CATALOGO_CORALES, f, indent=2, ensure_ascii=False)
# -----------------------------------------------

PAGE_TITLE = "- Sistema Experto: Corales de Mochima 🐚 -"
QUESTIONS = [
    {"field": "familia", "prompt": "¿A qué familia pertenece el coral? Ejemplo: Acroporidae, Mussidae, Poritidae."},
    {"field": "genero", "prompt": "¿A qué género pertenece el coral? Ejemplo: Acropora, Diploria, Porites."},
    {"field": "profundidad_ideal", "prompt": "¿En qué profundidad vive este coral? Responde Somera, Media o Profunda."},
    {"field": "forma", "prompt": "¿Cuál es la forma principal del coral? Responde Ramificado, Masivo o Incrustante."},
    {"field": "complejidad", "prompt": "¿Qué complejidad tiene su cuidado? Responde Baja, Media o Alta."},
]

WELCOME_MESSAGE = (
    "¡Hola! Soy CoralBot. Responde las preguntas taxonómicas una por una y utilizaré mi base de conocimientos para identificar la especie de coral en Mochima. "
    "También puedes escribir nombres comunes o descripciones breves como 'mano de gato', 'cerebro', 'ramas en abanico' o 'zona profunda'. "
    "Puedes escribir respuestas directas como 'Acroporidae', 'Acropora', 'Somera', 'Ramificado' o 'Baja'."
)

RESPONSABLES = [
    {
        "nombre": "Jhon Fernandez",
        "cedula": "32.086.485",
        "github": "https://github.com/Jhon-Fernandez1/Portafolio-Personal",
    },
    {
        "nombre": "Alfonso Cedeño",
        "cedula": "31.241.821",
        "github": "https://github.com/fonchocc/Portafolio-Personal-UDO",
    },
    {
        "nombre": "Roberth Alvarez",
        "cedula": "31.232.207",
        "github": "https://github.com/RoberthAlverez/RoberthAlverez",
    },
]

st.set_page_config(page_title=PAGE_TITLE, layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# --- INICIALIZACIONES DE ESTADO ---
def iniciar_identificacion():
    st.session_state.chat_history = [
        {"role": "assistant", "content": WELCOME_MESSAGE},
        {"role": "assistant", "content": QUESTIONS[0]["prompt"]},
    ]
    st.session_state.taxo_answers = {pregunta["field"]: None for pregunta in QUESTIONS}
    st.session_state.question_index = 0
    st.session_state.identification_done = False
    st.session_state.matches = list(CATALOGO_CORALES.items())

def reset_conversacion():
    iniciar_identificacion()
    st.session_state.page_view = "Chatbot"

def iniciar_cuestionario():
    st.session_state.akinator_respuestas = {}

if "chat_history" not in st.session_state: iniciar_identificacion()
if "akinator_respuestas" not in st.session_state: iniciar_cuestionario()
if "page_view" not in st.session_state: st.session_state.page_view = "Chatbot"
if "question_index" not in st.session_state: st.session_state.question_index = 0
if "taxo_answers" not in st.session_state: st.session_state.taxo_answers = {pregunta["field"]: None for pregunta in QUESTIONS}
if "identification_done" not in st.session_state: st.session_state.identification_done = False
if "matches" not in st.session_state: st.session_state.matches = list(CATALOGO_CORALES.items())
if "is_admin" not in st.session_state: st.session_state.is_admin = False

# Variables de control para limpiar formularios
if "form_add_version" not in st.session_state: st.session_state.form_add_version = 0
if "form_edit_version" not in st.session_state: st.session_state.form_edit_version = 0
if "success_add" not in st.session_state: st.session_state.success_add = ""
if "success_edit" not in st.session_state: st.session_state.success_edit = ""

def mostrar_mensaje(role, content):
    clase = "chat-assistant" if role == "assistant" else "chat-user"
    autor = "CoralBot" if role == "assistant" else "Tú"
    if "<div" not in content:
        html_content = content.replace("\n", "<br>")
    else:
        html_content = content

    st.markdown(
        f"""
        <div class='chat-container'>
            <div class='chat-message {clase}'>
                <div class='chat-meta'>{autor}</div>
                <div>{html_content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def normalized(text): return text.strip().lower()

def normalize_catalog_value(value):
    if isinstance(value, str): return value.strip().title()
    return value

def get_catalog_options(field):
    return sorted({normalize_catalog_value(datos.get(field, "")) for datos in CATALOGO_CORALES.values() if datos.get(field, "")})

def get_image_path(datos, index=0):
    if datos.get("img"):
        if index < len(datos["img"]):
            candidate = datos["img"][index]
            candidate_abs = os.path.join(os.path.dirname(__file__), candidate)
            if os.path.exists(candidate_abs):
                return candidate
        first = datos["img"][0] if datos["img"] else None
        if first:
            first_abs = os.path.join(os.path.dirname(__file__), first)
            if os.path.exists(first_abs):
                return first

    nombre = datos.get("nombre")
    if not nombre:
        posible = datos.get("genero")
        if posible and datos.get("familia"):
            nombre = f"{posible}"

    imagenes_root = os.path.join(os.path.dirname(__file__), "imagenes")
    if os.path.exists(imagenes_root):
        hints = []
        if datos.get("genero"): hints.append(normalized(datos.get("genero")))
        if datos.get("familia"): hints.append(normalized(datos.get("familia")))
        for root, _, files in os.walk(imagenes_root):
            for fname in files:
                low = fname.lower()
                for h in hints:
                    if h and h in low:
                        rel = os.path.relpath(os.path.join(root, fname), os.path.dirname(__file__))
                        return rel.replace("\\", "/")
    return None

def get_image_data_uri(img_path):
    ruta_img = os.path.join(os.path.dirname(__file__), img_path)
    if not os.path.exists(ruta_img): return None
    mime_type, _ = mimetypes.guess_type(ruta_img)
    if not mime_type: mime_type = "image/jpeg"
    with open(ruta_img, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

def format_known_attributes():
    parts = []
    for k, v in st.session_state.taxo_answers.items():
        if v: parts.append(f"<b>{k.capitalize()}</b>: {v}")
    if parts:
        return "<br><span style='font-size:0.85em; color:#555;'>Atributos deducidos: " + ", ".join(parts) + "</span>"
    return ""

def matches_by_clave(text):
    texto = normalized(text)
    if texto in {normalize_catalog_value(f).lower() for f in get_catalog_options('familia')}: return []
    if texto in {normalize_catalog_value(g).lower() for g in get_catalog_options('genero')}: return []

    resultados = []
    for nombre, datos in CATALOGO_CORALES.items():
        for clave in datos.get("claves", []):
            if clave and normalized(clave) in texto:
                resultados.append((nombre, datos))
                break
    return resultados

def parse_taxonomy_answer(field, texto):
    texto = normalized(texto)
    if not texto: return None
    opciones = get_catalog_options(field)
    
    if field in ["familia", "genero"]:
        for opcion in opciones:
            if normalized(opcion) == texto: return opcion
        for opcion in opciones:
            if normalized(opcion) in texto: return opcion
        posible = difflib.get_close_matches(texto.title(), opciones, n=1, cutoff=0.75)
        return posible[0] if posible else None

    if field == "profundidad_ideal":
        if "som" in texto: return "Somera"
        if "medi" in texto: return "Media"
        if "prof" in texto or "deep" in texto: return "Profunda"
        for opcion in opciones:
            if normalized(opcion) in texto: return opcion
        posible = difflib.get_close_matches(texto.title(), opciones, n=1, cutoff=0.6)
        return posible[0] if posible else None

    if field == "forma":
        if "rama" in texto or "branch" in texto: return "Ramificado"
        if "masiv" in texto: return "Masivo"
        if "incr" in texto or "encr" in texto: return "Incrustante"
        if "hemisf" in texto: return "Hemisférico"
        if "columnar" in texto: return "Columnar"
        if "solitario" in texto or "disco" in texto: return "Solitario / Discoidal"
        if "laminar" in texto or "hoja" in texto: return "Laminar"
        for opcion in opciones:
            if normalized(opcion) in texto: return opcion
        posible = difflib.get_close_matches(texto.title(), opciones, n=1, cutoff=0.6)
        return posible[0] if posible else None

    if field == "complejidad":
        if "baj" in texto or "facil" in texto or "fácil" in texto: return "Baja"
        if "medi" in texto or "normal" in texto: return "Media"
        if "alt" in texto or "dif" in texto or "dific" in texto: return "Alta"
        for opcion in opciones:
            if normalized(opcion) in texto: return opcion
        posible = difflib.get_close_matches(texto.title(), opciones, n=1, cutoff=0.6)
        return posible[0] if posible else None

    return None

def infer_shared_attributes(coincidencias, fields):
    shared = {}
    for field in fields:
        valores = [datos.get(field) for _, datos in coincidencias if datos.get(field)]
        if valores and all(v == valores[0] for v in valores):
            shared[field] = valores[0]
    return shared

def parse_attributes_from_text(texto):
    attrs = {}
    fields = ["familia", "genero", "profundidad_ideal", "forma", "complejidad"]
    for field in fields:
        valor = parse_taxonomy_answer(field, texto)
        if valor: attrs[field] = valor

    coincidencias = matches_by_clave(texto)
    if coincidencias:
        if len(coincidencias) == 1:
            _, datos = coincidencias[0]
            for field in fields: attrs[field] = datos.get(field)
        else:
            shared = infer_shared_attributes(coincidencias, fields)
            attrs.update(shared)
    return attrs

def is_likely_species_guess(nombre_guess):
    partes = normalized(nombre_guess).split()
    return len(partes) >= 2

def is_known_family_or_genus(nombre_guess):
    texto = normalized(nombre_guess)
    if texto in {normalize_catalog_value(f).lower() for f in get_catalog_options('familia')}: return True
    if texto in {normalize_catalog_value(g).lower() for g in get_catalog_options('genero')}: return True
    return False

def show_species_info(nombre_guess):
    texto = normalized(nombre_guess)
    nombres = list(CATALOGO_CORALES.keys())

    if is_known_family_or_genus(nombre_guess): return None, None

    for n in nombres:
        if n.lower() == texto: return n, CATALOGO_CORALES[n]

    if not is_likely_species_guess(nombre_guess):
        coincidencias = matches_by_clave(nombre_guess)
        if len(coincidencias) == 1: return coincidencias[0]
        return None, None

    posible = difflib.get_close_matches(nombre_guess.title(), nombres, n=1, cutoff=0.75)
    if posible:
        n = posible[0]
        return n, CATALOGO_CORALES[n]
    return None, None

def inferir_coral_por_taxonomia(familia=None, genero=None, profundidad=None, forma=None, complejidad=None):
    candidatos = []
    for nombre, datos in CATALOGO_CORALES.items():
        if familia:
            familia_data = datos.get("familia", "").lower()
            if familia.lower() not in familia_data and familia_data not in familia.lower(): continue
        if genero:
            genero_data = datos.get("genero", "").lower()
            if genero.lower() not in genero_data and genero_data not in genero.lower(): continue
        if profundidad:
            prof_value = datos.get("profundidad_ideal", "").lower()
            if profundidad.lower() not in prof_value and prof_value not in profundidad.lower(): continue
        if forma:
            forma_value = datos.get("forma", "").lower()
            if forma.lower() not in forma_value and forma_value not in forma.lower(): continue
        if complejidad:
            comp_value = datos.get("complejidad", "").lower()
            if complejidad.lower() not in comp_value and comp_value not in complejidad.lower(): continue
        candidatos.append((nombre, datos))
    return candidatos

def formatear_detalle_exito(nombre, datos, certeza=None):
    html = f"<div class='catalog-card success-card'>"
    
    # Añadimos el encabezado dinámico mostrando la certeza del sistema
    if certeza:
        html += f"<div class='catalog-heading'>¡Especie Identificada con {certeza:.1f}% de certeza! 🎯</div>"
    else:
        html += f"<div class='catalog-heading'>¡Especie Identificada! 🎯</div>"
        
    html += f"<h3 style='margin-top:0;'>{nombre}</h3>"
    img_path = get_image_path(datos, 0)
    if img_path:
        data_uri = get_image_data_uri(img_path)
        if data_uri:
                html += f"<img src='{data_uri}' alt='{nombre}' style='max-width:420px; width:100%; height:auto; object-fit:cover; margin-bottom:12px;'/>"
    html += f"<p>{datos.get('descripcion', '')}</p>"
    html += f"<div class='catalog-note'>"
    html += f"<b>Familia:</b> {datos.get('familia', 'N/A')} | <b>Género:</b> {datos.get('genero', 'N/A')}<br>"
    html += f"<b>Profundidad:</b> {datos.get('profundidad_ideal', 'N/A')} | <b>Forma:</b> {datos.get('forma', 'N/A')}<br>"
    html += f"<b>Complejidad:</b> {datos.get('complejidad', 'N/A')}"
    html += f"</div>"
    html += f"<div class='catalog-note'><b>Estado actual:</b> {datos.get('estado_actual', 'N/A')}</div>"
    html += f"<div class='catalog-note'><b>Morfología:</b> {datos.get('morfologia_detalle', 'N/A')}</div>"
    html += f"</div>"
    return html

def format_catalogo(corales):
    respuesta = "Aquí tienes los corales que coinciden:<br>"
    for nombre, datos in corales:
        respuesta += f"• <b>{nombre}</b>: {datos.get('descripcion', '')[:60]}...<br>"
    return respuesta

def format_match_summary(corales, max_items=6):
    respuesta = f"Quedan {len(corales)} especies posibles:<br>"
    for nombre, _ in corales[:max_items]:
        respuesta += f"• <b>{nombre}</b><br>"
    if len(corales) > max_items:
        respuesta += f"... y {len(corales) - max_items} más.<br>"
    return respuesta

def next_question_text():
    if st.session_state.question_index < len(QUESTIONS):
        return QUESTIONS[st.session_state.question_index]["prompt"]
    return None

def procesar_respuesta_usuario(mensaje):
    if st.session_state.identification_done:
        return "Ya identifiqué un coral. Usa el botón Reiniciar identificación para comenzar de nuevo."

    field = QUESTIONS[st.session_state.question_index]["field"] if st.session_state.question_index < len(QUESTIONS) else None
    
    if field:
        valor = parse_taxonomy_answer(field, mensaje)
        if valor is None:
            attrs = parse_attributes_from_text(mensaje)
            if not attrs:
                return "No entendí tu respuesta. Intenta con una característica válida." + format_known_attributes()
            for k, v in attrs.items(): st.session_state.taxo_answers[k] = v
        else:
            st.session_state.taxo_answers[field] = valor
            st.session_state.question_index += 1
    else:
        attrs = parse_attributes_from_text(mensaje)
        for k, v in attrs.items(): st.session_state.taxo_answers[k] = v

    st.session_state.matches = inferir_coral_por_taxonomia(
        familia=st.session_state.taxo_answers.get("familia"),
        genero=st.session_state.taxo_answers.get("genero"),
        profundidad=st.session_state.taxo_answers.get("profundidad_ideal"),
        forma=st.session_state.taxo_answers.get("forma"),
        complejidad=st.session_state.taxo_answers.get("complejidad")
    )

    if len(st.session_state.matches) == 1:
        st.session_state.identification_done = True
        return formatear_detalle_exito(st.session_state.matches[0][0], st.session_state.matches[0][1])
    
    if len(st.session_state.matches) == 0:
        return "No se encontró un coral con esa combinación. Intenta responder de otra forma o reinicia." + format_known_attributes()

    siguiente = next_question_text()
    texto_res = format_match_summary(st.session_state.matches)
    if siguiente: texto_res += f"<br>Continúa con la siguiente característica:<br>{siguiente}"
    else: texto_res += "<br>No hay más preguntas. Escribe un nombre o describe más."
    
    return texto_res + format_known_attributes()

def responder_pregunta(mensaje):
    texto = normalized(mensaje)
    if not texto: return "Escribe algo para continuar con la identificación."
    if "reiniciar" in texto or "reset" in texto:
        reset_conversacion()
        return "He reiniciado la identificación. " + next_question_text()
    if any(palabra in texto for palabra in ["catálogo", "catalogo", "lista", "mostrar", "ver todos"]):
        return format_catalogo(sorted(CATALOGO_CORALES.items()))
    
    especie_nombre, especie_datos = show_species_info(mensaje)
    if especie_nombre:
        st.session_state.identification_done = True
        return formatear_detalle_exito(especie_nombre, especie_datos)

    return procesar_respuesta_usuario(mensaje)

# --- SISTEMA DE DEDUCCIÓN MORFOLÓGICA AVANZADA (PARA LLEGAR A 1 ESPECIE) ---
def get_coral_traits(nombre, datos):
    """Extrae 15 dimensiones de morfología del coral leyendo el diccionario."""
    forma = datos.get("forma", "").lower()
    genero = datos.get("genero", "")
    fam = datos.get("familia", "")
    desc = datos.get("morfologia_detalle", "").lower() + " " + datos.get("descripcion", "").lower()
    claves = [c.lower() for c in datos.get("claves", [])]

    traits = {}
    
    # 1. Crecimiento general
    if "ramificad" in forma or "arbustivo" in desc: traits["crecimiento"] = "Ramificado"
    elif "laminar" in forma or "hoja" in forma or "hoja" in claves or "lámina" in desc: traits["crecimiento"] = "Laminar"
    elif "solitario" in forma or "discoidal" in forma or "solitario" in claves: traits["crecimiento"] = "Solitario"
    else: traits["crecimiento"] = "Masivo"

    # Detalles si es Ramificado
    if genero == "Acropora":
        traits["axial"] = "Sí"
        traits["forma_ramas"] = "Aplanadas" if "palmata" in nombre.lower() else "Cilíndricas"
    elif genero == "Porites":
        traits["axial"] = "No"
        traits["forma_ramas"] = "Hinchadas" if "porites" in nombre.lower() else "Bifurcadas"
    elif "oculina" in nombre.lower():
        traits["axial"] = "No"
        traits["forma_ramas"] = "Fusionadas"
    elif "mussa" in nombre.lower() or "eusmilia" in nombre.lower():
        traits["axial"] = "No"
        traits["forma_ramas"] = "Copas terminales grandes"

    # Detalles si es Masivo
    if "columnar" in forma: traits["forma_masiva"] = "Columnar"
    elif "hemisférico" in forma or "hemisferico" in forma: traits["forma_masiva"] = "Hemisferico"
    elif "irregular" in claves or "irregular" in desc: traits["forma_masiva"] = "Irregular"
    elif "incrustante" in forma or "costroso" in forma: traits["forma_masiva"] = "Incrustante"
    else: traits["forma_masiva"] = "Montículo estándar"

    # Disposición (Valles / Cerebros vs Circulares)
    if "valles" in desc or "meandroide" in forma or "cerebro" in claves or "surco" in desc:
        traits["disposicion"] = "Valles"
        if "surco ancho" in claves or ("surco" in desc and "diploria" in nombre.lower()): traits["tipo_valles"] = "Con surco profundo"
        elif "afiladas" in desc: traits["tipo_valles"] = "Crestas afiladas"
        elif "dentadas" in desc and "colpophyllia" in nombre.lower(): traits["tipo_valles"] = "Láminas dentadas"
        elif "anchos" in claves: traits["tipo_valles"] = "Valles muy anchos"
        else: traits["tipo_valles"] = "Valles estándar"
    else:
        traits["disposicion"] = "Circulares"

    # Paredes (Cerioides vs Plocoides)
    if genero in ["Siderastrea", "Favia", "Isophyllastrea", "Stephanocoenia", "Madracis"] or "astreoides" in nombre.lower() or "apiñadas" in desc or "comparten" in desc:
        traits["paredes"] = "Comparten"
        if genero == "Siderastrea":
            traits["pendiente"] = "45 Grados" if "siderea" in nombre.lower() else "Perpendicular"
        if genero == "Stephanocoenia": traits["num_septos"] = "24"
        if genero == "Madracis": traits["num_septos"] = "10"
    else:
        traits["paredes"] = "Separados"
        if genero == "Dichocoenia": traits["forma_caliz"] = "Ovalados"
        else: traits["forma_caliz"] = "Redondos"

    # Tamaño
    if genero in ["Scolymia", "Mussa", "Isophyllastrea", "Eusmilia", "Montastraea"] or "copas grandes" in claves or ("grande" in desc and "6 mm" not in desc) or "mayor a 10 mm" in desc:
        traits["tamano"] = "Mayor 10mm"
    else:
        traits["tamano"] = "Menor 10mm"

    # Septos y Dientes
    if fam == "Meandrinidae" or genero in ["Dichocoenia", "Eusmilia", "Meandrina"] or "lisos" in desc:
        traits["septos"] = "Lisos"
    else:
        traits["septos"] = "Dentados"
        if genero == "Scolymia":
            traits["dientes"] = "Finos" if "cubensis" in nombre.lower() else "Toscos"

    # Detalles si es Laminar
    if traits["crecimiento"] == "Laminar":
        if "juntas" in claves: traits["lamina_detalle"] = "Colinas juntas"
        elif "delgados" in claves: traits["lamina_detalle"] = "Septos delgados"
        elif "gruesos" in claves or "mycetophyllia" in nombre.lower(): traits["lamina_detalle"] = "Septos gruesos"

    # Columela
    if "columela" in desc or fam in ["Astrocoeniidae", "Poritidae"]:
        traits["columela"] = "Presente"
    else:
        traits["columela"] = "Ausente"

    return traits

# Jerarquía Estricta Dicotómica y Morfológica
PREGUNTAS_AKINATOR = [
    {
        "id": "crecimiento",
        "texto": "1. Forma general de la colonia\n¿Cuál es la forma principal de crecimiento de la colonia?",
        "opciones": [("Ramificado", "Ramificado (Árbol/Arbusto)"), ("Masivo", "Masivo/Incrustante (Roca)"), ("Laminar", "Laminar (Hojas)"), ("Solitario", "Solitario (Un pólipo)")]
    },
    {
        "id": "axial",
        "texto": "2. Estructura de las puntas\n¿Las ramas terminan en un único cáliz central prominente (axial)?",
        "condicion": lambda r: r.get("crecimiento") == "Ramificado",
        "opciones": [("Sí", "Sí, un cáliz central"), ("No", "No, múltiples cálices")]
    },
    {
        "id": "forma_ramas",
        "texto": "3. Morfología de las ramas\n¿Qué aspecto específico tienen las ramas de la colonia?",
        "condicion": lambda r: r.get("crecimiento") == "Ramificado",
        "opciones": [("Aplanadas", "Aplanadas (Orejones)"), ("Cilíndricas", "Cilíndricas"), ("Hinchadas", "Puntas hinchadas"), ("Bifurcadas", "Puntas bifurcadas"), ("Fusionadas", "Cortas y fusionadas"), ("Copas terminales grandes", "Terminan en copas enormes")]
    },
    {
        "id": "forma_masiva",
        "texto": "4. Tipo de crecimiento masivo\n¿Qué perfil específico forma la colonia sólida?",
        "condicion": lambda r: r.get("crecimiento") == "Masivo",
        "opciones": [("Columnar", "Forma columnas estrechas"), ("Hemisferico", "Montículos hemisféricos"), ("Irregular", "Superficie irregular con bultos"), ("Incrustante", "Costra fina sobre la roca"), ("Montículo estándar", "Montículo masivo común")]
    },
    {
        "id": "disposicion",
        "texto": "5. Disposición de los cálices (Corallites)\n¿La superficie presenta valles continuos (tipo cerebro) o cálices circulares individuales?",
        "condicion": lambda r: r.get("crecimiento") in ["Masivo", "Laminar"],
        "opciones": [("Valles", "Valles continuos (Meandroide)"), ("Circulares", "Cálices circulares individuales")]
    },
    {
        "id": "tipo_valles",
        "texto": "6. Estructura de los valles\n¿Qué característica distintiva tienen los valles de este coral cerebro?",
        "condicion": lambda r: r.get("disposicion") == "Valles",
        "opciones": [("Con surco profundo", "Paredes con un surco arriba"), ("Crestas afiladas", "Paredes con crestas afiladas"), ("Láminas dentadas", "Láminas dentadas en el fondo"), ("Valles muy anchos", "Valles inusualmente anchos"), ("Valles estándar", "Valles sinuosos regulares")]
    },
    {
        "id": "paredes",
        "texto": "7. Estructura de las paredes\n¿Los cálices comparten sus paredes directamente o están separados por tejido?",
        "condicion": lambda r: r.get("disposicion") == "Circulares",
        "opciones": [("Comparten", "Comparten paredes (Cerioides)"), ("Separados", "Separados por tejido (Plocoides)")]
    },
    {
        "id": "pendiente",
        "texto": "8. Inclinación de los septos\n¿Cómo caen los septos (estrellas) hacia el centro de la copa?",
        "condicion": lambda r: r.get("paredes") == "Comparten" and r.get("crecimiento") == "Masivo",
        "opciones": [("45 Grados", "En pendiente de 45°"), ("Perpendicular", "Caen perpendiculares")]
    },
    {
        "id": "num_septos",
        "texto": "9. Número de septos\n¿El coralito tiene un número de septos fijo y distintivo?",
        "condicion": lambda r: r.get("paredes") == "Comparten",
        "opciones": [("10", "Exactamente 10 septos"), ("24", "Exactamente 24 septos"), ("Variable", "Cantidad superior/variable")]
    },
    {
        "id": "forma_caliz",
        "texto": "10. Forma del cáliz\n¿Los cálices aislados son perfectamente redondos u ovalados/alargados?",
        "condicion": lambda r: r.get("paredes") == "Separados",
        "opciones": [("Redondos", "Completamente redondos"), ("Ovalados", "Ovalados o alargados")]
    },
    {
        "id": "lamina_detalle",
        "texto": "11. Detalles de la lámina\n¿Qué caracteriza a las líneas (septos/colinas) de esta forma de hoja?",
        "condicion": lambda r: r.get("crecimiento") == "Laminar",
        "opciones": [("Colinas juntas", "Colinas extremadamente juntas"), ("Septos delgados", "Septos finos y alternados"), ("Septos gruesos", "Septos tan o más gruesos que los espacios")]
    },
    {
        "id": "tamano",
        "texto": "12. Tamaño de los cálices\n¿El diámetro mide más de 10 mm (pólipo grande) o menos de 10 mm (pólipo pequeño)?",
        "opciones": [("Mayor 10mm", "Más de 10 mm"), ("Menor 10mm", "Menos de 10 mm")]
    },
    {
        "id": "septos",
        "texto": "13. Bordes de los Septos\n¿Los bordes superiores de los septos son lisos o presentan dientes/espinas?",
        "opciones": [("Lisos", "Completamente lisos"), ("Dentados", "Presentan dientes")]
    },
    {
        "id": "dientes",
        "texto": "14. Textura de los dientes\n¿Los dientes son finos (como agujas) o toscos (como pirámides gruesas)?",
        "condicion": lambda r: r.get("crecimiento") == "Solitario" or r.get("septos") == "Dentados",
        "opciones": [("Finos", "Dientes finos"), ("Toscos", "Dientes toscos o gruesos")]
    },
    {
        "id": "columela",
        "texto": "15. Presencia de Columela\n¿El fondo del cáliz tiene una estructura (esponjosa/sólida) en el centro o está vacío?",
        "opciones": [("Presente", "Columela presente"), ("Ausente", "Centro hueco/vacío")]
    }
]

with st.sidebar:
    # --- SECCIÓN DEL LOGO ---
    ruta_logo = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(ruta_logo): st.image(ruta_logo, use_container_width=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #160211;'>🪸 CoralBot</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='margin-top: 0; border: none; border-top: 1px solid #D0E3FF;'>", unsafe_allow_html=True)
    
    # --- BOTONES PRINCIPALES ---
    if st.button("📖 Catálogo", use_container_width=True): st.session_state.page_view = "Catálogo"
    if st.button("💬 Chatbot", use_container_width=True): st.session_state.page_view = "Chatbot"
    
    # --- NUEVO BOTÓN CUESTIONARIO ---
    if st.button("🧠 Cuestionario", use_container_width=True): 
        st.session_state.page_view = "Cuestionario"
        iniciar_cuestionario()

    if st.button("🛠️ Responsables", use_container_width=True):
        st.session_state.page_view = "Soporte"

    st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px solid #D0E3FF;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #160211;'>🔒 Modo Administrador</h4>", unsafe_allow_html=True)
    
    # --- LÓGICA DE LOGIN DESPLEGABLE ---
    if not st.session_state.is_admin:
        with st.expander("🔑 Iniciar Sesión", expanded=False):
            admin_user = st.text_input("Usuario:", key="admin_user")
            admin_pass = st.text_input("Contraseña:", type="password", key="admin_pass")
            if st.button("Ingresar", use_container_width=True):
                # Validación de credenciales
                if admin_user == "admin" and admin_pass == "admin123":
                    st.session_state.is_admin = True
                    st.success("Sesión iniciada correctamente.")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
    else:
        st.success("👨‍💻 Admin Autenticado")
        st.markdown(f"**Usuario:** `{st.session_state.get('admin_user', 'admin')}`")
        st.markdown(f"**Rol:** `Administrador`")
        
        if st.button("⚙️ Panel de Gestión (CRUD)", use_container_width=True): 
            st.session_state.page_view = "Admin"
        if st.button("🔴 Cerrar Sesión", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.page_view = "Chatbot"
            st.rerun()

# --- VISTA: SOPORTE Y RESPONSABLES ---
if st.session_state.page_view == "Soporte":
    st.title("🛠️ Soporte y Responsables")
    st.write("Equipo responsable del desarrollo y mantenimiento de CoralBot.")

    for responsable in RESPONSABLES:
        st.markdown(f"### {responsable['nombre']}")
        st.write(f"Cédula de Identidad: {responsable['cedula']}")
        st.markdown(f"GitHub: [{responsable['github']}]({responsable['github']})")
        st.markdown("---")

    st.info("Si necesitas ayuda, reportar un problema o colaborar con el proyecto, puedes contactar a cualquiera de los responsables.")

# --- VISTA: PANEL DE ADMINISTRADOR ---
elif st.session_state.page_view == "Admin" and st.session_state.is_admin:
    st.title("⚙️ Panel de Administración del Diccionario")
    st.write("Gestiona las especies de corales. Cualquier cambio creará un respaldo automático del diccionario.")
    
    tab_add, tab_edit, tab_delete = st.tabs(["➕ Agregar Especie", "✏️ Editar Especie", "🗑️ Eliminar Especie"])
    
    # PESTAÑA: AGREGAR
    with tab_add:
        st.subheader("Agregar una nueva especie")
        if st.session_state.success_add:
            st.success(st.session_state.success_add)
            st.session_state.success_add = ""
            
        v_add = st.session_state.form_add_version
        with st.form("form_add"):
            c1, c2 = st.columns(2)
            new_nombre = c1.text_input("Nombre Científico (Ej: Acropora palmata)*", key=f"add_nombre_{v_add}")
            new_familia = c2.text_input("Familia*", key=f"add_familia_{v_add}")
            new_genero = c1.text_input("Género*", key=f"add_genero_{v_add}")
            new_profundidad = c2.selectbox("Profundidad Ideal", ["Somera (0-5 metros)", "Media (5-15 metros)", "Profunda (15+ metros)", "Somera a Media", "Media a Profunda"], key=f"add_prof_{v_add}")
            new_forma = c1.selectbox("Forma Principal", ["Ramificado", "Masivo", "Incrustante", "Hemisférico", "Columnar", "Solitario / Discoidal", "Laminar"], key=f"add_forma_{v_add}")
            new_complejidad = c2.selectbox("Complejidad de Cuidado", ["Baja", "Media", "Alta"], key=f"add_comp_{v_add}")
            
            new_desc = st.text_area("Descripción General", key=f"add_desc_{v_add}")
            new_claves = st.text_input("Palabras Clave (Separadas por comas. Ej: coral, cerebro, ramoso)", key=f"add_claves_{v_add}")
            new_estado = st.text_area("Estado Actual", key=f"add_estado_{v_add}")
            new_morfo = st.text_area("Morfología Detallada", key=f"add_morfo_{v_add}")
            
            submit_add = st.form_submit_button("Guardar Nueva Especie")
            if submit_add:
                if new_nombre and new_familia and new_genero:
                    CATALOGO_CORALES[new_nombre] = {
                        "descripcion": new_desc,
                        "img": [],
                        "familia": new_familia.strip(),
                        "genero": new_genero.strip(),
                        "profundidad_ideal": new_profundidad,
                        "forma": new_forma,
                        "complejidad": new_complejidad,
                        "claves": [c.strip() for c in new_claves.split(",") if c.strip()],
                        "estado_actual": new_estado,
                        "morfologia_detalle": new_morfo
                    }
                    guardar_catalogo()
                    st.session_state.success_add = f"¡La especie '{new_nombre}' fue agregada exitosamente!"
                    st.session_state.form_add_version += 1
                    st.rerun()
                else:
                    st.error("Los campos marcados con * son obligatorios.")

    # PESTAÑA: EDITAR
    with tab_edit:
        st.subheader("Editar especie existente")
        if st.session_state.success_edit:
            st.success(st.session_state.success_edit)
            st.session_state.success_edit = ""
            
        lista_especies = sorted(CATALOGO_CORALES.keys())
        if lista_especies:
            especie_a_editar = st.selectbox("Selecciona la especie a editar:", lista_especies, key="sel_edit")
            datos_edit = CATALOGO_CORALES[especie_a_editar]
            
            v_edit = st.session_state.form_edit_version
            with st.form("form_edit"):
                c1, c2 = st.columns(2)
                edit_familia = c1.text_input("Familia", value=datos_edit.get("familia", ""), key=f"edit_fam_{v_edit}_{especie_a_editar}")
                edit_genero = c2.text_input("Género", value=datos_edit.get("genero", ""), key=f"edit_gen_{v_edit}_{especie_a_editar}")
                
                opciones_prof = ["Somera (0-5 metros)", "Media (5-15 metros)", "Profunda (15+ metros)", "Somera a Media", "Media a Profunda"]
                prof_actual = datos_edit.get("profundidad_ideal", "")
                if prof_actual not in opciones_prof: opciones_prof.append(prof_actual)
                edit_prof = c1.selectbox("Profundidad Ideal", opciones_prof, index=opciones_prof.index(prof_actual) if prof_actual in opciones_prof else 0, key=f"edit_prof_{v_edit}_{especie_a_editar}")
                
                opciones_forma = ["Ramificado", "Masivo", "Incrustante", "Hemisférico", "Columnar", "Solitario / Discoidal", "Laminar"]
                forma_actual = datos_edit.get("forma", "")
                if forma_actual not in opciones_forma: opciones_forma.append(forma_actual)
                edit_forma = c2.selectbox("Forma Principal", opciones_forma, index=opciones_forma.index(forma_actual) if forma_actual in opciones_forma else 0, key=f"edit_forma_{v_edit}_{especie_a_editar}")
                
                comp_actual = datos_edit.get("complejidad", "Baja")
                edit_comp = c1.selectbox("Complejidad", ["Baja", "Media", "Alta"], index=["Baja", "Media", "Alta"].index(comp_actual) if comp_actual in ["Baja", "Media", "Alta"] else 0, key=f"edit_comp_{v_edit}_{especie_a_editar}")
                edit_claves = c2.text_input("Palabras Clave (Separadas por comas)", value=", ".join(datos_edit.get("claves", [])), key=f"edit_claves_{v_edit}_{especie_a_editar}")
                edit_desc = st.text_area("Descripción", value=datos_edit.get("descripcion", ""), key=f"edit_desc_{v_edit}_{especie_a_editar}")
                edit_estado = st.text_area("Estado Actual", value=datos_edit.get("estado_actual", ""), key=f"edit_estado_{v_edit}_{especie_a_editar}")
                edit_morfo = st.text_area("Morfología Detallada", value=datos_edit.get("morfologia_detalle", ""), key=f"edit_morfo_{v_edit}_{especie_a_editar}")
                
                submit_edit = st.form_submit_button("Actualizar Especie")
                if submit_edit:
                    CATALOGO_CORALES[especie_a_editar].update({
                        "descripcion": edit_desc,
                        "familia": edit_familia,
                        "genero": edit_genero,
                        "profundidad_ideal": edit_prof,
                        "forma": edit_forma,
                        "complejidad": edit_comp,
                        "claves": [c.strip() for c in edit_claves.split(",") if c.strip()],
                        "estado_actual": edit_estado,
                        "morfologia_detalle": edit_morfo
                    })
                    guardar_catalogo()
                    st.session_state.success_edit = f"¡La especie '{especie_a_editar}' fue actualizada exitosamente!"
                    st.session_state.form_edit_version += 1
                    st.rerun()
        else:
            st.info("No hay especies en el diccionario.")

    # PESTAÑA: ELIMINAR
    with tab_delete:
        st.subheader("Eliminar especie del diccionario")
        lista_especies_del = sorted(CATALOGO_CORALES.keys())
        if lista_especies_del:
            especie_a_borrar = st.selectbox("Selecciona la especie a eliminar:", lista_especies_del, key="sel_del")
            st.warning(f"⚠️ Estás a punto de eliminar a **{especie_a_borrar}**. Se creará un respaldo antes de borrar.")
            if st.button("🗑️ Confirmar Eliminación", type="primary"):
                del CATALOGO_CORALES[especie_a_borrar]
                guardar_catalogo()
                st.success(f"Especie '{especie_a_borrar}' eliminada.")
                st.rerun()
        else:
            st.info("No hay especies en el diccionario.")

# --- VISTA: CATÁLOGO ---
elif st.session_state.page_view == "Catálogo":
    st.title("Catálogo de Corales")
    if not CATALOGO_CORALES:
        st.warning("El catálogo está vacío.")
    else:
        query = st.text_input("Buscar corales (nombre, familia, género, palabras clave)")
        norm_q = normalized(query) if query else ""

        def matches_query(nombre, datos, q):
            if not q: return True
            if q in normalized(nombre) or q in normalized(datos.get("familia", "")) or q in normalized(datos.get("genero", "")) or q in normalized(datos.get("descripcion", "")): return True
            for clave in datos.get("claves", []):
                if q in normalized(clave): return True
            return False

        filtered = [item for item in sorted(CATALOGO_CORALES.items(), key=lambda x: x[0].lower()) if matches_query(item[0], item[1], norm_q)]

        if not filtered: st.info("No se encontraron corales que coincidan con la búsqueda.")
        for nombre, datos in filtered:
            img_path = get_image_path(datos, 0)
            img_html = ""
            if img_path:
                data_uri = get_image_data_uri(img_path)
                if data_uri:
                    img_html = f"<div class='card-thumb'><img src='{data_uri}' alt='{nombre}'/></div>"

            card_html = (
                f"<div class='catalog-card'>"
                f"<div style='display:flex; align-items:flex-start; gap:12px;'>"
                f"{img_html}"
                f"<div style='flex:1;'>"
                f"<div class='catalog-heading'>{nombre}</div>"
                f"<div>{datos.get('descripcion', '')}</div>"
                f"<div class='catalog-note'>Familia: <b>{datos.get('familia', 'N/A')}</b> | Género: <b>{datos.get('genero', 'N/A')}</b> | Prof: <b>{datos.get('profundidad_ideal', 'N/A')}</b><br>Forma: <b>{datos.get('forma', 'N/A')}</b> | Complejidad: <b>{datos.get('complejidad', 'N/A')}</b></div>"
                f"</div></div></div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)

# --- VISTA: CUESTIONARIO (AKINATOR BIOLÓGICO EXPERTO) ---
elif st.session_state.page_view == "Cuestionario":
    st.title("🧠 Cuestionario Experto Dicotómico")
    st.write("Selecciona las características taxonómicas y morfológicas para deducir de qué especie de coral se trata.")
    
    # 1. Filtrar candidatos según respuestas del usuario
    candidatos_nombres = []
    for nombre, datos in CATALOGO_CORALES.items():
        traits = get_coral_traits(nombre, datos)
        match = True
        for q_id, r_val in st.session_state.akinator_respuestas.items():
            if traits.get(q_id) != r_val:
                match = False
                break
        if match:
            candidatos_nombres.append(nombre)
    
    # 2. Lógica de renderizado final
    if len(candidatos_nombres) == 1:
        # Cálculo de confianza en base al número de preguntas profundas respondidas
        certeza = min(99.9, 85.0 + (len(st.session_state.akinator_respuestas) * 2.3))
        
        nombre = candidatos_nombres[0]
        st.markdown(formatear_detalle_exito(nombre, CATALOGO_CORALES[nombre], certeza), unsafe_allow_html=True)
        if st.button("🔄 Identificar otro coral"):
            iniciar_cuestionario()
            st.rerun()
            
    elif len(candidatos_nombres) == 0:
        st.error("No encontré ningún coral en el diccionario que cumpla con TODAS estas características exactas.")
        if st.button("🔄 Volver a intentar"):
            iniciar_cuestionario()
            st.rerun()
            
    else:
        # 3. Buscar la siguiente pregunta válida que realmente divida el grupo restante
        pregunta_actual = None
        for p in PREGUNTAS_AKINATOR:
            if p["id"] not in st.session_state.akinator_respuestas:
                # Comprueba las condiciones lógicas en cascada (ej: No preguntar por tipo de valles si no es masivo)
                if "condicion" not in p or p["condicion"](st.session_state.akinator_respuestas):
                    
                    # Verificamos si esta característica existe y divide a los candidatos restantes
                    valores_presentes = set()
                    for c in candidatos_nombres:
                        t = get_coral_traits(c, CATALOGO_CORALES[c])
                        valores_presentes.add(t.get(p["id"]))
                        
                    if len(valores_presentes) > 1:
                        pregunta_actual = p
                        break
                    elif len(valores_presentes) == 1:
                        # Auto-completar la respuesta ya que todos los corales restantes comparten este rasgo
                        val = valores_presentes.pop()
                        st.session_state.akinator_respuestas[p["id"]] = val
                        st.rerun()
                        
        # 4. Renderizar la pregunta dinámica
        if pregunta_actual:
            st.markdown(f"### {pregunta_actual['texto']}")
            st.write(f"*(Quedan {len(candidatos_nombres)} especies posibles en mi base de datos)*")
            
            # Ajustar dinámicamente las columnas al número de opciones disponibles para este rasgo
            cols = st.columns(len(pregunta_actual["opciones"]))
            for idx, (val, label) in enumerate(pregunta_actual["opciones"]):
                if cols[idx].button(label, use_container_width=True):
                    st.session_state.akinator_respuestas[pregunta_actual["id"]] = val
                    st.rerun()
            
            if len(st.session_state.akinator_respuestas) > 0:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("↩️ Deshacer última respuesta"):
                    last_key = list(st.session_state.akinator_respuestas.keys())[-1]
                    del st.session_state.akinator_respuestas[last_key]
                    st.rerun()
        else:
            st.warning("Las especies restantes comparten las mismas características base. No puedo reducirlas más:")
            for c in candidatos_nombres:
                st.write(f"🔹 **{c}**")
            if st.button("🔄 Volver a intentar"):
                iniciar_cuestionario()
                st.rerun()

# --- VISTA: CHATBOT (PRINCIPAL) ---
else:
    st.title(PAGE_TITLE)
    st.write("Según tus respuestas, evaluaré las características mediante árboles de decisión para clasificar la especie.")

    if hasattr(st, "chat_input"):
        user_message = st.chat_input("Escribe tu respuesta...")
    else:
        user_message = st.text_input("Escribe tu respuesta...")

    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        respuesta = responder_pregunta(user_message)
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

    for mensaje in st.session_state.chat_history:
        mostrar_mensaje(mensaje["role"], mensaje["content"])
        
    if len(st.session_state.chat_history) > 2:
        if st.button("Reiniciar chat (Borrar historial)"):
            reset_conversacion()
            st.rerun()