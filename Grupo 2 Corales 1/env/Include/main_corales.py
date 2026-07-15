import streamlit as st
import os
import json
import difflib
import base64
import mimetypes

# Cargar catálogo desde JSON para facilidad de mantenimiento
catalogo_path = os.path.join(os.path.dirname(__file__), "diccionario.json")
if os.path.exists(catalogo_path):
    with open(catalogo_path, "r", encoding="utf-8") as f:
        CATALOGO_CORALES = json.load(f)
else:
    CATALOGO_CORALES = {}

# Normalizar la estructura de imágenes: admitimos una ruta o una lista de rutas.
for datos in CATALOGO_CORALES.values():
    if isinstance(datos.get("img"), str):
        datos["img"] = [datos["img"]]
    elif datos.get("img") is None:
        datos["img"] = []
    elif not isinstance(datos.get("img"), list):
        datos["img"] = [str(datos.get("img"))]
    datos["img_extra"] = datos["img"][2:]

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

st.set_page_config(page_title=PAGE_TITLE, layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

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

if "chat_history" not in st.session_state:
    iniciar_identificacion()

if "page_view" not in st.session_state:
    st.session_state.page_view = "Chatbot"

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "taxo_answers" not in st.session_state:
    st.session_state.taxo_answers = {pregunta["field"]: None for pregunta in QUESTIONS}

if "identification_done" not in st.session_state:
    st.session_state.identification_done = False

if "matches" not in st.session_state:
    st.session_state.matches = list(CATALOGO_CORALES.items())

def mostrar_mensaje(role, content):
    clase = "chat-assistant" if role == "assistant" else "chat-user"
    autor = "CoralBot" if role == "assistant" else "Tú"
    # Solo reemplazamos saltos de línea si no es un HTML ya estructurado
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

def normalized(text):
    return text.strip().lower()


def normalize_catalog_value(value):
    if isinstance(value, str):
        return value.strip().title()
    return value


def get_catalog_options(field):
    return sorted({normalize_catalog_value(datos.get(field, "")) for datos in CATALOGO_CORALES.values() if datos.get(field, "")})


def get_image_path(datos, index=0):
    # Prefer explicit paths from the catalog when they exist.
    if datos.get("img"):
        if index < len(datos["img"]):
            candidate = datos["img"][index]
            candidate_abs = os.path.join(os.path.dirname(__file__), candidate)
            if os.path.exists(candidate_abs):
                return candidate
        # fallback to first declared image if present and exists
        first = datos["img"][0] if datos["img"] else None
        if first:
            first_abs = os.path.join(os.path.dirname(__file__), first)
            if os.path.exists(first_abs):
                return first

    # If the declared paths don't exist, try to locate an image by species/genera name
    nombre = None
    if datos.get("nombre"):
        nombre = datos.get("nombre")
    # try to infer name from the key by inspecting familia/genero/descripcion
    if not nombre:
        posible = datos.get("genero")
        if posible and datos.get("familia"):
            nombre = f"{posible}"

    # search the imagenes folder recursively for a file that matches genus or species hints
    imagenes_root = os.path.join(os.path.dirname(__file__), "imagenes")
    if os.path.exists(imagenes_root):
        hints = []
        if datos.get("genero"):
            hints.append(normalized(datos.get("genero")))
        if datos.get("familia"):
            hints.append(normalized(datos.get("familia")))
        # also try species-like keys in catalog (some entries use description words)
        # iterate files and match any hint token in filename
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
    if not os.path.exists(ruta_img):
        return None
    mime_type, _ = mimetypes.guess_type(ruta_img)
    if not mime_type:
        mime_type = "image/jpeg"
    with open(ruta_img, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def format_known_attributes():
    parts = []
    for k, v in st.session_state.taxo_answers.items():
        if v:
            parts.append(f"<b>{k.capitalize()}</b>: {v}")
    if parts:
        return "<br><span style='font-size:0.85em; color:#555;'>Atributos deducidos: " + ", ".join(parts) + "</span>"
    return ""


def matches_by_clave(text):
    texto = normalized(text)
    if texto in {normalize_catalog_value(f).lower() for f in get_catalog_options('familia')}:
        return []
    if texto in {normalize_catalog_value(g).lower() for g in get_catalog_options('genero')}:
        return []

    resultados = []
    for nombre, datos in CATALOGO_CORALES.items():
        for clave in datos.get("claves", []):
            if clave and normalized(clave) in texto:
                resultados.append((nombre, datos))
                break
    return resultados


def parse_taxonomy_answer(field, texto):
    texto = normalized(texto)
    if not texto:
        return None

    opciones = get_catalog_options(field)
    if field in ["familia", "genero"]:
        for opcion in opciones:
            if normalized(opcion) == texto:
                return opcion
        for opcion in opciones:
            if normalized(opcion) in texto:
                return opcion
        posible = difflib.get_close_matches(texto.title(), opciones, n=1, cutoff=0.75)
        return posible[0] if posible else None

    if field == "profundidad_ideal":
        if "som" in texto: return "Somera"
        if "medi" in texto: return "Media"
        if "prof" in texto or "deep" in texto: return "Profunda"
        for opcion in opciones:
            if normalized(opcion) in texto:
                return opcion
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
            if normalized(opcion) in texto:
                return opcion
        posible = difflib.get_close_matches(texto.title(), opciones, n=1, cutoff=0.6)
        return posible[0] if posible else None

    if field == "complejidad":
        if "baj" in texto or "facil" in texto or "fácil" in texto: return "Baja"
        if "medi" in texto or "normal" in texto: return "Media"
        if "alt" in texto or "dif" in texto or "dific" in texto: return "Alta"
        for opcion in opciones:
            if normalized(opcion) in texto:
                return opcion
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
        if valor:
            attrs[field] = valor

    coincidencias = matches_by_clave(texto)
    if coincidencias:
        if len(coincidencias) == 1:
            _, datos = coincidencias[0]
            for field in fields:
                attrs[field] = datos.get(field)
        else:
            shared = infer_shared_attributes(coincidencias, fields)
            attrs.update(shared)
    return attrs

def is_likely_species_guess(nombre_guess):
    partes = normalized(nombre_guess).split()
    return len(partes) >= 2


def is_known_family_or_genus(nombre_guess):
    texto = normalized(nombre_guess)
    if texto in {normalize_catalog_value(f).lower() for f in get_catalog_options('familia')}:
        return True
    if texto in {normalize_catalog_value(g).lower() for g in get_catalog_options('genero')}:
        return True
    return False


def get_families_for_genero(genero):
    return {datos.get("familia") for datos in CATALOGO_CORALES.values() if datos.get("genero", "").lower() == genero.lower()}


def get_genera_for_familia(familia):
    return {datos.get("genero") for datos in CATALOGO_CORALES.values() if datos.get("familia", "").lower() == familia.lower()}


def show_species_info(nombre_guess):
    texto = normalized(nombre_guess)
    nombres = list(CATALOGO_CORALES.keys())

    if is_known_family_or_genus(nombre_guess):
        return None, None

    for n in nombres:
        if n.lower() == texto:
            return n, CATALOGO_CORALES[n]

    # Solo tratamos de reconocer nombres científicos completos como especies.
    if not is_likely_species_guess(nombre_guess):
        coincidencias = matches_by_clave(nombre_guess)
        if len(coincidencias) == 1:
            return coincidencias[0]
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
            familia_input = familia.lower()
            if familia_input != familia_data and familia_input not in familia_data and familia_data not in familia_input:
                continue
        if genero:
            genero_data = datos.get("genero", "").lower()
            genero_input = genero.lower()
            if genero_input != genero_data and genero_input not in genero_data and genero_data not in genero_input:
                continue
        if profundidad:
            prof_value = datos.get("profundidad_ideal", "").lower()
            if profundidad.lower() not in prof_value and prof_value not in profundidad.lower():
                continue
        if forma:
            forma_value = datos.get("forma", "").lower()
            if forma.lower() not in forma_value and forma_value not in forma.lower():
                continue
        if complejidad:
            comp_value = datos.get("complejidad", "").lower()
            if complejidad.lower() not in comp_value and comp_value not in complejidad.lower():
                continue
        candidatos.append((nombre, datos))
    return candidatos

def formatear_detalle_exito(nombre, datos):
    html = f"<div class='catalog-card success-card'>"
    html += f"<div class='catalog-heading'>¡Especie Identificada! 🎯</div>"
    html += f"<h3 style='margin-top:0;'>{nombre}</h3>"
    img_path = get_image_path(datos, 0)
    if img_path:
        data_uri = get_image_data_uri(img_path)
        if data_uri:
                html += f"<img src='{data_uri}' alt='{nombre}' style='max-width:420px; width:100%; height:auto; object-fit:cover; margin-bottom:12px;'/>"
    html += f"<p>{datos.get('descripcion', '')}</p>"
    html += f"<div class='catalog-note'>"
    html += f"<b>Familia:</b> {datos.get('familia', 'N/A')} | "
    html += f"<b>Género:</b> {datos.get('genero', 'N/A')}<br>"
    html += f"<b>Profundidad:</b> {datos.get('profundidad_ideal', 'N/A')} | "
    html += f"<b>Forma:</b> {datos.get('forma', 'N/A')}<br>"
    html += f"<b>Complejidad:</b> {datos.get('complejidad', 'N/A')}"
    html += f"</div>"
    html += f"<div class='catalog-note'><b>Estado actual:</b> {datos.get('estado_actual', 'N/A')}</div>"
    html += f"<div class='catalog-note'><b>Morfología:</b> {datos.get('morfologia_detalle', 'N/A')}</div>"
    if datos.get('img_extra'):
        html += f"<div class='catalog-note'><b>Imágenes adicionales:</b> {len(datos.get('img_extra'))} disponibles para enriquecer el conocimiento del sistema.</div>"
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

    if st.session_state.question_index >= len(QUESTIONS):
        attrs = parse_attributes_from_text(mensaje)
        if not attrs:
            return (
                "No quedan preguntas automáticas. "
                "Describe mejor el coral o escribe un nombre científico completo, o usa Reiniciar identificación." 
                + format_known_attributes()
            )

        saved = {}
        for k, v in attrs.items():
            saved[k] = st.session_state.taxo_answers.get(k)
            st.session_state.taxo_answers[k] = v

        st.session_state.matches = inferir_coral_por_taxonomia(
            familia=st.session_state.taxo_answers.get("familia"),
            genero=st.session_state.taxo_answers.get("genero"),
            profundidad=st.session_state.taxo_answers.get("profundidad_ideal"),
            forma=st.session_state.taxo_answers.get("forma"),
            complejidad=st.session_state.taxo_answers.get("complejidad"),
        )

        if len(st.session_state.matches) == 1:
            st.session_state.identification_done = True
            nombre, datos = st.session_state.matches[0]
            return formatear_detalle_exito(nombre, datos)

        if len(st.session_state.matches) == 0:
            for k, old in saved.items():
                st.session_state.taxo_answers[k] = old
            return (
                "No se encontró un coral con esa combinación. Intenta responder de otra forma o reinicia la identificación." 
                + format_known_attributes()
            )

        return (
            format_match_summary(st.session_state.matches)
            + "No hay más preguntas automáticas. Escribe un nombre científico completo o reinicia para empezar de nuevo." 
            + format_known_attributes()
        )

    field = QUESTIONS[st.session_state.question_index]["field"]
    valor = parse_taxonomy_answer(field, mensaje)
    
    if valor is None:
        attrs = parse_attributes_from_text(mensaje)
        if not attrs:
            return (
                "No entendí tu respuesta. Por favor, responde con la característica solicitada.<br>"
                "Puedes escribir el nombre científico, un nombre común o una descripción breve como 'mano de gato', 'coral de cerebro', 'ramas en abanico' o 'zona profunda'.<br>"
                "Ejemplo: Acroporidae, Acropora, Somera, Ramificado o Baja." + format_known_attributes()
            )
        saved = {}
        for k, v in attrs.items():
            saved[k] = st.session_state.taxo_answers.get(k)
            st.session_state.taxo_answers[k] = v

        st.session_state.matches = inferir_coral_por_taxonomia(
            familia=st.session_state.taxo_answers.get("familia"),
            genero=st.session_state.taxo_answers.get("genero"),
            profundidad=st.session_state.taxo_answers.get("profundidad_ideal"),
            forma=st.session_state.taxo_answers.get("forma"),
            complejidad=st.session_state.taxo_answers.get("complejidad"),
        )

        if len(st.session_state.matches) == 0:
            for k, old in saved.items():
                st.session_state.taxo_answers[k] = old
            return (
                "No se encontró un coral con esa combinación. Intenta responder de otra forma.<br><br>"
                + QUESTIONS[st.session_state.question_index]["prompt"]
                + format_known_attributes()
            )

        if field in attrs and st.session_state.taxo_answers.get(field):
            valor = st.session_state.taxo_answers.get(field)
        else:
            if len(st.session_state.matches) == 1:
                st.session_state.identification_done = True
                nombre, datos = st.session_state.matches[0]
                return formatear_detalle_exito(nombre, datos)

            return (
                format_match_summary(st.session_state.matches)
                + "Para descartar, dime otra característica como profundidad, forma o complejidad." 
                + format_known_attributes()
            )

    st.session_state.taxo_answers[field] = valor
    st.session_state.matches = inferir_coral_por_taxonomia(
        familia=st.session_state.taxo_answers.get("familia"),
        genero=st.session_state.taxo_answers.get("genero"),
        profundidad=st.session_state.taxo_answers.get("profundidad_ideal"),
        forma=st.session_state.taxo_answers.get("forma"),
        complejidad=st.session_state.taxo_answers.get("complejidad"),
    )

    if len(st.session_state.matches) == 1:
        st.session_state.identification_done = True
        nombre, datos = st.session_state.matches[0]
        return formatear_detalle_exito(nombre, datos)

    if len(st.session_state.matches) == 0:
        st.session_state.taxo_answers[field] = None
        return (
            "No se encontró un coral con esa combinación. Intenta responder de otra forma.<br><br>"
            + QUESTIONS[st.session_state.question_index]["prompt"]
            + format_known_attributes()
        )

    if field == "familia" and st.session_state.matches:
        # Cuando el usuario ingresa sólo familia, tomarla como filtro sin cerrar la identificación.
        st.session_state.question_index += 1
        if st.session_state.question_index >= len(QUESTIONS):
            return (
                format_match_summary(st.session_state.matches)
                + "Por favor, dime otra característica para seguir descartando dentro de esa familia." 
                + format_known_attributes()
            )
        siguiente = next_question_text()
        return (
            format_match_summary(st.session_state.matches)
            + f"Continúa con la siguiente característica:<br><br>{siguiente}"
            + format_known_attributes()
        )

    st.session_state.question_index += 1
    if st.session_state.question_index >= len(QUESTIONS):
        return (
            format_match_summary(st.session_state.matches)
            + "Aún no es posible identificar una sola especie. Por favor, confirma otra característica para descartar." 
            + format_known_attributes()
        )

    siguiente = next_question_text()
    return (
        format_match_summary(st.session_state.matches)
        + f"Continúa con la siguiente característica:<br><br>{siguiente}"
        + format_known_attributes()
    )

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
        inconsistencias = []
        if st.session_state.taxo_answers.get("familia") and st.session_state.taxo_answers["familia"].lower() not in especie_datos.get("familia", "").lower():
            inconsistencias.append("familia")
        if st.session_state.taxo_answers.get("genero") and st.session_state.taxo_answers["genero"].lower() not in especie_datos.get("genero", "").lower():
            inconsistencias.append("género")
        if inconsistencias:
            campos = " y ".join(inconsistencias)
            return (
                f"La especie propuesta no coincide con el {campos} ya indicado. "
                "Corrige los datos anteriores o reinicia la identificación para evitar errores."
            )
        st.session_state.identification_done = True
        return formatear_detalle_exito(especie_nombre, especie_datos)

    return procesar_respuesta_usuario(mensaje)

with st.sidebar:
    # --- SECCIÓN DEL LOGO ---
    ruta_logo = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, use_container_width=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #160211;'>🪸 CoralBot</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='margin-top: 0; border: none; border-top: 1px solid #D0E3FF;'>", unsafe_allow_html=True)
    
    # Botones estilo Gemini (con iconos)
    if st.button("📖 Catálogo", use_container_width=True): st.session_state.page_view = "Catálogo"
    if st.button("💬 Chatbot", use_container_width=True): st.session_state.page_view = "Chatbot"
    if st.button("🔄 Reiniciar identificación", use_container_width=True): reset_conversacion()

if st.session_state.page_view == "Catálogo":
    st.title("Catálogo de Corales")
    if not CATALOGO_CORALES:
        st.warning("El catálogo está vacío.")
    else:
        # Buscador: filtra por nombre, familia, género, descripción y claves
        query = st.text_input("Buscar corales (nombre, familia, género, palabras clave)")
        norm_q = normalized(query) if query else ""

        def matches_query(nombre, datos, q):
            if not q:
                return True
            if q in normalized(nombre):
                return True
            if q in normalized(datos.get("familia", "")):
                return True
            if q in normalized(datos.get("genero", "")):
                return True
            if q in normalized(datos.get("descripcion", "")):
                return True
            for clave in datos.get("claves", []):
                if q in normalized(clave):
                    return True
            return False

        filtered = [item for item in sorted(CATALOGO_CORALES.items(), key=lambda x: x[0].lower()) if matches_query(item[0], item[1], norm_q)]

        if not filtered:
            st.info("No se encontraron corales que coincidan con la búsqueda.")
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
                f"<div class='catalog-note'><b>Estado actual:</b> {datos.get('estado_actual', 'N/A')}</div>"
                f"<div class='catalog-note'><b>Morfología:</b> {datos.get('morfologia_detalle', 'N/A')}</div>"
                f"</div></div></div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)
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

    # Mostrar los mensajes
    for mensaje in st.session_state.chat_history:
        mostrar_mensaje(mensaje["role"], mensaje["content"])
        
    # Mostrar el botón de Reiniciar chat SOLO si hay más de 2 mensajes (la bienvenida y la 1ra pregunta)
    if len(st.session_state.chat_history) > 2:
        if st.button("Reiniciar chat"):
            reset_conversacion()
            try:
                # Actualizado para soportar las nuevas versiones de Streamlit
                if hasattr(st, "rerun"): st.rerun()
                elif hasattr(st, "experimental_rerun"): st.experimental_rerun()
                else: st.stop()
            except Exception:
                st.stop()