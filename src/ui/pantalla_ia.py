import flet as ft
import json
import os
from .pantallas import COLORS, crear_shell, crear_sidebar, NeoPill, LISTA_ESPECIES_ROQUES

# ─── CONSTANTES ───────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGENES_DIR = os.path.join(BASE_DIR, "data", "Imagenes")

# Mapeo de id de especie → nombre de archivo de imagen
IMAGENES_MAP = {
    "millepora_alcicornis":  "millepora_alcicornis.jpg",
    "millepora_complanata":  "millepora_complanata.jpg",
    "millepora_squarrosa":   "millepora_squarrosa.jpg",
    "stylaster_roseus":      "stylaster_roseus.jpg",
    "acropora_palmata":      "acropora_palmata.jpg",
}

TRADUCCIONES = {
    "p1":  {"s": "Coralitos visibles",    "no": "Sin coralitos"},
    "p4":  {"colonial": "Colonial",       "solitario": "Solitario"},
    "p6":  {"ramificado": "Ramificado",   "no": "No ramificado"},
    "p7":  {"puntas": "Coralitos en puntas", "toda": "Coralitos en toda la rama"},
    "p10": {"cilindricas": "Proj. cilíndricas", "conicas": "Proj. cónicas"},
    "p11": {"aplastadas": "Ramas aplanadas", "cilindricas": "Ramas cilíndricas"},
    "p14": {"mas_10": ">10 escleroseptos", "menos_10": "<10 escleroseptos"},
    "p19": {"laminar": "Laminar",         "masiva": "Masivo"},
    "p20": {"colinas": "Con colinas",     "valles": "Con valles", "copas": "Con copas"},
    "p22": {"s": "Con columela",          "no": "Sin columela"},
    "p30": {"valles": "Valles serpenteantes", "copas": "Copas individuales"},
    "p31": {"pronunciados": "Valles profundos", "suaves": "Valles suaves"},
    "p33": {"dentados": "Septos dentados", "lisos": "Septos lisos"},
    "p35": {"sin": "Sin columela",        "con": "Con columela"},
    "p42": {"anchos": "Valles anchos",    "estrechos": "Valles estrechos"},
    "p48": {"menor_1": "Coralitos <1mm", "entre_1_3": "Coralitos 1-3mm", "mayor_3": "Coralitos >3mm"},
    "p49": {"compacto": "Compacto",       "espaciado": "Espaciado"},
    "p53": {"s": "Tentáculos visibles",   "no": "Sin tentáculos"},
    "p54": {"brillante": "Brillante",     "opaco": "Opaco"},
    "p55": {"separadas": "Copas separadas", "juntas": "Copas fusionadas"},
    "p62": {"lisa": "Superficie lisa",   "desigual": "Superficie irregular"},
    "p63": {"columnar": "Columnar",      "costroso_hemisferico": "Crustoso/hemisférico"},
}

CLAVES_RANKING = ["p1", "p4", "p6", "p7", "p10", "p11", "p19", "p20", "p22", "p30"]

BADGE_SIMILITUD = [
    (85, "Muy similar",        "#388BFD", "#1E388BFD"),
    (70, "Alta similitud",     "#3FB950", "#1E3FB950"),
    (50, "Similitud moderada", "#D29922", "#1ED29922"),
    (0,  "Baja similitud",     "#F85149", "#1EF85149"),
]


def _get_badge(score_pct):
    for threshold, label, color, bg in BADGE_SIMILITUD:
        if score_pct >= threshold:
            return label, color, bg
    return "Baja similitud", "#F85149", "#1EF85149"


def _norm(w: str) -> str:
    w = w.lower().strip()
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u")]:
        w = w.replace(a, b)
    if len(w) > 3 and w.endswith("s"):
        w = w[:-1]
    return w


# ─── PANTALLA IA ──────────────────────────────────────────────────────────────

class PantallaIA:
    """Pantalla IA rediseñada: panel izquierdo de input + panel derecho de resultados en lista."""

    def __init__(self, page: ft.Page, predictor, motor, on_volver):
        self.page = page
        self.predictor = predictor
        self.motor = motor
        self.on_volver = on_volver
        self.campo_texto = None
        self._lista_resultados_ref = None
        self._overlay_ref = None
        self._char_count_ref = None

    # ─────────────────────────────────────────────────────────────────────────
    # MOSTRAR
    # ─────────────────────────────────────────────────────────────────────────
    def mostrar(self):
        modelo_cargado = self.predictor is not None and self.predictor.esta_cargado()

        # ── PANEL IZQUIERDO ──────────────────────────────────────────────────

        # Título de la sección
        titulo_izq = ft.Column([
            ft.Text("Describe tu coral", size=16, weight=ft.FontWeight.BOLD,
                    color=COLORS["cobalt"]),
            ft.Text("Entre más detalles proporciones, mejores serán los resultados.",
                    size=11, color=COLORS["text_secondary"]),
        ], spacing=4)

        # Textarea principal
        self._char_count_ref = ft.Text("0/1000", size=10, color=COLORS["text_muted"])

        def on_change_texto(e):
            val = e.control.value or ""
            self._char_count_ref.value = f"{len(val)}/1000"
            self._char_count_ref.update()

        self.campo_texto = ft.TextField(
            hint_text="Ej: Coral grande redondo con surcos profundos como un cerebro, color gris oscuro, lo vi en zona profunda...",
            multiline=True,
            min_lines=10,
            max_lines=14,
            max_length=1000,
            text_size=13,
            color=COLORS["text_primary"],
            bgcolor=COLORS["surface"],
            border_color=COLORS["card_border"],
            border_radius=12,
            focused_border_color=COLORS["cobalt"],
            cursor_color=COLORS["cobalt"],
            content_padding=ft.padding.Padding(16, 14, 16, 14),
            hint_style=ft.TextStyle(color=COLORS["text_muted"], size=12),
            on_change=on_change_texto,
        )

        campo_wrapper = ft.Stack([
            self.campo_texto,
            ft.Container(
                content=self._char_count_ref,
                alignment=ft.alignment.Alignment(1, 1),
                padding=ft.padding.Padding(0, 0, 12, 12),
            )
        ])

        # Funcionalidad interactiva para insertar palabras clave en el textarea
        def insert_keyword(tag):
            if self.campo_texto:
                curr = self.campo_texto.value or ""
                spacer = "" if not curr or curr.endswith(" ") else " "
                self.campo_texto.value = curr + spacer + f"{tag}: "
                self.campo_texto.focus()
                self.campo_texto.update()

        # Chips de filtro rápido
        chips_filtro = ft.Row([
            _chip_filtro(ft.Icons.COLOR_LENS_ROUNDED,   "Color", lambda _: insert_keyword("Color")),
            _chip_filtro(ft.Icons.SHAPE_LINE_ROUNDED,    "Forma", lambda _: insert_keyword("Forma")),
            _chip_filtro(ft.Icons.STRAIGHTEN_ROUNDED,    "Tamaño", lambda _: insert_keyword("Tamaño")),
            _chip_filtro(ft.Icons.TEXTURE_ROUNDED,       "Textura", lambda _: insert_keyword("Textura")),
            _chip_filtro(ft.Icons.PLACE_ROUNDED,         "Hábitat", lambda _: insert_keyword("Hábitat")),
        ], spacing=8, alignment=ft.MainAxisAlignment.START)

        # Botón principal de búsqueda
        btn_buscar = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color="#FFFFFF", size=18),
                ft.Text("Buscar especies similares", size=13,
                        weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            gradient=ft.LinearGradient(
                begin=ft.alignment.Alignment(-1, 0),
                end=ft.alignment.Alignment(1, 0),
                colors=[COLORS["cobalt"], COLORS["purple"]],
            ),
            border_radius=10,
            padding=ft.padding.Padding(0, 14, 0, 14),
            on_click=self._analizar_texto,
            on_hover=lambda e: _hover_btn(e),
            shadow=ft.BoxShadow(
                blur_radius=20,
                color=COLORS["cobalt_glow"],
                offset=ft.Offset(0, 4),
            ),
        )

        # Consejos
        consejos = ft.Container(
            content=ft.Column([
                ft.Text("Consejos para mejores resultados", size=12,
                        weight=ft.FontWeight.BOLD, color=COLORS["cobalt"]),
                ft.Container(height=8),
                _consejo("Describe el color y patrón del coral"),
                _consejo("Menciona la forma y tamaño general"),
                _consejo("Indica el hábitat o profundidad"),
                _consejo("Si puedes, adjunta una imagen"),
            ], spacing=6),
            bgcolor=COLORS["surface"],
            border_radius=10,
            border=ft.Border.all(1, COLORS["card_border"]),
            padding=ft.padding.Padding(14, 12, 14, 12),
        )

        # Zona de carga de imagen
        zona_imagen = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.UPLOAD_FILE_ROUNDED, color=COLORS["text_muted"], size=28),
                ft.Container(height=4),
                ft.Text("Arrastra una imagen o haz clic para subir",
                        size=11, color=COLORS["text_muted"],
                        text_align=ft.TextAlign.CENTER),
                ft.Text("JPG, PNG hasta 10MB", size=10, color=COLORS["text_muted"],
                        text_align=ft.TextAlign.CENTER),
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            border=ft.Border.all(1.5, COLORS["card_border"]),
            border_radius=10,
            padding=ft.padding.Padding(20, 18, 20, 18),
            bgcolor=COLORS["surface"],
            alignment=ft.alignment.Alignment(0, 0),
        )

        # Status modelo
        status_modelo = ft.Container(
            content=ft.Row([
                ft.Container(
                    width=6, height=6,
                    bgcolor=COLORS["success"] if modelo_cargado else COLORS["warning"],
                    border_radius=3,
                ),
                ft.Text(
                    "Modelo activo" if modelo_cargado else "Modelo no disponible",
                    size=10, color=COLORS["text_muted"],
                ),
            ], spacing=6),
        )

        panel_izq = ft.Container(
            content=ft.Column([
                titulo_izq,
                ft.Container(height=14),
                campo_wrapper,
                ft.Container(height=10),
                chips_filtro,
                ft.Container(height=14),
                btn_buscar,
                ft.Container(height=16),
                consejos,
                ft.Container(height=12),
                zona_imagen,
                ft.Container(height=10),
                status_modelo,
            ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE),
            expand=2,
            padding=ft.padding.Padding(24, 24, 20, 24),
            bgcolor=COLORS["card"],
            border=ft.Border(right=ft.BorderSide(1, COLORS["card_border"])),
        )

        # ── PANEL DERECHO ─────────────────────────────────────────────────────

        # Lista de resultados (inicialmente vacía → muestra catálogo)
        self._lista_resultados_ref = ft.Column(
            [self._construir_estado_inicial()],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

        # Header del panel derecho
        self._header_der_ref = ft.Row([
            ft.Text("Resultados de IA", size=16, weight=ft.FontWeight.BOLD,
                    color=COLORS["text_primary"]),
            ft.Container(
                content=ft.Text("Top 5 especies más similares", size=10,
                                color=COLORS["cobalt"], weight=ft.FontWeight.BOLD),
                bgcolor=COLORS["cobalt_dim"],
                border_radius=20,
                padding=ft.padding.Padding(10, 4, 10, 4),
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Nota informativa inferior
        nota_inferior = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, color=COLORS["text_muted"], size=13),
                ft.Text(
                    "Los resultados se basan en algoritmos de IA entrenados con datos científicos verificados.",
                    size=10, color=COLORS["text_muted"], expand=True,
                ),
            ], spacing=6),
            padding=ft.padding.Padding(0, 10, 0, 0),
            border=ft.Border(top=ft.BorderSide(1, COLORS["card_border"])),
        )

        panel_der = ft.Container(
            content=ft.Column([
                self._header_der_ref,
                ft.Container(height=14),
                ft.Container(content=self._lista_resultados_ref, expand=True),
                nota_inferior,
            ], spacing=0, expand=True),
            expand=4,
            padding=ft.padding.Padding(24, 24, 24, 16),
        )

        main_content = ft.Row([
            panel_izq,
            panel_der,
        ], spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)

        sidebar = crear_sidebar(
            self.page,
            active_screen="ia",
            on_inicio=self.on_volver,
            on_consulta=self.on_volver,
        )

        crear_shell(self.page, sidebar, main_content)

    # ─────────────────────────────────────────────────────────────────────────
    # ESTADO INICIAL (sin resultados)
    # ─────────────────────────────────────────────────────────────────────────
    def _construir_estado_inicial(self):
        """Estado vacío: muestra catálogo agrupado de todas las especies."""
        grupos_iconos = {
            "hidrocoral": ("🔥", "#EF4444"),
            "ramificado": ("🌿", COLORS["accent"]),
            "laminar":    ("🍃", "#10B981"),
            "masivo":     ("🪨", COLORS["text_secondary"]),
            "solitario":  ("🔵", COLORS["cobalt"]),
        }

        grupos: dict = {}
        for c in LISTA_ESPECIES_ROQUES:
            g = c.get("grupo", "otro")
            grupos.setdefault(g, []).append(c)

        items = []
        for grupo, especies in grupos.items():
            icon, color = grupos_iconos.get(grupo, ("🪸", COLORS["accent"]))
            items.append(ft.Container(
                content=ft.Row([
                    ft.Text(icon, size=13),
                    ft.Text(grupo.upper(), size=10, weight=ft.FontWeight.BOLD, color=color),
                    ft.Container(
                        content=ft.Text(str(len(especies)), size=9, color=color,
                                        weight=ft.FontWeight.BOLD),
                        padding=ft.padding.Padding(6, 2, 6, 2),
                        bgcolor=color + "20",
                        border_radius=8,
                    ),
                ], spacing=6),
                padding=ft.padding.Padding(0, 10, 0, 4),
            ))
            for c in especies:
                items.append(ft.Container(
                    content=ft.Row([
                        ft.Container(width=12),
                        ft.Column([
                            ft.Text(c["nombre"], size=11, weight=ft.FontWeight.W_600,
                                    color=COLORS["text_primary"]),
                            ft.Text(c["familia"], size=9, color=COLORS["text_muted"]),
                        ], spacing=0, expand=True),
                    ], spacing=0),
                    padding=ft.padding.Padding(0, 6, 0, 6),
                    border=ft.Border(bottom=ft.BorderSide(1, COLORS["card_border"])),
                ))

        return ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.BIOTECH_ROUNDED, color=COLORS["accent"], size=16),
                ft.Text("Catálogo de Especies", size=13, weight=ft.FontWeight.BOLD,
                        color=COLORS["text_primary"]),
                ft.Container(
                    content=ft.Text("41 especies", size=10, color=COLORS["text_secondary"]),
                    padding=ft.padding.Padding(8, 3, 8, 3),
                    bgcolor=COLORS["surface"],
                    border_radius=8,
                ),
            ], spacing=8),
            ft.Text("Describe tu coral para obtener resultados específicos.",
                    size=11, color=COLORS["text_secondary"]),
            ft.Container(height=12),
            ft.Column(items, spacing=0),
        ], spacing=4)

    # ─────────────────────────────────────────────────────────────────────────
    # ANÁLISIS
    # ─────────────────────────────────────────────────────────────────────────
    def _analizar_texto(self, e):
        import time
        texto = self.campo_texto.value.strip() if self.campo_texto else ""
        if not texto:
            self._mostrar_error("Por favor, ingresa una descripción del coral.")
            return
        if not self.predictor or not self.predictor.esta_cargado():
            self._mostrar_error("Modelo no cargado. Ejecuta el entrenamiento primero.")
            return

        # Predecir primero en el backend (guardamos los resultados en memoria)
        resultado_modelo = self.predictor.predecir_con_ponderacion(texto)
        if not resultado_modelo.get("success"):
            self._mostrar_error(resultado_modelo.get("error", "Error en la predicción"))
            return

        respuestas_predichas = resultado_modelo.get("respuestas_red", {})
        respuestas_filtradas = {k: v for k, v in respuestas_predichas.items()
                                if v != "desconocido"}
        self.motor.ejecutar(respuestas_filtradas)
        ranking = resultado_modelo.get("ranking", [])

        # Mostrar animación de carga por pasos (Miga de pan / Stepper)
        pasos = [
            ("🔍", "Leyendo descripción y normalizando texto..."),
            ("🧠", "Procesando rasgos morfológicos con red neuronal Keras..."),
            ("🪸", "Ejecutando inferencia semántica híbrida..."),
            ("📊", "Calculando ranking de similitud taxonómica..."),
        ]

        controles_carga = []
        for icon, desc in pasos:
            controles_carga.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, color=COLORS["text_muted"], size=16),
                            width=24, height=24,
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                        ft.Text(desc, size=12, color=COLORS["text_secondary"]),
                    ], spacing=12),
                    padding=ft.padding.Padding(16, 10, 16, 10),
                    bgcolor=COLORS["surface"],
                    border_radius=8,
                    border=ft.Border.all(1, COLORS["card_border"]),
                    opacity=0.5,
                )
            )

        loading_container = ft.Column(
            [
                ft.Container(height=16),
                ft.Text("PROCESANDO ANÁLISIS DE INTELIGENCIA ARTIFICIAL", size=10, color=COLORS["cobalt"], weight=ft.FontWeight.BOLD),
                ft.Container(height=14),
                ft.Column(controles_carga, spacing=8),
                ft.Container(height=24),
                ft.Row([
                    ft.ProgressRing(width=16, height=16, stroke_width=2, color=COLORS["cobalt"]),
                    ft.Text("Interpretando respuestas del usuario...", size=11, color=COLORS["text_muted"]),
                ], spacing=8),
            ],
            spacing=0,
        )

        self._lista_resultados_ref.controls = [loading_container]
        self._lista_resultados_ref.update()

        # Ejecutar simulación de carga de 2 segundos (0.5s por paso)
        for i in range(len(pasos)):
            # Activar paso
            controles_carga[i].opacity = 1.0
            controles_carga[i].bgcolor = COLORS["surface"]
            controles_carga[i].border = ft.Border.all(1, COLORS["cobalt"] + "70")
            controles_carga[i].content.controls[0].content = ft.ProgressRing(
                width=12, height=12, stroke_width=2, color=COLORS["cobalt"]
            )
            self._lista_resultados_ref.update()

            time.sleep(0.5)

            # Completar paso
            controles_carga[i].border = ft.Border.all(1, COLORS["success"] + "40")
            controles_carga[i].content.controls[0].content = ft.Icon(
                ft.Icons.CHECK_CIRCLE_ROUNDED, color=COLORS["success"], size=16
            )
            self._lista_resultados_ref.update()

        # Mostrar resultados reales al completar
        self._actualizar_panel_resultados(ranking)

    # ─────────────────────────────────────────────────────────────────────────
    # RESULTADOS
    # ─────────────────────────────────────────────────────────────────────────
    def _actualizar_panel_resultados(self, ranking: list):
        top5 = ranking[:5]
        cards = []
        for idx, item in enumerate(top5):
            esp = item["especie"]
            score = item["score"]
            tax_score = item["tax_score"]
            text_score = item["text_score"]
            coincidencias = item["coincidencias"]
            
            card = self._construir_fila_resultado(
                idx + 1, esp, score, tax_score, text_score, coincidencias
            )
            cards.append(card)

        self._lista_resultados_ref.controls = cards
        self._lista_resultados_ref.update()

    def _construir_fila_resultado(self, pos, esp, score, tax_score, text_score, coincidencias):
        """Fila de resultado al estilo de la imagen: foto + info + % circular. Si pos == 1, destaca."""
        pct = int(score * 100)
        badge_label, badge_color, badge_bg = _get_badge(pct)
        is_top1 = (pos == 1)

        # ── Imagen de la especie (Búsqueda dinámica por ID y extensiones) ──
        tiene_imagen = False
        img_path = ""
        for ext in [".jpg", ".jpeg", ".png", ".JPG", ".PNG", ".JPEG"]:
            p = os.path.join(IMAGENES_DIR, f"{esp.get('id')}{ext}")
            if os.path.isfile(p):
                img_path = p
                tiene_imagen = True
                break

        img_size = 100 if is_top1 else 80

        if tiene_imagen:
            imagen_widget = ft.Image(
                src=img_path,
                width=img_size,
                height=img_size,
                fit="cover",
                border_radius=ft.BorderRadius(8, 8, 8, 8),
            )
        else:
            # Placeholder si no hay imagen
            grupo = next(
                (c["grupo"] for c in LISTA_ESPECIES_ROQUES
                 if c["nombre"] == esp.get("nombre_cientifico", "")),
                "otro"
            )
            emoji = {"hidrocoral": "🔥", "ramificado": "🌿",
                     "laminar": "🍃", "masivo": "🪨", "solitario": "🔵"}.get(grupo, "🪸")
            imagen_widget = ft.Container(
                content=ft.Text(emoji, size=38 if is_top1 else 30),
                width=img_size, height=img_size,
                bgcolor=COLORS["surface"],
                border_radius=8,
                alignment=ft.alignment.Alignment(0, 0),
                border=ft.Border.all(1, COLORS["card_border"]),
            )

        # ── Chips de características clave ──
        tags_chips = []
        if esp.get("caracteristicas"):
            car = esp["caracteristicas"]
            forma = str(car.get("forma", "")).replace("_", " ").capitalize()
            if forma:
                tags_chips.append(_tag_chip(forma))
            for k, v in coincidencias.items():
                if v.get("match"):
                    label = TRADUCCIONES.get(k, {}).get(v["predicho"], v["predicho"])
                    tags_chips.append(_tag_chip(label))
                if len(tags_chips) >= 4:
                    break

        tags_row = ft.Row(tags_chips[:4], spacing=4, wrap=False) if tags_chips else ft.Container()

        # ── Botón estrella / favorito ──
        btn_star = ft.Container(
            content=ft.Icon(ft.Icons.STAR_BORDER_ROUNDED,
                            color=COLORS["text_muted"], size=20 if is_top1 else 18),
            on_click=lambda _, e=esp, s=score, tx=tax_score, ts=text_score, co=coincidencias:
                self._abrir_modal(e, s, tx, ts, co),
            padding=4,
        )

        # ── Círculo de similitud ──
        color_pct = (
            COLORS["cobalt"] if pct >= 85 else
            COLORS["success"] if pct >= 70 else
            COLORS["warning"] if pct >= 50 else
            COLORS["error"]
        )
        circulo_size = 60 if is_top1 else 52
        circulo = ft.Stack([
            ft.ProgressRing(
                value=score,
                color=color_pct,
                bgcolor=COLORS["surface"],
                stroke_width=4.5 if is_top1 else 4,
                width=circulo_size,
                height=circulo_size,
            ),
            ft.Column([
                ft.Text(f"{pct}%", size=13 if is_top1 else 11, weight=ft.FontWeight.BOLD,
                        color=color_pct),
                ft.Text("Similitud", size=8 if is_top1 else 7, color=COLORS["text_muted"]),
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.alignment.Alignment(0, 0), width=circulo_size, height=circulo_size)

        # ── Fila completa ──
        def hover_fila(e):
            if is_top1:
                # Top 1 conservará su color base resaltado o cambiará sutilmente
                e.control.bgcolor = "#2200F5D4" if e.data == "true" else "#0A00F5D4"
            else:
                e.control.bgcolor = COLORS["surface"] if e.data == "true" else "transparent"
            e.control.update()

        fila = ft.Container(
            content=ft.Row([
                # Imagen
                imagen_widget,
                ft.Container(width=16 if is_top1 else 12),
                # Info central
                ft.Column([
                    ft.Row([
                        ft.Text(esp.get("nombre_cientifico", ""), size=16 if is_top1 else 13,
                                weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                        ft.Container(width=8),
                        ft.Container(
                            content=ft.Text(badge_label, size=10 if is_top1 else 9,
                                            color=badge_color, weight=ft.FontWeight.BOLD),
                            bgcolor=badge_bg,
                            border_radius=20,
                            padding=ft.padding.Padding(10, 4, 10, 4) if is_top1 else ft.padding.Padding(8, 3, 8, 3),
                        ),
                    ], spacing=0),
                    ft.Container(height=2),
                    ft.Text(f"Familia: {esp.get('familia', 'N/A')}",
                            size=11 if is_top1 else 10, color=COLORS["text_secondary"]),
                    ft.Container(height=6 if is_top1 else 4),
                    ft.Text(
                        esp.get("descripcion", "")[:150] + "…"
                        if is_top1 and len(esp.get("descripcion", "")) > 150
                        else esp.get("descripcion", "")[:120] + "…"
                        if len(esp.get("descripcion", "")) > 120
                        else esp.get("descripcion", ""),
                        size=12 if is_top1 else 11, color=COLORS["text_secondary"],
                        overflow=ft.TextOverflow.ELLIPSIS,
                        max_lines=2,
                    ),
                    ft.Container(height=10 if is_top1 else 8),
                    tags_row,
                ], spacing=0, expand=True),
                ft.Container(width=16 if is_top1 else 12),
                # Derecha: círculo + estrella
                ft.Column([
                    circulo,
                    ft.Container(height=8 if is_top1 else 6),
                    btn_star,
                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.Padding(18, 16, 18, 16) if is_top1 else ft.padding.Padding(14, 12, 14, 12),
            bgcolor="#0A00F5D4" if is_top1 else "transparent",
            border_radius=12 if is_top1 else 0,
            border=ft.Border.all(1.5, COLORS["accent"] + "40") if is_top1 else ft.Border(bottom=ft.BorderSide(1, COLORS["card_border"])),
            margin=ft.margin.Margin(0, 0, 0, 12) if is_top1 else ft.margin.Margin(0, 0, 0, 0),
            on_hover=hover_fila,
            on_click=lambda _, e=esp, s=score, tx=tax_score, ts=text_score, co=coincidencias:
                self._abrir_modal(e, s, tx, ts, co),
        )
        return fila

    # ─────────────────────────────────────────────────────────────────────────
    # MODAL DE DETALLE
    # ─────────────────────────────────────────────────────────────────────────
    def _abrir_modal(self, esp, score, tax_score, text_score, coincidencias):
        pct = int(score * 100)
        badge_label, badge_color, badge_bg = _get_badge(pct)

        color_pct = (
            COLORS["cobalt"] if pct >= 85 else
            COLORS["success"] if pct >= 70 else
            COLORS["warning"] if pct >= 50 else
            COLORS["error"]
        )

        # Imagen del modal (Búsqueda dinámica por ID y extensiones)
        tiene_imagen = False
        img_path = ""
        for ext in [".jpg", ".jpeg", ".png", ".JPG", ".PNG", ".JPEG"]:
            p = os.path.join(IMAGENES_DIR, f"{esp.get('id')}{ext}")
            if os.path.isfile(p):
                img_path = p
                tiene_imagen = True
                break

        if tiene_imagen:
            img_modal = ft.Image(
                src=img_path,
                width=120, height=120,
                fit="cover",
                border_radius=ft.BorderRadius(12, 12, 12, 12),
            )
        else:
            img_modal = ft.Container(
                content=ft.Text("🪸", size=50),
                width=120, height=120,
                bgcolor=COLORS["surface"],
                border_radius=12,
                alignment=ft.alignment.Alignment(0, 0),
            )

        # Filas de tabla de coincidencias
        filas_tabla = []
        for k, det in coincidencias.items():
            pred_label = TRADUCCIONES.get(k, {}).get(det["predicho"], det["predicho"])
            esp_label  = TRADUCCIONES.get(k, {}).get(det["especie"], det["especie"] or "—")
            match = det["match"]
            filas_tabla.append(ft.Container(
                content=ft.Row([
                    ft.Text("✅" if match else "❌", size=13),
                    ft.Column([
                        ft.Text(pred_label, size=11, color=COLORS["text_primary"]),
                        ft.Text(f"Especie: {esp_label}", size=9, color=COLORS["text_secondary"]),
                    ], spacing=1, expand=True),
                    ft.Container(
                        content=ft.Text(
                            "Coincide" if match else "No coincide",
                            size=9, weight=ft.FontWeight.BOLD,
                            color=COLORS["success"] if match else COLORS["error"],
                        ),
                        padding=ft.padding.Padding(6, 3, 6, 3),
                        bgcolor="#1510B981" if match else "#15EF4444",
                        border_radius=6,
                    ),
                ], spacing=8),
                padding=ft.padding.Padding(10, 8, 10, 8),
                bgcolor=COLORS["surface"],
                border_radius=8,
                border=ft.Border.all(1, COLORS["card_border"]),
                margin=ft.margin.Margin(0, 0, 0, 4),
            ))

        if not filas_tabla:
            filas_tabla.append(ft.Text(
                "No se encontraron características taxonómicas comparables.",
                size=11, color=COLORS["text_secondary"],
            ))

        modal_content = ft.Container(
            content=ft.Column([
                # Header del modal
                ft.Row([
                    ft.Row([
                        img_modal,
                        ft.Container(width=16),
                        ft.Column([
                            ft.Text(esp.get("nombre_cientifico", ""), size=18,
                                    weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                            ft.Text(esp.get("nombre_comun", ""), size=12,
                                    color=COLORS["text_secondary"]),
                            ft.Container(height=8),
                            ft.Row([
                                ft.Container(
                                    content=ft.Text(badge_label, size=10,
                                                    color=badge_color, weight=ft.FontWeight.BOLD),
                                    bgcolor=badge_bg,
                                    border_radius=20,
                                    padding=ft.padding.Padding(10, 4, 10, 4),
                                ),
                                ft.Container(
                                    content=ft.Text(f"{pct}% CONFIANZA", size=10,
                                                    color=color_pct, weight=ft.FontWeight.BOLD),
                                    bgcolor=color_pct + "20",
                                    border_radius=20,
                                    padding=ft.padding.Padding(10, 4, 10, 4),
                                ),
                            ], spacing=6),
                            ft.Container(height=6),
                            ft.Text(f"Familia: {esp.get('familia', 'N/A')}  ·  "
                                    f"Orden: {esp.get('orden', 'N/A')}",
                                    size=10, color=COLORS["text_muted"]),
                        ], spacing=0, expand=True),
                    ], expand=True),
                    ft.Container(
                        content=ft.Icon(ft.Icons.CLOSE_ROUNDED,
                                        color=COLORS["text_secondary"], size=18),
                        padding=8,
                        bgcolor=COLORS["surface"],
                        border_radius=20,
                        on_click=lambda _: self._cerrar_modal(),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                   vertical_alignment=ft.CrossAxisAlignment.START),

                ft.Divider(color=COLORS["card_border"], height=20),

                # Desglose puntuación
                ft.Row([
                    _score_box("Taxonómica", int(tax_score * 100),
                               COLORS["accent"], "%"),
                    _score_box("Textual", int(text_score * 100),
                               COLORS["cobalt"], "%"),
                    _score_box("Total", pct, color_pct, "%"),
                ], spacing=10),

                ft.Divider(color=COLORS["card_border"], height=20),

                # Tabla rasgos
                ft.Text("ANÁLISIS DE RASGOS MORFOLÓGICOS", size=10,
                        color=COLORS["text_secondary"], weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                ft.Column(filas_tabla, spacing=0,
                          scroll=ft.ScrollMode.ADAPTIVE, height=150),

                ft.Divider(color=COLORS["card_border"], height=20),

                # Descripción
                ft.Text("DESCRIPCIÓN", size=10, color=COLORS["text_secondary"],
                        weight=ft.FontWeight.BOLD),
                ft.Container(height=6),
                ft.Container(
                    content=ft.Text(esp.get("descripcion", "Sin descripción."),
                                    size=12, color=COLORS["text_primary"]),
                    padding=12,
                    bgcolor=COLORS["surface"],
                    border_radius=10,
                    border=ft.Border.all(1, COLORS["card_border"]),
                ),
                ft.Container(height=8),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PLACE_ROUNDED, color=COLORS["cobalt"], size=13),
                        ft.Text(esp.get("habitat", "Hábitat no especificado."),
                                size=11, color=COLORS["text_secondary"], expand=True),
                    ], spacing=6),
                    padding=ft.padding.Padding(12, 8, 12, 8),
                    bgcolor=COLORS["surface"],
                    border_radius=10,
                    border=ft.Border.all(1, COLORS["card_border"]),
                ),
            ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE),
            padding=28,
            bgcolor=COLORS["card"],
            border_radius=16,
            border=ft.Border.all(1, COLORS["card_border"]),
            shadow=ft.BoxShadow(blur_radius=40, color="#80000000", offset=ft.Offset(0, 8)),
            width=680,
        )

        overlay = ft.Container(
            content=ft.Stack([
                ft.Container(
                    bgcolor="#CC0D1117",
                    expand=True,
                    on_click=lambda _: self._cerrar_modal(),
                ),
                ft.Container(
                    content=modal_content,
                    alignment=ft.alignment.Alignment(0, 0),
                    expand=True,
                    padding=40,
                ),
            ]),
            expand=True,
        )

        self._overlay_ref = overlay
        self.page.overlay.append(overlay)
        self.page.update()

    def _cerrar_modal(self):
        if self._overlay_ref and self._overlay_ref in self.page.overlay:
            self.page.overlay.remove(self._overlay_ref)
            self._overlay_ref = None
            self.page.update()

    # ─────────────────────────────────────────────────────────────────────────
    # ERROR
    # ─────────────────────────────────────────────────────────────────────────
    def _mostrar_error(self, mensaje: str):
        snack = ft.SnackBar(
            ft.Text(mensaje, color="#FFFFFF", weight=ft.FontWeight.BOLD),
            bgcolor=COLORS["error"],
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def _chip_filtro(icon, label, on_click=None):
    def on_hover(e):
        e.control.bgcolor = COLORS["card_border"] if e.data == "true" else COLORS["surface"]
        e.control.update()

    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, color=COLORS["text_secondary"], size=13),
            ft.Text(label, size=11, color=COLORS["text_secondary"]),
        ], spacing=4),
        bgcolor=COLORS["surface"],
        border_radius=20,
        border=ft.Border.all(1, COLORS["card_border"]),
        padding=ft.padding.Padding(10, 5, 10, 5),
        on_click=on_click,
        on_hover=on_hover,
    )


def _consejo(texto):
    return ft.Row([
        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                color=COLORS["cobalt"], size=14),
        ft.Text(texto, size=11, color=COLORS["text_secondary"], expand=True),
    ], spacing=8)


def _tag_chip(label):
    return ft.Container(
        content=ft.Text(label, size=9, color=COLORS["text_secondary"]),
        bgcolor=COLORS["surface"],
        border_radius=20,
        border=ft.Border.all(1, COLORS["card_border"]),
        padding=ft.padding.Padding(8, 3, 8, 3),
    )


def _score_box(label, value, color, unit=""):
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=10, color=COLORS["text_secondary"]),
            ft.Text(f"{value}{unit}", size=22, weight=ft.FontWeight.BOLD, color=color),
        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        padding=12,
        bgcolor=color + "15",
        border_radius=10,
        border=ft.Border.all(1, color + "30"),
    )


def _hover_btn(e):
    e.control.opacity = 0.85 if e.data == "true" else 1.0
    e.control.update()