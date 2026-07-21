import copy
import streamlit as st
import json
import numpy as np
import os 
import time 
import shutil
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ==========================================
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="ScleraSys - Corales", page_icon="🪸", layout="wide")

# Inicialización de variables de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = "guest"
if "mostrar_resultados" not in st.session_state:
    st.session_state.mostrar_resultados = False

# Variables de sesión para campos dinámicos
if "extra_morfo_add" not in st.session_state:
    st.session_state.extra_morfo_add = 0
if "extra_eco_add" not in st.session_state:
    st.session_state.extra_eco_add = 0
if "extra_morfo_edit" not in st.session_state:
    st.session_state.extra_morfo_edit = 0
if "extra_eco_edit" not in st.session_state:
    st.session_state.extra_eco_edit = 0

# ==========================================
# FUNCIONES DE GESTIÓN DE DATOS
# ==========================================
def cargar_base_conocimientos(ruta_archivo="corales_cubagua.json"):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        st.error("El archivo JSON tiene un formato inválido.")
        return {}

def guardar_base_conocimientos(datos, ruta_archivo="corales_cubagua.json"):
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error al guardar los datos: {e}")
        return False

def guardar_imagen_especie(uploaded_file, nombre_especie):
    if uploaded_file is None:
        return None
    nombre_base = str(nombre_especie).strip()
    if not nombre_base:
        return None
    extension = os.path.splitext(uploaded_file.name)[1].lower()
    if extension in [".jpg", ".jpeg"]:
        ruta_destino = os.path.join("imagenes", f"{nombre_base}.jpg")
    elif extension == ".png":
        ruta_destino = os.path.join("imagenes", f"{nombre_base}.png")
    else:
        st.warning("Solo se admiten imágenes en formato JPG/JPEG o PNG.")
        return None

    os.makedirs("imagenes", exist_ok=True)
    with open(ruta_destino, "wb") as archivo:
        archivo.write(uploaded_file.getbuffer())
    return ruta_destino

# ==========================================
# FUNCIÓN PARA LA GALERÍA EMERGENTE
# ==========================================
@st.dialog("Galería Fotográfica", width="large")
def abrir_galeria(especie):
    st.markdown(f"<h2 style='text-align: center; color: #1D5277;'>{especie}</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Morfologías y variaciones en su hábitat natural.<br><b>💡 Haz clic sobre cualquier imagen para verla en pantalla completa.</b></p>", unsafe_allow_html=True)
    st.divider()
    
    sufijos = ["", "_2", "_3"]
    imagenes_encontradas = 0
    
    for suf in sufijos:
        ruta_jpg = os.path.join("imagenes", f"{especie}{suf}.jpg")
        ruta_png = os.path.join("imagenes", f"{especie}{suf}.png")
        
        if os.path.exists(ruta_jpg):
            st.image(ruta_jpg, use_container_width=True)
            st.write("") 
            imagenes_encontradas += 1
        elif os.path.exists(ruta_png):
            st.image(ruta_png, use_container_width=True)
            st.write("") 
            imagenes_encontradas += 1
            
    if imagenes_encontradas == 0:
        st.info("Aún no hay imágenes cargadas en la galería para esta especie.")

# ========================
# MOTOR DE INFERENCIA
# ========================
class MotorInferencia:
    def __init__(self, base_conocimientos):
        self.base = base_conocimientos

    def filtrar_dinamico(self, atributos_usuario):
        candidatos = {}
        if not atributos_usuario:
            return candidatos

        for especie, datos in self.base.items():
            atributos_evaluados = 0
            coincidencias = 0
            
            for clave, valor_usuario in atributos_usuario.items():
                if clave in datos and clave != "descripcion":
                    atributos_evaluados += 1
                    valores_bd = datos[clave]
                    
                    if isinstance(valores_bd, str):
                        valores_bd = [valores_bd.lower()]
                    elif isinstance(valores_bd, list):
                        valores_bd = [v.lower() for v in valores_bd]
                    else:
                        continue
                    
                    if valor_usuario.lower() in valores_bd:
                        coincidencias += 1
            
            if atributos_evaluados > 0:
                porcentaje_coincidencia = (coincidencias / atributos_evaluados) * 100
                if porcentaje_coincidencia >= 70.0:
                    datos_candidato = dict(datos)
                    datos_candidato["coincidencia_morfologica"] = porcentaje_coincidencia
                    candidatos[especie] = datos_candidato
                    
        candidatos_ordenados = dict(sorted(candidatos.items(), key=lambda item: item[1]['coincidencia_morfologica'], reverse=True))
        return candidatos_ordenados

# =====================================================================
# LÓGICA DIFUSA ECOLÓGICA-BIOLÓGICA
# =====================================================================
class EvaluadorDifuso:
    def __init__(self):
        self.prof = ctrl.Antecedent(np.arange(0, 31, 1), 'prof')
        self.vis = ctrl.Antecedent(np.arange(0, 21, 1), 'vis')
        self.algas = ctrl.Antecedent(np.arange(0, 101, 1), 'algas')
        self.dist = ctrl.Antecedent(np.arange(0, 601, 1), 'dist')
        
        self.tol_turb = ctrl.Antecedent(np.arange(0, 11, 1), 'tol_turb')
        self.tol_algas = ctrl.Antecedent(np.arange(0, 11, 1), 'tol_algas')
        
        self.confianza = ctrl.Consequent(np.arange(0, 101, 1), 'confianza')

        self.prof['somera'] = fuzz.trimf(self.prof.universe, [0, 0, 12])
        self.prof['media'] = fuzz.trimf(self.prof.universe, [8, 15, 22])
        self.prof['profunda'] = fuzz.trimf(self.prof.universe, [18, 30, 30])

        self.vis['baja'] = fuzz.trimf(self.vis.universe, [0, 0, 8])
        self.vis['media'] = fuzz.trimf(self.vis.universe, [6, 10, 15])
        self.vis['alta'] = fuzz.trimf(self.vis.universe, [12, 20, 20])

        self.algas['baja'] = fuzz.trimf(self.algas.universe, [0, 0, 25])
        self.algas['media'] = fuzz.trimf(self.algas.universe, [15, 50, 85])
        self.algas['alta'] = fuzz.trimf(self.algas.universe, [65, 100, 100])

        self.dist['orilla'] = fuzz.trimf(self.dist.universe, [0, 0, 150])
        self.dist['media'] = fuzz.trimf(self.dist.universe, [100, 300, 500])
        self.dist['lejos'] = fuzz.trimf(self.dist.universe, [400, 600, 600])

        self.tol_turb['baja'] = fuzz.trimf(self.tol_turb.universe, [0, 0, 5])
        self.tol_turb['media'] = fuzz.trimf(self.tol_turb.universe, [0, 5, 10])
        self.tol_turb['alta'] = fuzz.trimf(self.tol_turb.universe, [5, 10, 10])

        self.tol_algas['baja'] = fuzz.trimf(self.tol_algas.universe, [0, 0, 5])
        self.tol_algas['media'] = fuzz.trimf(self.tol_algas.universe, [0, 5, 10])
        self.tol_algas['alta'] = fuzz.trimf(self.tol_algas.universe, [5, 10, 10])

        self.confianza['baja'] = fuzz.trimf(self.confianza.universe, [0, 0, 45])
        self.confianza['media'] = fuzz.trimf(self.confianza.universe, [30, 50, 70])
        self.confianza['alta'] = fuzz.trimf(self.confianza.universe, [60, 100, 100])

        r1 = ctrl.Rule(self.prof['somera'] & self.vis['alta'] & self.algas['baja'] & self.tol_turb['alta'], self.confianza['alta'])
        r2 = ctrl.Rule(self.prof['somera'] & self.vis['alta'] & self.algas['baja'] & self.tol_turb['media'], self.confianza['alta'])
        r3 = ctrl.Rule(self.prof['somera'] & self.vis['alta'] & self.algas['baja'] & self.tol_turb['baja'], self.confianza['media'])
        r4 = ctrl.Rule(self.vis['media'] & self.tol_turb['alta'], self.confianza['alta'])
        r5 = ctrl.Rule(self.vis['media'] & self.tol_turb['media'], self.confianza['media'])
        r6 = ctrl.Rule(self.vis['media'] & self.tol_turb['baja'], self.confianza['baja'])
        r7 = ctrl.Rule(self.vis['baja'] & self.tol_turb['alta'], self.confianza['media'])
        r8 = ctrl.Rule(self.vis['baja'], self.confianza['baja']) 
        r9 = ctrl.Rule(self.algas['media'] & self.tol_algas['alta'], self.confianza['alta'])
        r10 = ctrl.Rule(self.algas['media'] & self.tol_algas['media'], self.confianza['media'])
        r11 = ctrl.Rule(self.algas['media'] & self.tol_algas['baja'], self.confianza['baja'])
        r12 = ctrl.Rule(self.algas['alta'] & self.tol_algas['alta'], self.confianza['media'])
        r13 = ctrl.Rule(self.algas['alta'], self.confianza['baja']) 
        r14 = ctrl.Rule(self.prof['somera'] & self.dist['lejos'], self.confianza['alta'])
        r15 = ctrl.Rule(self.prof['somera'] & self.dist['media'], self.confianza['alta'])
        r16 = ctrl.Rule(self.prof['media'], self.confianza['media'])
        r17 = ctrl.Rule(self.prof['profunda'], self.confianza['baja'])

        self.sistema_control = ctrl.ControlSystem([
            r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17
        ])
        
    def evaluar_certeza(self, prof, vis, algas, dist, str_tol_turb, str_tol_algas):
        simulacion = ctrl.ControlSystemSimulation(self.sistema_control)
        mapa_tolerancias = {"baja": 0.0, "media": 5.0, "alta": 10.0}
        val_turb = mapa_tolerancias.get(str_tol_turb.lower(), 5.0)
        val_algas = mapa_tolerancias.get(str_tol_algas.lower(), 5.0)
        
        try:
            simulacion.input['prof'] = prof
            simulacion.input['vis'] = vis
            simulacion.input['algas'] = algas
            simulacion.input['dist'] = dist
            simulacion.input['tol_turb'] = val_turb
            simulacion.input['tol_algas'] = val_algas
            simulacion.compute()
            return simulacion.output['confianza']
        except Exception as e:
            return 0.0

# =====================================================================
# PANTALLA DE LOGIN
# =====================================================================
if not st.session_state.logged_in:
    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
        with st.container(border=True):
            if os.path.exists("images.png"):
                st.image("images.png", use_container_width=True)
            st.markdown("<h2 style='text-align: center; color: #1D5277;'>Control de Acceso</h2>", unsafe_allow_html=True)
            st.divider()
            
            usuario = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            
            st.write("")
            if st.button("🔑 Ingresar como Administrador", use_container_width=True, type="primary"):
                if usuario == "admin" and password == "udo123":
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
            
            st.divider()
            st.markdown("<p style='text-align: center; color: #666;'>¿No tienes cuenta administrativa?</p>", unsafe_allow_html=True)
            
            if st.button("👤 Ingresar como Visitante", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.role = "guest"
                st.rerun()
                
    st.stop()

# =====================================================================
# INTERFAZ PRINCIPAL (Panel Lateral y Menú)
# =====================================================================
with st.sidebar:
    if os.path.exists("images.png"):
        st.image("images.png", use_container_width=True)
    st.divider()
    
    opciones_menu = ["Sistema Experto", "Catálogo de Especies", "Info"]
    if st.session_state.role == "admin":
        opciones_menu.extend(["Agregar Especie", "Gestionar Especies"])
        
    menu_seleccionado = st.radio("Menú de Navegación:", opciones_menu, index=0)
    st.divider()
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = "guest"
        st.session_state.mostrar_resultados = False
        st.rerun()
        
    st.caption(f"Autenticado como: **{st.session_state.role.upper()}**")

# Carga global
base_datos = cargar_base_conocimientos()

# Constante de claves fijas (para separar las dinámicas)
CLAVES_ESTATICAS = ["nombre_comun", "descripcion", "forma_colonia", "superficie", "tamaño_polipos", "organizacion_coralites", "tipo_gemacion", "tipo_columnela", "tolerancia_turbidez", "tolerancia_algas", "abundancia_local"]

if base_datos is not None:
    motor = MotorInferencia(base_datos)
    evaluador = EvaluadorDifuso()

    # =================================================================
    # VISTA 1: SISTEMA EXPERTO
    # =================================================================
    if menu_seleccionado == "Sistema Experto":
        st.title("🪸 Diagnóstico de Corales Pétreos")
        st.markdown("Sistema de inferencia para ecosistemas bentónicos en la **Isla de Cubagua**.")
        st.write("")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            with st.container(border=True):
                st.markdown("#### 🧬 1. Atributos Morfológicos")
                atributos_evaluar = {}
                forma = st.selectbox("Forma base de la colonia:", ["", "masiva", "ramificada", "incrustante", "laminar", "esferica", "columnar", "arbustiva", "lobulada", "pequeña", "faldones"])
                if forma: atributos_evaluar["forma_colonia"] = forma
                
                superficie = st.selectbox("Textura/Estructura de la superficie:", ["", "cerebriforme", "porosa", "nodular", "lisa", "con copas", "irregular", "bultos", "costillas"])
                if superficie: atributos_evaluar["superficie"] = superficie

                if forma == "ramificada":
                    ram = st.selectbox("Tipo de ramificación específica:", ["", "aplanada", "ancha", "cilindrica", "delgada", "fina", "fusionada", "gruesa", "chata", "corta"])
                    if ram: atributos_evaluar["tipo_ramificacion"] = ram
                    
                if superficie == "cerebriforme":
                    crestas = st.selectbox("Dimensiones de las crestas/valles:", ["", "estrechas", "regulares", "bajas", "anchas con surco", "profundas", "muy anchas", "cortas"])
                    if crestas: atributos_evaluar["anchura_crestas"] = crestas
                    
                if superficie not in ["", "cerebriforme", "hojas"] and forma not in ["laminar"]:
                    polipos = st.selectbox("Tamaño estimado de cálices/pólipos:", ["", "pequeño", "mediano", "grande"])
                    if polipos: atributos_evaluar["tamaño_polipos"] = polipos

                st.divider()
                st.markdown("##### Opcional para desempate taxonómico:")
                org_cor = st.selectbox("Organización de los coralites:", ["", "plocoide", "cerioide", "meandroide"])
                if org_cor: atributos_evaluar["organizacion_coralites"] = org_cor
                
                gemacion = st.selectbox("Tipo de gemación:", ["", "extratentacular", "intratentacular"])
                if gemacion: atributos_evaluar["tipo_gemacion"] = gemacion
                
                colum = st.selectbox("Estructura de la columnela (centro):", ["", "ausente", "trabecular", "papilosa"])
                if colum: atributos_evaluar["tipo_columnela"] = colum

                # --- LECTURA DE ATRIBUTOS DINÁMICOS ---
                st.divider()
                st.markdown("##### 🔬 Características Específicas (Dinámicas)")
                claves_dinamicas_encontradas = set()
                for datos_especie in base_datos.values():
                    for clave_json in datos_especie.keys():
                        if clave_json not in CLAVES_ESTATICAS:
                            claves_dinamicas_encontradas.add(clave_json)
                            
                if claves_dinamicas_encontradas:
                    for clave_dinamica in claves_dinamicas_encontradas:
                        valores_posibles = set()
                        for datos_especie in base_datos.values():
                            if clave_dinamica in datos_especie:
                                for v in datos_especie[clave_dinamica]:
                                    valores_posibles.add(v)
                        
                        titulo_pregunta = clave_dinamica.replace("_", " ").capitalize()
                        seleccion_dinamica = st.selectbox(f"¿Posee {titulo_pregunta}?:", [""] + list(valores_posibles))
                        
                        if seleccion_dinamica:
                            atributos_evaluar[clave_dinamica] = seleccion_dinamica
                else:
                    st.caption("No hay atributos dinámicos adicionales registrados.")

        with col2:
            with st.container(border=True):
                st.markdown("#### 🌊 2. Parámetros del Entorno")
                st.write("Ajuste las condiciones detectadas en el ecosistema.")
                st.write("")
                prof_input = st.slider("Profundidad medida (metros):", 0.0, 30.0, 3.0, 0.5)
                vis_input = st.slider("Visibilidad/Turbidez del agua (metros):", 0.0, 20.0, 15.0, 1.0)
                algas_input = st.slider("Porcentaje de cobertura por macroalgas (%):", 0, 100, 0, 5)
                dist_input = st.slider("Distancia perpendicular a la costa (m):", 0, 600, 100, 10)

        st.write("")
        st.write("")
        
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            analizar = st.button("🔍 Procesar Análisis Experto", type="primary", use_container_width=True)

        if analizar:
            st.session_state.mostrar_resultados = True

        if st.session_state.mostrar_resultados:
            if analizar:
                with st.spinner("Analizando base de conocimientos y calculando lógica difusa..."):
                    time.sleep(1.2)
                    
            resultados = motor.filtrar_dinamico(atributos_evaluar)

            if not resultados:
                st.error("❌ No se encontraron especies que coincidan morfológicamente (Umbral: 70%). Revisa las características.")
            else:
                st.success(f"✅ Análisis completado. Se encontraron {len(resultados)} candidato(s) probable(s):")

                for especie, caracteristicas in resultados.items():
                    coincidencia_porcentaje = caracteristicas.get("coincidencia_morfologica", 0)
                    tol_turb = caracteristicas.get("tolerancia_turbidez", "media")
                    tol_algas = caracteristicas.get("tolerancia_algas", "media")
                    descripcion_coral = caracteristicas.get("descripcion", "Sin ficha técnica registrada en la base de datos.")

                    certeza_ecologica = evaluador.evaluar_certeza(
                        prof_input, vis_input, algas_input, dist_input, tol_turb, tol_algas
                    )

                    with st.expander(f"📌 Resultado: {especie} - {caracteristicas.get('nombre_comun', '')}", expanded=True):
                        with st.container(border=True):
                            col_info, col_img = st.columns([2, 1.5]) 
                            
                            with col_info:
                                st.markdown("#### 🧬 Similitud Morfológica")
                                st.progress(int(coincidencia_porcentaje) / 100.0)
                                st.metric(label="Coincidencia Taxonómica", value=f"{coincidencia_porcentaje:.1f}%")

                                st.divider()

                                st.markdown("#### 🌊 Índice de Certeza Ecológica")
                                st.markdown(f"*(Tolerancia a Turbidez: `{tol_turb.upper()}` | Tolerancia a Algas: `{tol_algas.upper()}`)*")
                                st.progress(int(certeza_ecologica) / 100.0)
                                st.metric(label="Viabilidad del Hábitat", value=f"{certeza_ecologica:.1f}%")
                                
                                st.divider()
                                st.markdown("##### 📝 Ficha Técnica")
                                st.caption(descripcion_coral)
                                
                            with col_img:
                                ruta_jpg = os.path.join("imagenes", f"{especie}.jpg")
                                ruta_png = os.path.join("imagenes", f"{especie}.png")
                                
                                if os.path.exists(ruta_jpg):
                                    st.image(ruta_jpg, caption=f"{especie}", use_container_width=True)
                                elif os.path.exists(ruta_png):
                                    st.image(ruta_png, caption=f"{especie}", use_container_width=True)
                                else:
                                    st.info(f"📸 Imagen no disponible")
                                    
                                if st.button("🖼️ Ver Galería", key=f"btn_galeria_{especie}", use_container_width=True):
                                    abrir_galeria(especie)

    # =================================================================
    # VISTA 2: CATÁLOGO DE ESPECIES
    # =================================================================
    elif menu_seleccionado == "Catálogo de Especies":
        st.title("📚 Catálogo de Especies")
        st.markdown("Explora la base de datos completa de corales registrados en el sistema.")
        st.write("")

        # Filtro de búsqueda en tiempo real
        busqueda = st.text_input("🔍 Buscar por nombre científico o común...", "").lower()
        st.divider()

        # Lógica para filtrar las especies
        especies_filtradas = {}
        for especie, datos in base_datos.items():
            nombre_comun = datos.get("nombre_comun", "").lower()
            if busqueda in especie.lower() or busqueda in nombre_comun:
                especies_filtradas[especie] = datos

        if not especies_filtradas:
            st.info("No se encontraron especies que coincidan con tu búsqueda.")
        else:
            st.caption(f"Mostrando {len(especies_filtradas)} especie(s).")
            
            for especie, datos in especies_filtradas.items():
                nombre_comun = datos.get("nombre_comun", "Sin nombre común")
                
                with st.expander(f"🪸 {especie} ({nombre_comun})"):
                    col_info, col_img = st.columns([2, 1.5])
                    
                    with col_info:
                        st.markdown("##### 📝 Ficha Técnica")
                        st.write(datos.get("descripcion", "Sin descripción disponible."))
                        
                        st.divider()
                        st.markdown("##### 🧬 Características Morfológicas")
                        
                        # Extraer y mostrar de forma limpia todos los atributos
                        for clave, valor in datos.items():
                            if clave not in ["nombre_comun", "descripcion", "tolerancia_turbidez", "tolerancia_algas", "abundancia_local"]:
                                clave_formateada = clave.replace("_", " ").title()
                                valor_str = valor[0] if isinstance(valor, list) and len(valor) > 0 else str(valor)
                                st.markdown(f"- **{clave_formateada}**: {valor_str.capitalize()}")

                        st.divider()
                        st.markdown("##### 🌊 Tolerancias Ecológicas Base")
                        st.markdown(f"- **Tolerancia a Turbidez**: {datos.get('tolerancia_turbidez', 'No definida').title()}")
                        st.markdown(f"- **Tolerancia a Algas**: {datos.get('tolerancia_algas', 'No definida').title()}")

                    with col_img:
                        ruta_jpg = os.path.join("imagenes", f"{especie}.jpg")
                        ruta_png = os.path.join("imagenes", f"{especie}.png")
                        
                        if os.path.exists(ruta_jpg):
                            st.image(ruta_jpg, caption=especie, use_container_width=True)
                        elif os.path.exists(ruta_png):
                            st.image(ruta_png, caption=especie, use_container_width=True)
                        else:
                            st.info("📸 Imagen principal no disponible")
                            
                        if st.button("🖼️ Ver Galería", key=f"cat_galeria_{especie}", use_container_width=True):
                            abrir_galeria(especie)

    # =================================================================
    # VISTA 3: AGREGAR ESPECIE (Solo Admin)
    # =================================================================
    elif menu_seleccionado == "Agregar Especie" and st.session_state.role == "admin":
        st.title("⚙️ Agregar Nueva Especie")
        st.markdown("Agrega nuevas especies a la base de conocimientos `.json` de forma segura.")
        st.write("")
        
        with st.form("form_nueva_especie"):
            st.subheader("Datos Taxonómicos Principales")
            nombre_cientifico = st.text_input("Nombre Científico (Ej: Favia fragum)")
            nombre_comun = st.text_input("Nombre Común")
            descripcion_nueva = st.text_area("Descripción / Ficha Técnica (Datos base)")
            imagen_nueva = st.file_uploader("Imagen asociada a la especie (opcional)", type=["jpg", "jpeg", "png"])
            
            st.divider()
            st.subheader("Atributos Morfológicos (Estáticos)")
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                f_colonia = st.selectbox("Forma de la colonia:", ["masiva", "ramificada", "incrustante", "laminar", "esferica", "columnar", "arbustiva", "lobulada", "pequeña", "faldones"])
                f_superficie = st.selectbox("Superficie:", ["cerebriforme", "porosa", "nodular", "lisa", "con copas", "irregular", "bultos", "costillas"])
                f_polipos = st.selectbox("Tamaño de pólipos:", ["pequeño", "mediano", "grande"])
            with col_form2:
                f_organizacion = st.selectbox("Organización coralites:", ["plocoide", "cerioide", "meandroide"])
                f_gemacion = st.selectbox("Tipo gemación:", ["extratentacular", "intratentacular"])
                f_columnela = st.selectbox("Columnela:", ["ausente", "trabecular", "papilosa"])

            st.divider()
            st.subheader("🧬 Atributos Morfológicos Extra (Dinámicos)")
            st.caption("Añade características que se mostrarán dinámicamente en el Sistema Experto.")
            btn_add_morfo = st.form_submit_button("➕ Añadir nueva característica morfológica")
            if btn_add_morfo: st.session_state.extra_morfo_add += 1
                
            atributos_dinamicos_morfo = {}
            for i in range(st.session_state.extra_morfo_add):
                c1, c2 = st.columns(2)
                with c1: k = st.text_input(f"Característica {i+1} (Ej: color_tentaculo)", key=f"k_m_{i}")
                with c2: v = st.text_input(f"Valor {i+1} (Ej: verde)", key=f"v_m_{i}")
                if k and v: atributos_dinamicos_morfo[k.strip().lower().replace(" ", "_")] = [v.strip().lower()]

            st.divider()
            st.subheader("Tolerancias Ecológicas del Motor Lógico")
            col_tol1, col_tol2 = st.columns(2)
            with col_tol1:
                t_turbidez = st.selectbox("Tolerancia a Turbidez:", ["baja", "media", "alta"])
            with col_tol2:
                t_algas = st.selectbox("Tolerancia a Algas:", ["baja", "media", "alta"])
            
            st.divider()
            st.subheader("🌊 Datos Ecológicos Extra (Dinámicos)")
            st.caption("Estos datos se guardarán automáticamente en la Ficha Técnica para consulta.")
            btn_add_eco = st.form_submit_button("➕ Añadir nueva variable ecológica")
            if btn_add_eco: st.session_state.extra_eco_add += 1

            textos_eco_extra = []
            for i in range(st.session_state.extra_eco_add):
                c1, c2 = st.columns(2)
                with c1: k_e = st.text_input(f"Variable (Ej: Distancia a la costa)", key=f"k_e_{i}")
                with c2: v_e = st.text_input(f"Valor (Ej: 150 metros)", key=f"v_e_{i}")
                if k_e and v_e: textos_eco_extra.append(f"- **{k_e.strip().capitalize()}**: {v_e.strip()}")
                
            st.divider()
            submit_especie = st.form_submit_button("💾 Guardar Especie Completamente", type="primary")
            
            if submit_especie:
                if nombre_cientifico.strip() == "":
                    st.error("El nombre científico es obligatorio.")
                elif nombre_cientifico in base_datos:
                    st.warning("Esta especie ya existe.")
                else:
                    # Anexar textos ecológicos a la descripción
                    if textos_eco_extra:
                        descripcion_final = descripcion_nueva + "\n\n**Parámetros Ecológicos Adicionales:**\n" + "\n".join(textos_eco_extra)
                    else:
                        descripcion_final = descripcion_nueva

                    nueva_especie_datos = {
                        "nombre_comun": nombre_comun,
                        "descripcion": descripcion_final,
                        "forma_colonia": [f_colonia],
                        "superficie": [f_superficie],
                        "tamaño_polipos": [f_polipos],
                        "organizacion_coralites": [f_organizacion],
                        "tipo_gemacion": [f_gemacion],
                        "tipo_columnela": [f_columnela],
                        "tolerancia_turbidez": t_turbidez,
                        "tolerancia_algas": t_algas,
                        "abundancia_local": "comun"
                    }
                    
                    # Añadir diccionarios morfológicos dinámicos
                    nueva_especie_datos.update(atributos_dinamicos_morfo)
                    
                    base_datos[nombre_cientifico.strip()] = nueva_especie_datos
                    
                    if guardar_base_conocimientos(base_datos):
                        if imagen_nueva is not None:
                            guardar_imagen_especie(imagen_nueva, nombre_cientifico.strip())
                        st.session_state.extra_morfo_add = 0
                        st.session_state.extra_eco_add = 0
                        st.success(f"Especie '{nombre_cientifico}' registrada exitosamente.")
                        time.sleep(1.5)
                        st.rerun()

    # =================================================================
    # VISTA 4: GESTIONAR ESPECIES EXISTENTES (Solo Admin)
    # =================================================================
    elif menu_seleccionado == "Gestionar Especies" and st.session_state.role == "admin":
        st.title("🛠️ Gestión de Taxonomía Existente")
        st.markdown("Edita características (estáticas o dinámicas) o elimina registros.")
        st.write("")

        lista_especies = list(base_datos.keys())
        especie_seleccionada = st.selectbox("🔍 Buscar y seleccionar especie:", [""] + lista_especies)

        if especie_seleccionada != "":
            datos_actuales = base_datos[especie_seleccionada]

            st.divider()
            col_titulo, col_eliminar = st.columns([3, 1])
            with col_titulo:
                st.subheader(f"Editando: {especie_seleccionada}")
            with col_eliminar:
                if st.button("🗑️ Eliminar Especie (Auto-Respaldo)", type="primary", use_container_width=True):
                    try:
                        if not os.path.exists("respaldos"): os.makedirs("respaldos")
                        fecha_hora = time.strftime("%Y%m%d_%H%M%S")
                        shutil.copy("corales_cubagua.json", os.path.join("respaldos", f"backup_{fecha_hora}.json"))
                        st.toast("Respaldo automático creado.", icon="💾")
                    except:
                        pass
                    
                    del base_datos[especie_seleccionada]
                    if guardar_base_conocimientos(base_datos):
                        st.success(f"Especie '{especie_seleccionada}' eliminada.")
                        time.sleep(1.5)
                        st.rerun()

            def get_val(clave):
                valor = datos_actuales.get(clave, "")
                if isinstance(valor, list) and len(valor) > 0: return valor[0]
                return valor
            def get_index(opciones, clave):
                val = get_val(clave)
                return opciones.index(val) if val in opciones else 0

            opc_forma = ["masiva", "ramificada", "incrustante", "laminar", "esferica", "columnar", "arbustiva", "lobulada", "pequeña", "faldones"]
            opc_super = ["cerebriforme", "porosa", "nodular", "lisa", "con copas", "irregular", "bultos", "costillas"]
            opc_polipos = ["pequeño", "mediano", "grande"]
            opc_org = ["plocoide", "cerioide", "meandroide"]
            opc_gem = ["extratentacular", "intratentacular"]
            opc_col = ["ausente", "trabecular", "papilosa"]
            opc_tol = ["baja", "media", "alta"]

            with st.form("form_editar_especie"):
                st.text_input("Nombre Científico (Clave Única - No editable)", value=especie_seleccionada, disabled=True)
                nombre_comun_edit = st.text_input("Nombre Común", value=datos_actuales.get("nombre_comun", ""))
                descripcion_edit = st.text_area("Descripción / Ficha Técnica (Aquí se reflejan los datos ecológicos agregados)", value=datos_actuales.get("descripcion", ""), height=150)
                
                st.divider()
                st.markdown("##### Atributos Morfológicos Base")
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    f_colonia = st.selectbox("Forma de la colonia:", opc_forma, index=get_index(opc_forma, "forma_colonia"))
                    f_superficie = st.selectbox("Superficie:", opc_super, index=get_index(opc_super, "superficie"))
                    f_polipos = st.selectbox("Tamaño de pólipos:", opc_polipos, index=get_index(opc_polipos, "tamaño_polipos"))
                with col_form2:
                    f_organizacion = st.selectbox("Organización coralites:", opc_org, index=get_index(opc_org, "organizacion_coralites"))
                    f_gemacion = st.selectbox("Tipo gemación:", opc_gem, index=get_index(opc_gem, "tipo_gemacion"))
                    f_columnela = st.selectbox("Columnela:", opc_col, index=get_index(opc_col, "tipo_columnela"))
                
                st.divider()
                st.markdown("##### 🧬 Atributos Morfológicos Dinámicos Existentes")
                atributos_dinamicos_actualizados = {}
                encontrados = False
                for k, v in datos_actuales.items():
                    if k not in CLAVES_ESTATICAS:
                        encontrados = True
                        val_str = v[0] if isinstance(v, list) and len(v) > 0 else str(v)
                        nuevo_v = st.text_input(f"Editar {k.capitalize()}", value=val_str)
                        if nuevo_v.strip(): atributos_dinamicos_actualizados[k] = [nuevo_v.strip().lower()]
                if not encontrados:
                    st.caption("No tiene características extra previas.")

                btn_add_morfo_edit = st.form_submit_button("➕ Añadir nueva característica morfológica")
                if btn_add_morfo_edit: st.session_state.extra_morfo_edit += 1
                
                for i in range(st.session_state.extra_morfo_edit):
                    c1, c2 = st.columns(2)
                    with c1: k = st.text_input(f"Nueva Característica {i+1}", key=f"k_m_ed_{i}")
                    with c2: v = st.text_input(f"Valor {i+1}", key=f"v_m_ed_{i}")
                    if k and v: atributos_dinamicos_actualizados[k.strip().lower().replace(" ", "_")] = [v.strip().lower()]

                st.divider()
                st.markdown("##### Tolerancias Ecológicas (Motor Lógico)")
                col_tol1, col_tol2 = st.columns(2)
                with col_tol1:
                    t_turbidez = st.selectbox("Tolerancia a Turbidez:", opc_tol, index=get_index(opc_tol, "tolerancia_turbidez"))
                with col_tol2:
                    t_algas = st.selectbox("Tolerancia a Algas:", opc_tol, index=get_index(opc_tol, "tolerancia_algas"))
                    
                st.divider()
                st.markdown("##### 🌊 Añadir Más Datos Ecológicos")
                btn_add_eco_edit = st.form_submit_button("➕ Añadir variable ecológica al texto")
                if btn_add_eco_edit: st.session_state.extra_eco_edit += 1

                textos_eco_extra_edit = []
                for i in range(st.session_state.extra_eco_edit):
                    c1, c2 = st.columns(2)
                    with c1: k_e = st.text_input(f"Variable Ecológica {i+1}", key=f"k_e_ed_{i}")
                    with c2: v_e = st.text_input(f"Valor {i+1}", key=f"v_e_ed_{i}")
                    if k_e and v_e: textos_eco_extra_edit.append(f"- **{k_e.strip().capitalize()}**: {v_e.strip()}")

                st.divider()
                submit_edicion = st.form_submit_button("🔄 Actualizar Datos", type="primary")
                
                if submit_edicion:
                    if textos_eco_extra_edit:
                        descripcion_final_edit = descripcion_edit + "\n\n**Parámetros Ecológicos Adicionales:**\n" + "\n".join(textos_eco_extra_edit)
                    else:
                        descripcion_final_edit = descripcion_edit

                    datos_actualizados = {
                        "nombre_comun": nombre_comun_edit,
                        "descripcion": descripcion_final_edit,
                        "forma_colonia": [f_colonia],
                        "superficie": [f_superficie],
                        "tamaño_polipos": [f_polipos],
                        "organizacion_coralites": [f_organizacion],
                        "tipo_gemacion": [f_gemacion],
                        "tipo_columnela": [f_columnela],
                        "tolerancia_turbidez": t_turbidez,
                        "tolerancia_algas": t_algas,
                        "abundancia_local": datos_actuales.get("abundancia_local", "comun")
                    }
                    datos_actualizados.update(atributos_dinamicos_actualizados)
                    base_datos[especie_seleccionada] = datos_actualizados
                    
                    if guardar_base_conocimientos(base_datos):
                        st.session_state.extra_morfo_edit = 0
                        st.session_state.extra_eco_edit = 0
                        st.success(f"Datos de '{especie_seleccionada}' actualizados correctamente.")
                        time.sleep(1.5)
                        st.rerun()

    # =================================================================
    # VISTA 5: INFO
    # =================================================================
    elif menu_seleccionado == "Info":
        with st.container(border=True):
            st.title("ℹ️ Información del Sistema Experto")
            st.write("Ficha técnica y créditos de desarrollo.")
            st.divider()

            st.markdown("### 👥 Equipo de Desarrollo")
            st.write("Este sistema experto ha sido diseñado y programado por los bachilleres:")
            st.markdown("""
            * 🧑‍💻 **[Samuel Salazar](https://github.com/Pancho-1234/Portafolio-Personal.git)**
            * 🧑‍💻 **[Cruz Marcano](https://elmacho946.github.io/)**
            * 🧑‍💻 **[Jesús Brito](https://portfolio-jesus-brito.vercel.app/es/)**
            """)
             
            st.divider()
            st.markdown("### 🗃️ Ficha Técnica del Proyecto")
            st.markdown("* **Institución:** Universidad de Oriente (UDO), Núcleo Nueva Esparta.\n* **Área de Aplicación:** Bionomía Bentónica Costera y Taxonomía Marina.\n* **Localización del Modelo:** Litoral Este y Oeste de la Isla de Cubagua, Estado Nueva Esparta, Venezuela.\n* **Metodología:** Integración multicriterio mediante un motor determinista (Lógica Difusa) para la clasificación taxonómica física, acoplado a un motor matemático de inferencia difusa (*scikit-fuzzy*) para el cálculo del índice de incertidumbre y adecuación del hábitat litoral.")