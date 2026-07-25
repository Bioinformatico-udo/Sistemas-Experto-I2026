import flet as ft
import json

# â”€â”€â”€ PALETA DE COLORES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
COLORS = {
    "bg":            "#0D1117",
    "sidebar":       "#161B22",
    "sidebar_hover": "#1E2631",
    "sidebar_active":"#1E3A5F",
    "card":          "#161B22",
    "card_border":   "#21262D",
    "surface":       "#1C2333",
    "surface2":      "#0D1117",
    "text_primary":  "#E6EDF3",
    "text_secondary":"#8B949E",
    "text_muted":    "#484F58",
    "accent":        "#00F5D4",
    "accent_dim":    "#1A00F5D4",
    "cobalt":        "#388BFD",
    "cobalt_dim":    "#1E388BFD",
    "cobalt_glow":   "#40388BFD",
    "success":       "#3FB950",
    "warning":       "#D29922",
    "error":         "#F85149",
    "purple":        "#8957E5",
}

# â”€â”€â”€ LISTA ESTÃTICA DE ESPECIES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
LISTA_ESPECIES_ROQUES = [
    {"nombre": "Millepora alcicornis",      "familia": "Milleporidae",    "grupo": "hidrocoral"},
    {"nombre": "Millepora complanata",       "familia": "Milleporidae",    "grupo": "hidrocoral"},
    {"nombre": "Millepora squarrosa",        "familia": "Milleporidae",    "grupo": "hidrocoral"},
    {"nombre": "Acropora palmata",           "familia": "Acroporidae",     "grupo": "ramificado"},
    {"nombre": "Acropora cervicornis",       "familia": "Acroporidae",     "grupo": "ramificado"},
    {"nombre": "Acropora prolifera",         "familia": "Acroporidae",     "grupo": "ramificado"},
    {"nombre": "Madracis decactis",          "familia": "Pocilloporidae",  "grupo": "ramificado"},
    {"nombre": "Eusmilia fastigiata",        "familia": "Meandrinidae",    "grupo": "ramificado"},
    {"nombre": "Mussa angulosa",             "familia": "Mussidae",        "grupo": "ramificado"},
    {"nombre": "Porites divaricata",         "familia": "Poritidae",       "grupo": "ramificado"},
    {"nombre": "Porites furcata",            "familia": "Poritidae",       "grupo": "ramificado"},
    {"nombre": "Porites porites",            "familia": "Poritidae",       "grupo": "ramificado"},
    {"nombre": "Scolymia lacera",            "familia": "Mussidae",        "grupo": "solitario"},
    {"nombre": "Scolymia cubensis",          "familia": "Mussidae",        "grupo": "solitario"},
    {"nombre": "Undaria agaricites",         "familia": "Agariciidae",     "grupo": "laminar"},
    {"nombre": "Agaricia fragilis",          "familia": "Agariciidae",     "grupo": "laminar"},
    {"nombre": "Agaricia lamarcki",          "familia": "Agariciidae",     "grupo": "laminar"},
    {"nombre": "Agaricia tenuifolia",        "familia": "Agariciidae",     "grupo": "laminar"},
    {"nombre": "Agaricia undata",            "familia": "Agariciidae",     "grupo": "laminar"},
    {"nombre": "Leptoseris cucullata",       "familia": "Agariciidae",     "grupo": "laminar"},
    {"nombre": "Porites astreoides",         "familia": "Poritidae",       "grupo": "masivo"},
    {"nombre": "Siderastrea radians",        "familia": "Siderastreidae",  "grupo": "masivo"},
    {"nombre": "Siderastrea siderea",        "familia": "Siderastreidae",  "grupo": "masivo"},
    {"nombre": "Dendrogyra cylindrus",       "familia": "Meandrinidae",    "grupo": "masivo"},
    {"nombre": "Meandrina meandrites",       "familia": "Meandrinidae",    "grupo": "masivo"},
    {"nombre": "Isophyllia sinuosa",         "familia": "Mussidae",        "grupo": "masivo"},
    {"nombre": "Isophyllastrea rigida",      "familia": "Mussidae",        "grupo": "masivo"},
    {"nombre": "Mycetophyllia aliciae",      "familia": "Mussidae",        "grupo": "masivo"},
    {"nombre": "Mycetophyllia ferox",        "familia": "Mussidae",        "grupo": "masivo"},
    {"nombre": "Mycetophyllia lamarckiana",  "familia": "Mussidae",        "grupo": "masivo"},
    {"nombre": "Orbicella annularis",        "familia": "Merulinidae",     "grupo": "masivo"},
    {"nombre": "Orbicella faveolata",        "familia": "Merulinidae",     "grupo": "masivo"},
    {"nombre": "Orbicella franksi",          "familia": "Merulinidae",     "grupo": "masivo"},
    {"nombre": "Montastraea cavernosa",      "familia": "Montastraeidae",  "grupo": "masivo"},
    {"nombre": "Diploria labyrinthiformis",  "familia": "Faviidae",        "grupo": "masivo"},
    {"nombre": "Pseudodiploria strigosa",    "familia": "Faviidae",        "grupo": "masivo"},
    {"nombre": "Colpophyllia natans",        "familia": "Merulinidae",     "grupo": "masivo"},
    {"nombre": "Favia fragum",               "familia": "Faviidae",        "grupo": "masivo"},
    {"nombre": "Manicina areolata",          "familia": "Faviidae",        "grupo": "masivo"},
    {"nombre": "Stephanocoenia intersepta",  "familia": "Astrocoeniidae",  "grupo": "masivo"},
]


def filtrar_candidatos(respuestas):
    """Deduce candidatos en base a respuestas parciales clave."""
    candidatos = LISTA_ESPECIES_ROQUES
    if respuestas.get("p1") == "no":
        return [c for c in candidatos if c["grupo"] == "hidrocoral"]
    elif respuestas.get("p1") == "s":
        res = [c for c in candidatos if c["grupo"] != "hidrocoral"]
        if respuestas.get("p4") == "solitario":
            return [c for c in res if c["grupo"] == "solitario"]
        elif respuestas.get("p4") == "colonial":
            res = [c for c in res if c["grupo"] != "solitario"]
            if respuestas.get("p6") == "ramificado":
                return [c for c in res if c["grupo"] == "ramificado"]
            elif respuestas.get("p6") == "no":
                res = [c for c in res if c["grupo"] != "ramificado"]
                if respuestas.get("p19") == "laminar":
                    return [c for c in res if c["grupo"] == "laminar"]
                elif respuestas.get("p19") == "masiva":
                    return [c for c in res if c["grupo"] == "masivo"]
        return res
    return candidatos


# â”€â”€â”€ COMPONENTES AUXILIARES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def NeoPill(text, is_active=True, on_click=None):
    """BotÃ³n ovalado (Pill) estilo Neo-Tactile."""
    return ft.Container(
        content=ft.Text(
            text, size=12, weight=ft.FontWeight.BOLD,
            color="#FFFFFF" if is_active else COLORS["text_secondary"],
            text_align=ft.TextAlign.CENTER
        ),
        bgcolor=COLORS["cobalt"] if is_active else "#1A1A2E",
        border_radius=18,
        border=ft.Border.all(1, COLORS["cobalt"] if is_active else COLORS["card_border"]),
        padding=ft.padding.Padding(20, 8, 20, 8),
        alignment=ft.alignment.Alignment(0, 0),
        on_click=on_click,
        shadow=ft.BoxShadow(
            blur_radius=15,
            color=COLORS["cobalt_glow"] if is_active else "transparent",
            offset=ft.Offset(0, 4)
        ) if is_active else None
    )


def ProgressStepper(current, total=5):
    """RepresentaciÃ³n visual del progreso del cuestionario."""
    nodes = []
    for i in range(1, total + 1):
        is_active = i <= current
        is_current = i == current
        node = ft.Container(
            content=ft.Text(
                str(i), size=10, weight=ft.FontWeight.BOLD,
                color=COLORS["bg"] if is_active else COLORS["text_secondary"]
            ),
            width=22, height=22,
            bgcolor=COLORS["accent"] if is_active else "#20FFFFFF",
            border_radius=11,
            alignment=ft.alignment.Alignment(0, 0),
            border=ft.Border.all(1.5, COLORS["accent"] if (is_active or is_current) else COLORS["card_border"]),
            shadow=ft.BoxShadow(blur_radius=8, color=COLORS["accent_dim"], spread_radius=1) if is_current else None
        )
        nodes.append(node)
        if i < total:
            nodes.append(ft.Container(
                width=28, height=2,
                bgcolor=COLORS["accent"] if i < current else "#15FFFFFF"
            ))
    return ft.Row(nodes, alignment=ft.MainAxisAlignment.CENTER, spacing=0)


def _sidebar_item(icon, label, active, on_click=None):
    """Un Ã­tem de navegaciÃ³n del sidebar."""
    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, color=COLORS["accent"] if active else COLORS["text_secondary"], size=18),
            ft.Text(
                label, size=12,
                color=COLORS["text_primary"] if active else COLORS["text_secondary"],
                weight=ft.FontWeight.W_600 if active else ft.FontWeight.NORMAL
            ),
        ], spacing=10),
        bgcolor=COLORS["sidebar_active"] if active else "transparent",
        border_radius=8,
        padding=ft.padding.Padding(12, 10, 12, 10),
        on_click=on_click,
        on_hover=lambda e: _on_hover_sidebar(e, active),
        border=ft.Border.all(1, COLORS["cobalt"] if active else "transparent"),
    )


def _on_hover_sidebar(e, active):
    if not active:
        e.control.bgcolor = COLORS["sidebar_hover"] if e.data == "true" else "transparent"
        e.control.update()


def crear_sidebar(page, active_screen, on_inicio=None, on_consulta=None, on_ia=None, on_guia=None):
    """Sidebar de navegación lateral con logo y menú."""

    # Si es None, usamos el global asignado a page. Si el global no existe, usamos una función vacía.
    on_inicio = on_inicio if on_inicio is not None else getattr(page, "on_nav_inicio", lambda: None)
    on_consulta = on_consulta if on_consulta is not None else getattr(page, "on_nav_consulta", lambda: None)
    on_ia = on_ia if on_ia is not None else getattr(page, "on_nav_ia", lambda: None)
    on_guia = on_guia if on_guia is not None else getattr(page, "on_nav_guia", lambda: None)

    nav_items = ft.Column([
        _sidebar_item(ft.Icons.HOME_ROUNDED,        "Inicio",          active_screen == "inicio",   on_click=lambda _: on_inicio()),
        _sidebar_item(ft.Icons.ASSIGNMENT_ROUNDED,  "Consulta",        active_screen == "consulta", on_click=lambda _: on_consulta()),
        _sidebar_item(ft.Icons.AUTO_AWESOME_ROUNDED,"IA Assistant",    active_screen == "ia",       on_click=lambda _: on_ia()),
        _sidebar_item(ft.Icons.MENU_BOOK_ROUNDED,   "Guía de Corales", active_screen == "guia",     on_click=lambda _: on_guia()),
    ], spacing=4)

    footer_items = ft.Column([
        ft.Divider(color=COLORS["card_border"], height=1),
        ft.Container(height=8),
        ft.Row([
            ft.Icon(ft.Icons.LOCATION_ON_ROUNDED, color=COLORS["text_muted"], size=13),
            ft.Text("Los Roques, VE", size=10, color=COLORS["text_muted"]),
        ], spacing=6),
        ft.Container(height=4),
        ft.Row([
            ft.Icon(ft.Icons.SETTINGS_ROUNDED, color=COLORS["text_muted"], size=14),
            ft.Text("Sistema v2.0", size=10, color=COLORS["text_muted"]),
        ], spacing=6),
    ], spacing=0)

    return ft.Container(
        content=ft.Column([
            # Logo / Branding
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("ðŸª¸", size=18),
                            width=36, height=36,
                            bgcolor="#1A2A4A",
                            border_radius=10,
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                    ]),
                    ft.Container(height=6),
                    ft.Text("Expert", size=13, weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                    ft.Text("Coral v2", size=11, color=COLORS["cobalt"]),
                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START),
                padding=ft.padding.Padding(14, 16, 14, 16),
            ),
            ft.Divider(color=COLORS["card_border"], height=1),
            ft.Container(height=8),
            # Items de navegaciÃ³n
            ft.Container(
                content=nav_items,
                padding=ft.padding.Padding(8, 0, 8, 0),
                expand=True
            ),
            # Footer
            ft.Container(
                content=footer_items,
                padding=ft.padding.Padding(14, 0, 14, 14),
            ),
        ], spacing=0, expand=True),
        width=168,
        bgcolor=COLORS["sidebar"],
        border=ft.Border(right=ft.BorderSide(1, COLORS["card_border"])),
        expand=False,
    )


def crear_shell(page, sidebar, main_content, status_bar=None):
    """
    Renderiza el layout principal: sidebar fijo + contenido principal.
    """
    page.clean()
    page.bgcolor = COLORS["bg"]
    page.padding = 0

    contenido = ft.Column([main_content], expand=True, spacing=0)
    if status_bar:
        contenido = ft.Column([
            ft.Container(content=main_content, expand=True),
            status_bar,
        ], spacing=0, expand=True)

    layout = ft.Row([
        sidebar,
        ft.Container(
            content=contenido,
            expand=True,
        )
    ], spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)

    page.add(layout)
    page.update()


# ──────────────── PANTALLA INICIO ──────────────────────────────────────────────────

class PantallaInicio:
    """Pantalla de bienvenida con tarjetas de modos y estadísticas."""

    def __init__(self, page: ft.Page, on_iniciar, on_modo_ia=None, on_guia=None):
        self.page = page
        self.on_iniciar = on_iniciar
        self.on_modo_ia = on_modo_ia
        self.on_guia = on_guia

    def mostrar(self):
        # ── Tarjeta: Consulta por Encuesta ──
        card_consulta = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("Consulta por encuesta", size=24, weight=ft.FontWeight.BOLD,
                                color=COLORS["text_primary"]),
                        ft.Container(height=6),
                        ft.Text("Responde algunas preguntas guiadas paso a paso y encuentra posibles especies locales de forma rápida y confiable.",
                                size=15, color=COLORS["text_secondary"]),
                    ], expand=True, spacing=0),
                    ft.Container(
                        content=ft.Icon(ft.Icons.ASSIGNMENT_ROUNDED, color=COLORS["accent"], size=36),
                        width=64, height=64,
                        bgcolor=COLORS["accent_dim"],
                        border_radius=16,
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=30),
                # Features
                _feature_row(ft.Icons.CHECK_CIRCLE_ROUNDED, COLORS["success"],
                             "Preguntas guiadas por expertos", "Proceso de filtrado dinámico fácil de seguir paso a paso."),
                ft.Container(height=16),
                _feature_row(ft.Icons.SPA_ROUNDED, COLORS["accent"],
                             "Base de datos y conocimiento", "Criterios taxonómicos validados por científicos del Parque."),
                ft.Container(height=16),
                _feature_row(ft.Icons.ADJUST_ROUNDED, COLORS["cobalt"],
                             "Resultados y explicaciones", "Información detallada, distribución y características clave."),
                ft.Container(height=35),
                # Botón iniciar
                ft.Container(
                    content=ft.Row([
                        ft.Text("Iniciar encuesta taxonómica", size=16, weight=ft.FontWeight.BOLD,
                                color=COLORS["bg"]),
                        ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=COLORS["bg"], size=18),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    bgcolor=COLORS["accent"],
                    border_radius=12,
                    padding=ft.padding.Padding(0, 16, 0, 16),
                    on_click=self.on_iniciar,
                    shadow=ft.BoxShadow(blur_radius=20, color=COLORS["accent_dim"],
                                        offset=ft.Offset(0, 4)),
                ),
            ], spacing=0),
            bgcolor=COLORS["card"],
            border_radius=20,
            border=ft.Border.all(1, COLORS["card_border"]),
            padding=32,
            expand=True,
        )

        # ── Tarjeta: IA Assistant ──
        card_ia = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("IA Assistant", size=24, weight=ft.FontWeight.BOLD,
                                color=COLORS["text_primary"]),
                        ft.Container(height=6),
                        ft.Text("Describe las características de tu coral en texto libre para que la IA identifique las especies más probables.",
                                size=15, color=COLORS["text_secondary"]),
                    ], expand=True, spacing=0),
                    ft.Container(
                        content=ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color=COLORS["purple"], size=36),
                        width=64, height=64,
                        bgcolor="#1A8957E5",
                        border_radius=16,
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=30),
                # Paso a paso IA
                ft.Row([
                    _ia_step("1", "Describir",
                             "Describe libremente forma, color o textura.", COLORS["cobalt"]),
                    _ia_step("2", "Analizar",
                             "La IA procesa rasgos morfológicos.", COLORS["purple"]),
                    _ia_step("3", "Identificar",
                             "Obtén similitudes y explicaciones.", COLORS["accent"]),
                ], spacing=12),
                ft.Container(height=35),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color="#FFFFFF", size=18),
                        ft.Text("Buscar especies similares", size=16, weight=ft.FontWeight.BOLD,
                                color="#FFFFFF"),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    bgcolor=COLORS["purple"],
                    border_radius=12,
                    padding=ft.padding.Padding(0, 16, 0, 16),
                    on_click=self.on_modo_ia if self.on_modo_ia else None,
                    shadow=ft.BoxShadow(blur_radius=20, color="#308957E5", offset=ft.Offset(0, 4)),
                ),
            ], spacing=0),
            bgcolor=COLORS["card"],
            border_radius=20,
            border=ft.Border.all(1, COLORS["card_border"]),
            padding=32,
            expand=True,
        )

        # ── Fila de tarjetas ──
        cards_row = ft.Row([card_consulta, card_ia], spacing=24, expand=False)

        # ── Barra de stats inferior ──
        stats_bar = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("Sistema Experto", size=14, color=COLORS["text_secondary"],
                            weight=ft.FontWeight.BOLD),
                    ft.Text("Información general", size=11, color=COLORS["text_muted"]),
                ], spacing=2),
                ft.Container(width=1, height=48, bgcolor=COLORS["card_border"]),
                _stat("41", "Especies\nregistradas", ft.Icons.WATER_ROUNDED, COLORS["accent"]),
                ft.Container(width=1, height=48, bgcolor=COLORS["card_border"]),
                _stat("15", "Familias", ft.Icons.CATEGORY_ROUNDED, COLORS["cobalt"]),
                ft.Container(width=1, height=48, bgcolor=COLORS["card_border"]),
                _stat("2", "Órdenes", ft.Icons.ACCOUNT_TREE_ROUNDED, COLORS["purple"]),
                ft.Container(width=1, height=48, bgcolor=COLORS["card_border"]),
                _stat("100%", "Datos\nverificados", ft.Icons.VERIFIED_ROUNDED, COLORS["success"]),
            ], spacing=40, alignment=ft.MainAxisAlignment.CENTER,
               vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=COLORS["card"],
            border_radius=ft.BorderRadius(0, 0, 0, 0),
            border=ft.Border(top=ft.BorderSide(1, COLORS["card_border"])),
            padding=ft.padding.Padding(24, 20, 24, 20),
        )

        # ── Encabezado de bienvenida ──
        header = ft.Container(
            content=ft.Column([
                ft.Text("Bienvenido al Sistema Experto Taxonómico",
                        size=32, weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                ft.Text("Tu identificador experto de corales del Parque Nacional Los Roques, Venezuela",
                        size=16, color=COLORS["text_secondary"]),
            ], spacing=6),
            padding=ft.padding.Padding(0, 16, 0, 24),
        )

        # ── Contenido principal ──
        main_content = ft.Container(
            content=ft.Column([
                header,
                ft.Container(content=cards_row, expand=False),
            ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE),
            padding=ft.padding.Padding(36, 28, 36, 0),
            expand=True,
        )

        sidebar = crear_sidebar(
            self.page,
            active_screen="inicio",
            on_consulta=self.on_iniciar,
            on_ia=self.on_modo_ia,
            on_guia=self.on_guia,
        )

        crear_shell(self.page, sidebar, main_content, status_bar=stats_bar)

    def _mostrar_creditos_dialog(self):
        dialog = ft.AlertDialog(
            bgcolor=COLORS["card"],
            title=ft.Text("ðŸ“š CrÃ©ditos del Sistema", color=COLORS["text_primary"],
                          size=16, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("Desarrollado para el curso de Sistemas Expertos (Los Roques, Venezuela)",
                        size=12, color=COLORS["text_secondary"]),
                ft.Divider(color=COLORS["card_border"]),
                ft.Text("Clave taxonÃ³mica basada en:", size=12, color=COLORS["text_primary"],
                        weight=ft.FontWeight.BOLD),
                ft.Text("â€¢ Villamizar et al. (2015) - Diversidad de corales en Los Roques",
                        size=10, color=COLORS["text_secondary"]),
                ft.Text("â€¢ Beltran-Torres & Carricart (1999) - Clave del AtlÃ¡ntico",
                        size=10, color=COLORS["text_secondary"]),
                ft.Divider(color=COLORS["card_border"]),
                ft.Text("â€¢ 41 especies de corales pÃ©treos e hidrocorales locales",
                        size=10, color=COLORS["accent"]),
                ft.Text("â€¢ 15 familias registradas en Los Roques",
                        size=10, color=COLORS["accent"]),
            ], tight=True, spacing=6),
            actions=[
                ft.TextButton("Cerrar",
                              style=ft.ButtonStyle(color=COLORS["accent"]),
                              on_click=lambda e: self._cerrar_dialog(dialog)),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _cerrar_dialog(self, dialog):
        dialog.open = False
        self.page.update()


def _feature_row(icon, color, title, subtitle):
    return ft.Row([
        ft.Container(
            content=ft.Icon(icon, color=color, size=22),
            width=40, height=40,
            bgcolor=COLORS["surface"],
            border_radius=10,
            alignment=ft.alignment.Alignment(0, 0),
        ),
        ft.Column([
            ft.Text(title, size=15, weight=ft.FontWeight.W_600, color=COLORS["text_primary"]),
            ft.Text(subtitle, size=12, color=COLORS["text_secondary"]),
        ], spacing=1, expand=True),
    ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER)


def _ia_step(num, title, desc, color):
    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(num, size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                width=30, height=30, border_radius=15,
                bgcolor=color, alignment=ft.alignment.Alignment(0, 0),
            ),
            ft.Container(height=8),
            ft.Text(title, size=14, weight=ft.FontWeight.W_600, color=COLORS["text_primary"]),
            ft.Text(desc, size=12, color=COLORS["text_secondary"]),
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        alignment=ft.alignment.Alignment(0, -1),
    )


def _stat(value, label, icon, color):
    return ft.Row([
        ft.Icon(icon, color=color, size=24),
        ft.Column([
            ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=color),
            ft.Text(label, size=12, color=COLORS["text_secondary"]),
        ], spacing=0),
    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)


# â”€â”€â”€ PANTALLA PREGUNTAS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class PantallaPreguntas:
    """Pantalla para resolver cada paso de la clave dicotÃ³mica con sidebar."""

    def __init__(self, page: ft.Page, pregunta, numero, total,
                 on_responder, on_volver):
        self.page = page
        self.pregunta = pregunta
        self.numero = numero
        self.total = total
        self.on_responder = on_responder
        self.on_volver = on_volver

    def mostrar(self):
        # â”€â”€ Cabecera de la pantalla â”€â”€
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                color=COLORS["text_secondary"], size=14),
                        ft.Text("Volver al inicio", size=12, color=COLORS["text_secondary"]),
                    ], spacing=6),
                    on_click=lambda _: self.on_volver(),
                    padding=ft.padding.Padding(0, 4, 12, 4),
                ),
                ProgressStepper(current=min(self.numero, 5), total=5),
                ft.Text(f"Paso {self.numero}", size=11,
                        color=COLORS["text_secondary"], weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.Padding(0, 0, 0, 24),
        )

        # â”€â”€ Texto de la pregunta â”€â”€
        pregunta_card = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("PREGUNTA TAXONÃ“MICA", size=10,
                                    color=COLORS["accent"], weight=ft.FontWeight.BOLD),
                    bgcolor=COLORS["accent_dim"],
                    border_radius=4,
                    padding=ft.padding.Padding(8, 4, 8, 4),
                ),
                ft.Container(height=12),
                ft.Text(
                    self.pregunta.get("texto", ""),
                    size=18, weight=ft.FontWeight.BOLD,
                    color=COLORS["text_primary"],
                ),
                ft.Container(height=6),
                ft.Text(
                    self.pregunta.get("descripcion", ""),
                    size=12, color=COLORS["text_secondary"],
                ) if self.pregunta.get("descripcion") else ft.Container(),
            ], spacing=0),
            bgcolor=COLORS["card"],
            border_radius=14,
            border=ft.Border.all(1, COLORS["card_border"]),
            padding=20,
        )

        # â”€â”€ Opciones de respuesta â”€â”€
        opciones_lista = self.pregunta.get("opciones", [])
        opciones_controls = []

        def on_hover_opt(e):
            c = e.control
            h = e.data == "true"
            c.bgcolor = "#20388BFD" if h else COLORS["surface"]
            c.border = ft.Border.all(1.5, COLORS["cobalt"] if h else COLORS["card_border"])
            c.update()

        for op in opciones_lista:
            icono = ft.Icons.HELP_OUTLINE_ROUNDED
            lbl = op["label"].lower()
            if "ramificado" in lbl or "rama" in lbl:
                icono = ft.Icons.SPA_ROUNDED
            elif "laminar" in lbl or "hoja" in lbl or "lÃ¡mina" in lbl:
                icono = ft.Icons.LAYERS_ROUNDED
            elif "solitario" in lbl:
                icono = ft.Icons.ADJUST_ROUNDED
            elif "colonial" in lbl or "muchos" in lbl:
                icono = ft.Icons.GRID_VIEW_ROUNDED
            elif "sÃ­" in lbl or "si" in lbl or "tiene" in lbl:
                icono = ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED
            elif "no" in lbl or "sin" in lbl:
                icono = ft.Icons.HIGHLIGHT_OFF_ROUNDED
            elif "masiv" in lbl or "globos" in lbl:
                icono = ft.Icons.CIRCLE_ROUNDED
            elif "incrustante" in lbl:
                icono = ft.Icons.TERRAIN_ROUNDED

            def make_handler(val=op["valor"]):
                return lambda _: self.on_responder(val)

            btn_opcion = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(icono, color=COLORS["cobalt"], size=20),
                        width=36, height=36,
                        bgcolor=COLORS["cobalt_dim"],
                        border_radius=10,
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                    ft.Text(op["label"], size=13, weight=ft.FontWeight.W_500,
                            color=COLORS["text_primary"], expand=True),
                    ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
                            color=COLORS["text_muted"], size=18),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=COLORS["surface"],
                border_radius=12,
                border=ft.Border.all(1, COLORS["card_border"]),
                padding=16,
                on_hover=on_hover_opt,
                on_click=make_handler(),
            )
            opciones_controls.append(btn_opcion)

        opciones_col = ft.Column(opciones_controls, spacing=10)

        # â”€â”€ Panel izquierdo â€” pregunta y opciones â”€â”€
        panel_izq = ft.Container(
            content=ft.Column([
                header,
                pregunta_card,
                ft.Container(height=16),
                ft.Text("Selecciona una opciÃ³n:", size=11,
                        color=COLORS["text_secondary"], weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                opciones_col,
            ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE),
            expand=3,
            padding=ft.padding.Padding(28, 24, 20, 24),
        )

        # â”€â”€ Panel derecho â€” candidatos taxonÃ³micos â”€â”€
        respuestas_actuales = {}
        if hasattr(self.page, "respuestas_acumuladas"):
            respuestas_actuales = self.page.respuestas_acumuladas

        candidatos = filtrar_candidatos(respuestas_actuales)

        candidatos_views = []
        for c in candidatos:
            grupo_color = {
                "hidrocoral": "#FF6B35",
                "ramificado": COLORS["accent"],
                "solitario":  COLORS["cobalt"],
                "laminar":    COLORS["purple"],
                "masivo":     COLORS["success"],
            }.get(c["grupo"], COLORS["text_secondary"])

            card_c = ft.Container(
                content=ft.Row([
                    ft.Container(
                        width=6, height=6,
                        bgcolor=grupo_color,
                        border_radius=3,
                    ),
                    ft.Column([
                        ft.Text(c["nombre"], size=11, weight=ft.FontWeight.W_600,
                                color=COLORS["text_primary"],
                                overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(c["familia"], size=9, color=COLORS["text_muted"]),
                    ], spacing=1, expand=True),
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.Padding(8, 8, 8, 8),
                border=ft.Border(bottom=ft.BorderSide(1, COLORS["card_border"])),
            )
            candidatos_views.append(card_c)

        badge_count = ft.Container(
            content=ft.Text(
                f"{len(candidatos)} CANDIDATOS COINCIDENTES",
                size=9, color=COLORS["accent"], weight=ft.FontWeight.BOLD,
            ),
            bgcolor=COLORS["accent_dim"],
            border_radius=4,
            padding=ft.padding.Padding(8, 4, 8, 4),
        )

        panel_der = ft.Container(
            content=ft.Column([
                ft.Text("Candidatos TaxonÃ³micos", size=14,
                        weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                ft.Text("Especies que coinciden con tus respuestas",
                        size=11, color=COLORS["text_secondary"]),
                ft.Container(height=12),
                badge_count,
                ft.Container(height=8),
                ft.Column(
                    candidatos_views,
                    spacing=0,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                ),
            ], spacing=0, expand=True),
            bgcolor=COLORS["card"],
            border_radius=0,
            border=ft.Border(left=ft.BorderSide(1, COLORS["card_border"])),
            padding=ft.padding.Padding(20, 24, 20, 24),
            expand=2,
        )

        main_content = ft.Row([
            panel_izq,
            panel_der,
        ], spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)

        sidebar = crear_sidebar(
            self.page,
            active_screen="consulta",
            on_inicio=self.on_volver,
        )

        crear_shell(self.page, sidebar, main_content)


# â”€â”€â”€ PANTALLA RESULTADO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class PantallaResultado:
    """Pantalla final que resume el diagnÃ³stico taxonÃ³mico."""

    def __init__(self, page: ft.Page, resultado, historial, on_reiniciar):
        self.page = page
        self.resultado = resultado
        self.historial = historial
        self.on_reiniciar = on_reiniciar

    def mostrar(self):
        if hasattr(self.page, "respuestas_acumuladas"):
            self.page.respuestas_acumuladas = {}

        is_success = self.resultado.get("success", True)
        color_status = COLORS["success"] if is_success else COLORS["warning"]

        # â”€â”€ Cabecera de resultado â”€â”€
        estado_badge = ft.Container(
            content=ft.Text(
                "IDENTIFICADO" if is_success else "NO IDENTIFICADO",
                size=10, color=COLORS["bg"], weight=ft.FontWeight.BOLD,
            ),
            bgcolor=color_status,
            border_radius=6,
            padding=ft.padding.Padding(10, 4, 10, 4),
        )

        resultado_header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("DIAGNÃ“STICO TAXONÃ“MICO", size=10,
                            color=COLORS["text_secondary"], weight=ft.FontWeight.BOLD),
                    ft.Container(width=8, height=8, bgcolor=color_status, border_radius=4),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=20),
                # CÃ­rculo de porcentaje
                ft.Row([
                    ft.Container(
                        content=ft.Text(
                            "96%" if is_success else "â€“",
                            size=20, weight=ft.FontWeight.BOLD, color=color_status,
                        ),
                        width=72, height=72,
                        border_radius=36,
                        border=ft.Border.all(3, color_status),
                        alignment=ft.alignment.Alignment(0, 0),
                        shadow=ft.BoxShadow(blur_radius=16, color=color_status + "50",
                                            spread_radius=-2),
                    ),
                    ft.Container(width=16),
                    ft.Column([
                        estado_badge,
                        ft.Container(height=8),
                        ft.Text(
                            self.resultado.get("especie", "No identificada"),
                            size=18, weight=ft.FontWeight.W_300,
                            color=COLORS["text_primary"],
                        ),
                        ft.Text(
                            self.resultado.get("nombre_comun", ""),
                            size=12, color=COLORS["text_secondary"],
                        ) if self.resultado.get("nombre_comun") else ft.Container(),
                    ], spacing=0),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=20),
                # Badges familia / orden
                ft.Row([
                    _badge_info("Familia", self.resultado.get("familia", "N/A"), color_status),
                    ft.Container(width=8),
                    _badge_info("Orden", self.resultado.get("orden", "N/A"),
                                COLORS["text_secondary"]),
                ]),
            ], spacing=0),
            bgcolor=COLORS["card"],
            border_radius=14,
            border=ft.Border.all(1, COLORS["card_border"]),
            padding=20,
        )

        # â”€â”€ Mensaje de fallo â”€â”€
        mensaje_excluido = ft.Container(
            content=ft.Column([
                ft.Text(self.resultado.get("mensaje", ""), size=12,
                        weight=ft.FontWeight.BOLD, color=COLORS["warning"]),
                ft.Text(self.resultado.get("sugerencia", ""), size=11,
                        color=COLORS["text_secondary"]),
            ], spacing=4),
            padding=12,
            bgcolor="#25D29922",
            border_radius=10,
            border=ft.Border.all(1, COLORS["warning"] + "40"),
        ) if not is_success else ft.Container()

        # â”€â”€ Botones de acciÃ³n â”€â”€
        btn_nuevo = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.REFRESH_ROUNDED, color="#FFFFFF", size=16),
                ft.Text("Nueva Consulta", size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor=COLORS["cobalt"],
            border_radius=10,
            padding=ft.padding.Padding(0, 14, 0, 14),
            on_click=self.on_reiniciar,
            shadow=ft.BoxShadow(blur_radius=20, color=COLORS["cobalt_glow"],
                                offset=ft.Offset(0, 4)),
        )

        btn_exportar = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.DOWNLOAD_ROUNDED, color=COLORS["text_secondary"], size=14),
                ft.Text("Exportar Resultado", size=12, color=COLORS["text_secondary"]),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            on_click=lambda _: self._guardar_resultado(),
            padding=ft.padding.Padding(0, 10, 0, 10),
            border_radius=8,
            border=ft.Border.all(1, COLORS["card_border"]),
            bgcolor=COLORS["surface"],
        )

        # â”€â”€ Panel izquierdo â”€â”€
        panel_izq = ft.Container(
            content=ft.Column([
                resultado_header,
                ft.Container(height=12),
                mensaje_excluido,
                ft.Container(height=16),
                btn_nuevo,
                ft.Container(height=8),
                btn_exportar,
            ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE),
            expand=2,
            padding=ft.padding.Padding(28, 24, 20, 24),
        )

        # â”€â”€ Panel derecho: traza de inferencia â”€â”€
        trace_views = []
        for i, item in enumerate(self.historial):
            trace_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text(str(i + 1), size=8, color="#FFFFFF",
                                            weight=ft.FontWeight.BOLD),
                            bgcolor=COLORS["sidebar_active"],
                            width=18, height=18,
                            border_radius=9,
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                        ft.Text(item["pregunta"], size=11, color=COLORS["text_secondary"],
                                weight=ft.FontWeight.W_500, expand=True,
                                overflow=ft.TextOverflow.ELLIPSIS),
                    ], spacing=8),
                    ft.Container(
                        content=ft.Text(item["respuesta"], size=12,
                                        color=color_status, weight=ft.FontWeight.BOLD),
                        padding=ft.padding.Padding(26, 0, 0, 0),
                    ),
                ], spacing=4),
                padding=ft.padding.Padding(0, 10, 0, 10),
                border=ft.Border(bottom=ft.BorderSide(1, COLORS["card_border"])),
            )
            trace_views.append(trace_card)

        panel_der = ft.Container(
            content=ft.Column([
                ft.Text("Traza de Inferencia", size=14,
                        weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                ft.Text("LÃ³gica deductiva empleada", size=11, color=COLORS["text_secondary"]),
                ft.Container(height=16),
                ft.Column(
                    trace_views if trace_views else [
                        ft.Text("Sin pasos registrados.", size=12,
                                color=COLORS["text_muted"])
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                ),
            ], spacing=0, expand=True),
            bgcolor=COLORS["card"],
            border=ft.Border(left=ft.BorderSide(1, COLORS["card_border"])),
            border_radius=0,
            padding=ft.padding.Padding(20, 24, 20, 24),
            expand=3,
        )

        main_content = ft.Row([
            panel_izq,
            panel_der,
        ], spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)

        sidebar = crear_sidebar(
            self.page,
            active_screen="consulta",
            on_inicio=self.on_reiniciar,
            on_consulta=self.on_reiniciar,
        )

        crear_shell(self.page, sidebar, main_content)

    def _badge_info(self, label, val, color):
        return _badge_info(label, val, color)

    def _guardar_resultado(self):
        import datetime
        filename = f"resultado_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== CORAL EXPERT SYSTEM - LOS ROQUES ===\n")
            f.write(f"Fecha: {datetime.datetime.now()}\n\n")
            f.write(f"Especie: {self.resultado.get('especie', 'No identificada')}\n")
            f.write(f"Nombre comÃºn: {self.resultado.get('nombre_comun', 'N/A')}\n")
            f.write(f"Familia: {self.resultado.get('familia', 'Desconocida')}\n")
            f.write(f"Orden: {self.resultado.get('orden', 'Desconocido')}\n")
            f.write(f"Estado: {'Identificado' if self.resultado.get('success', True) else 'No identificado'}\n")
            if self.resultado.get("mensaje"):
                f.write(f"Mensaje: {self.resultado['mensaje']}\n")
            f.write(f"\nTraza de inferencia:\n")
            for i, item in enumerate(self.historial):
                f.write(f"{i+1}. {item['pregunta']} â†’ {item['respuesta']}\n")

        snack = ft.SnackBar(
            ft.Text(f"âœ… Resultado guardado en {filename}",
                    color=COLORS["bg"], weight=ft.FontWeight.BOLD),
            bgcolor=COLORS["accent"],
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()


def _badge_info(label, val, color):
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=9, color=COLORS["text_secondary"]),
            ft.Text(val, size=12, weight=ft.FontWeight.BOLD, color=color),
        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=COLORS["surface"],
        border_radius=10,
        border=ft.Border.all(1, COLORS["card_border"]),
        padding=10,
        expand=True,
    )


# â”€â”€â”€ PANTALLA GUÃA DE CORALES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class PantallaGuia:
    """Catálogo navegable de todas las especies registradas."""

    def __init__(self, page: ft.Page, on_volver):
        self.page = page
        self.on_volver = on_volver
        self._todas = []
        self._overlay_ref = None
        self._load_especies()

    def _load_especies(self):
        import os
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(base, "data", "especies.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._todas = json.load(f)
        except Exception:
            self._todas = []

    def mostrar(self):
        grid_ref = ft.Ref()

        def hover_card(e):
            e.control.border = ft.Border.all(1, COLORS["accent"] if e.data == "true" else COLORS["card_border"])
            e.control.shadow = ft.BoxShadow(blur_radius=12, color=COLORS["accent"] + "15", offset=ft.Offset(0, 4)) if e.data == "true" else None
            e.control.update()

        def renderizar(filtro=""):
            cards = []
            for esp in self._todas:
                nc = esp.get("nombre_comun", "").lower()
                nci = esp.get("nombre_cientifico", "").lower()
                if filtro and filtro.lower() not in nc and filtro.lower() not in nci:
                    continue

                grupo = esp.get("tipo", "Coral")
                grupo_color = {
                    "Hidrocoral": "#FF6B35",
                    "Escleractinia": COLORS["accent"],
                }.get(grupo, COLORS["cobalt"])

                card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(grupo[0], size=10, weight=ft.FontWeight.BOLD,
                                                color=grupo_color),
                                width=28, height=28,
                                bgcolor=grupo_color + "25",
                                border_radius=8,
                                alignment=ft.alignment.Alignment(0, 0),
                            ),
                            ft.Container(
                                content=ft.Text(grupo.upper(), size=9,
                                                color=grupo_color, weight=ft.FontWeight.BOLD),
                                bgcolor=grupo_color + "15",
                                border_radius=4,
                                padding=ft.padding.Padding(6, 2, 6, 2),
                            ),
                        ], spacing=8),
                        ft.Container(height=10),
                        ft.Text(esp.get("nombre_comun", ""), size=13,
                                weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                        ft.Text(esp.get("nombre_cientifico", ""), size=11,
                                color=COLORS["text_secondary"], italic=True),
                        ft.Divider(color=COLORS["card_border"], height=12),
                        ft.Row([
                            ft.Icon(ft.Icons.PLACE_ROUNDED, size=11,
                                    color=COLORS["text_muted"]),
                            ft.Text(esp.get("habitat", "")[:50] + "…"
                                    if len(esp.get("habitat", "")) > 50
                                    else esp.get("habitat", ""),
                                    size=10, color=COLORS["text_muted"], expand=True,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                        ], spacing=4),
                        ft.Container(height=6),
                        ft.Text(
                            esp.get("descripcion", "")[:100] + "…"
                            if len(esp.get("descripcion", "")) > 100
                            else esp.get("descripcion", ""),
                            size=11, color=COLORS["text_secondary"],
                            overflow=ft.TextOverflow.ELLIPSIS, max_lines=3,
                        ),
                        ft.Row([
                            ft.Text(f"Familia: {esp.get('familia', 'N/A')}",
                                    size=10, color=COLORS["text_muted"]),
                        ]),
                    ], spacing=0),
                    bgcolor=COLORS["card"],
                    border_radius=12,
                    border=ft.Border.all(1, COLORS["card_border"]),
                    padding=16,
                    col={"sm": 12, "md": 6, "lg": 4},
                    on_click=lambda _, e=esp: self._abrir_modal(e),
                    on_hover=hover_card,
                )
                cards.append(card)
            return cards

        self._grid = ft.ResponsiveRow(renderizar(), spacing=12)

        search_field = ft.TextField(
            hint_text="Buscar por nombre común o científico…",
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            bgcolor=COLORS["surface"],
            border_color=COLORS["card_border"],
            focused_border_color=COLORS["cobalt"],
            border_radius=10,
            color=COLORS["text_primary"],
            hint_style=ft.TextStyle(color=COLORS["text_muted"]),
            height=44,
            text_size=13,
            on_change=lambda e: self._actualizar_grid(e.control.value, renderizar),
        )

        main_content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("Guía de Corales", size=22,
                                weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                        ft.Text(f"{len(self._todas)} especies del Parque Nacional Los Roques",
                                size=13, color=COLORS["text_secondary"]),
                    ], spacing=2, expand=True),
                    ft.Container(
                        content=ft.Text(f"{len(self._todas)}", size=24,
                                        weight=ft.FontWeight.BOLD, color=COLORS["accent"]),
                        padding=ft.padding.Padding(16, 8, 16, 8),
                        bgcolor=COLORS["accent_dim"],
                        border_radius=12,
                    ),
                ]),
                ft.Container(height=16),
                search_field,
                ft.Container(height=16),
                ft.Container(content=self._grid, expand=True),
            ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE),
            padding=ft.padding.Padding(28, 24, 28, 24),
            expand=True,
        )

        sidebar = crear_sidebar(
            self.page,
            active_screen="guia"
        )

        crear_shell(self.page, sidebar, main_content)

    def _actualizar_grid(self, filtro, renderizar_fn):
        self._grid.controls = renderizar_fn(filtro)
        self._grid.update()

    def _abrir_modal(self, esp):
        import os
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        imagenes_dir = os.path.join(base, "data", "Imagenes")

        # Buscar imagen
        tiene_imagen = False
        img_path = ""
        for ext in [".jpg", ".jpeg", ".png", ".JPG", ".PNG", ".JPEG"]:
            p = os.path.join(imagenes_dir, f"{esp.get('id')}{ext}")
            if os.path.isfile(p):
                img_path = p
                tiene_imagen = True
                break

        # Construir columnas/filas para mostrar características
        filas_caract = []
        caract = esp.get("caracteristicas", {})
        
        traducciones_caract = {
            "tiene_coralitos": "Tiene coralitos",
            "forma": "Forma de la colonia",
            "tipo_esqueleto": "Tipo de esqueleto",
            "urticante": "Urticante (ortiga)",
            "color": "Color de colonia",
            "ramas_aplanadas": "Ramas aplanadas",
            "ramas_largas_fusionadas": "Tipo de ramificaciones",
            "coralitos_en": "Posición de coralitos",
            "septos": "Bordes de septos",
            "columela": "Tiene columela",
            "copas_ovales": "Copas ovaladas",
            "copas_circulares": "Copas circulares",
            "copas_apiñadas": "Copas apiñadas",
            "colinas_valles": "Forma de la colonia",
            "valles_anchura": "Anchura de valles",
            "columela_estiliforme": "Columela estiliforme",
            "copas_ancho": "Ancho de copas",
            "copas_separadas": "Copas separadas",
            "superficie_irregular": "Superficie irregular",
            "crecimiento_columnar": "Crecimiento columnar",
        }

        for k, v in caract.items():
            k_friendly = traducciones_caract.get(k, k.replace("_", " ").capitalize())
            v_friendly = "Sí" if v is True else ("No" if v is False else str(v).replace("_", " ").capitalize())
            
            filas_caract.append(ft.Container(
                content=ft.Row([
                    ft.Text(k_friendly, size=11, color=COLORS["text_secondary"], weight=ft.FontWeight.BOLD),
                    ft.Text(v_friendly, size=11, color=COLORS["accent"], weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.Padding(0, 6, 0, 6),
                border=ft.Border(bottom=ft.BorderSide(1, COLORS["card_border"])),
            ))

        if tiene_imagen:
            imagen_widget = ft.Image(
                src=img_path,
                width=160,
                height=160,
                fit="cover",
                border_radius=ft.BorderRadius(12, 12, 12, 12),
            )
        else:
            imagen_widget = ft.Container(
                content=ft.Icon(ft.Icons.SPA_ROUNDED, color=COLORS["text_secondary"], size=40),
                width=160, height=160,
                bgcolor=COLORS["surface"],
                border_radius=12,
                alignment=ft.alignment.Alignment(0, 0),
            )

        modal_content = ft.Container(
            content=ft.Column([
                # Fila Cabecera
                ft.Row([
                    imagen_widget,
                    ft.Container(width=16),
                    ft.Column([
                        ft.Text(esp.get("nombre_cientifico", ""), size=20,
                                weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                        ft.Text(esp.get("nombre_comun", ""), size=14,
                                color=COLORS["text_secondary"]),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Text(esp.get("tipo", "Coral").upper(), size=10,
                                            color=COLORS["accent"], weight=ft.FontWeight.BOLD),
                            bgcolor=COLORS["accent_dim"],
                            border_radius=20,
                            padding=ft.padding.Padding(10, 4, 10, 4),
                        ),
                        ft.Container(height=6),
                        ft.Text(f"Familia: {esp.get('familia', 'N/A')}  ·  Orden: {esp.get('orden', 'N/A')}",
                                size=10, color=COLORS["text_muted"]),
                    ], spacing=0, expand=True),
                ], vertical_alignment=ft.CrossAxisAlignment.START),

                ft.Divider(color=COLORS["card_border"], height=24),

                # Contenido con scroll
                ft.Column([
                    ft.Text("CARACTERÍSTICAS TAXONÓMICAS", size=10,
                            color=COLORS["text_secondary"], weight=ft.FontWeight.BOLD),
                    ft.Container(height=8),
                    ft.Column(filas_caract, spacing=0),
                    
                    ft.Container(height=20),

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
                    
                    ft.Container(height=14),
                    
                    # Hábitat
                    ft.Text("HÁBITAT", size=10, color=COLORS["text_secondary"],
                            weight=ft.FontWeight.BOLD),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PLACE_ROUNDED, color=COLORS["cobalt"], size=13),
                            ft.Text(esp.get("habitat", "Hábitat no especificado."),
                                    size=11, color=COLORS["text_secondary"], expand=True),
                        ], spacing=6),
                        padding=12,
                        bgcolor=COLORS["surface"],
                        border_radius=10,
                        border=ft.Border.all(1, COLORS["card_border"]),
                    ),
                ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE, expand=True),
                
                ft.Divider(color=COLORS["card_border"], height=24),
                
                # Botón de Cerrar
                ft.Container(
                    content=ft.Text("Cerrar Detalle", size=14, color=COLORS["bg"], weight=ft.FontWeight.BOLD),
                    bgcolor=COLORS["accent"],
                    border_radius=10,
                    padding=ft.padding.Padding(0, 12, 0, 12),
                    alignment=ft.alignment.Alignment(0, 0),
                    on_click=lambda _: self._cerrar_modal(),
                ),
            ], spacing=0, expand=True),
            padding=28,
            bgcolor=COLORS["card"],
            border_radius=16,
            border=ft.Border.all(1, COLORS["card_border"]),
            shadow=ft.BoxShadow(blur_radius=40, color="#80000000", offset=ft.Offset(0, 8)),
            width=680,
            height=600,
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
        if hasattr(self, "_overlay_ref") and self._overlay_ref and self._overlay_ref in self.page.overlay:
            self.page.overlay.remove(self._overlay_ref)
            self._overlay_ref = None
            self.page.update()

