import flet as ft
from base_conocimiento import BaseConocimiento
from motor_inferencia import MotorInferencia
from explicacion import GeneradorExplicacion

class SistemaExpertoGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema Experto Taxonómico - Los Roques"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        
        # Paleta de colores marinos premium
        self.color_bg = "#0B132B"       # Deep blue oscuro
        self.color_card = "#1C2541"     # Navy azul oscuro
        self.color_primary = "#3A86C8"  # Azul océano
        self.color_accent = "#00F5D4"   # Turquesa brillante
        self.color_text = "#F8FAFC"     # Blanco suave
        self.color_subtext = "#94A3B8"  # Gris suave
        
        # Configurar colores de la página
        self.page.bgcolor = self.color_bg
        
        # Inicializar lógica del Sistema Experto
        try:
            self.bc = BaseConocimiento()
            self.motor = MotorInferencia(self.bc)
            self.explicador = GeneradorExplicacion()
        except Exception as e:
            self.show_error_dialog(f"Error al cargar base de conocimiento: {str(e)}")
            return
            
        # Variables de estado del diagnóstico
        self.hechos = {}
        self.historial_hechos = []  # Pila de estados previos para función "Atrás"
        
        # Contenedor principal que se refrescará para simular pantallas
        self.main_container = ft.Container(expand=True)
        self.page.add(self.main_container)
        
        # Mostrar pantalla inicial
        self.mostrar_bienvenida()

    def show_error_dialog(self, message):
        def cerrar_dialog(e):
            dialog.open = False
            self.page.update()
            
        dialog = ft.AlertDialog(
            title=ft.Text("Error del Sistema"),
            content=ft.Text(message),
            actions=[ft.TextButton("Aceptar", on_click=cerrar_dialog)]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def limpiar_pantalla(self):
        self.main_container.content = None
        self.page.update()

    def mostrar_bienvenida(self):
        self.limpiar_pantalla()
        
        # Header con gradiente premium
        header = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon=ft.icons.WATER_DROP_ROUNDED, size=50, color=self.color_accent),
                    ft.Text(
                        "SISTEMA EXPERTO TAXONÓMICO",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=self.color_text,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Clave Taxonómica Dicotómica de Los Roques",
                        size=16,
                        color=self.color_accent,
                        text_align=ft.TextAlign.CENTER,
                        italic=True
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[self.color_card, "#1E293B"]
            ),
            alignment=ft.alignment.center
        )
        
        # Tarjeta informativa
        intro_card = ft.Container(
            content=ft.Text(
                "Este sistema experto interactivo le guiará a través de preguntas dicotómicas morfológicas para identificar las especies marinas más representativas del Parque Nacional Archipiélago de Los Roques, explicando el razonamiento lógico científico utilizado.",
                size=15,
                color=self.color_subtext,
                text_align=ft.TextAlign.CENTER
            ),
            padding=20,
            bgcolor=self.color_card,
            border_radius=15,
            border=ft.border.all(1, "#334155")
        )
        
        # Botones de acción principal
        btn_diagnostico = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(icon=ft.icons.SEARCH_ROUNDED, color=self.color_bg),
                        ft.Text("INICIAR DIAGNÓSTICO", weight=ft.FontWeight.BOLD, size=16, color=self.color_bg)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                style=ft.ButtonStyle(
                    bgcolor={"": self.color_accent},
                    shape={"": ft.RoundedRectangleBorder(radius=10)},
                ),
                height=55,
                on_click=lambda _: self.iniciar_diagnostico()
            ),
            expand=True
        )
        
        btn_catalogo = ft.Container(
            content=ft.OutlinedButton(
                content=ft.Row(
                    [
                        ft.Icon(icon=ft.icons.MENU_BOOK_ROUNDED, color=self.color_accent),
                        ft.Text("EXPLORAR ESPECIES", weight=ft.FontWeight.BOLD, size=16, color=self.color_accent)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                style=ft.ButtonStyle(
                    side={"": ft.BorderSide(2, self.color_accent)},
                    shape={"": ft.RoundedRectangleBorder(radius=10)},
                ),
                height=55,
                on_click=lambda _: self.mostrar_catalogo()
            ),
            expand=True
        )
        
        botones = ft.Row([btn_diagnostico, btn_catalogo], spacing=20, width=500)
        
        # Layout vertical centralizado
        layout = ft.Column(
            [
                header,
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                intro_card,
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Container(content=botones, alignment=ft.alignment.center),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.ADAPTIVE
        )
        
        self.main_container.content = ft.Container(
            content=layout,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(vertical=40)
        )
        self.page.update()

    def iniciar_diagnostico(self):
        self.hechos = {}
        self.historial_hechos = []
        self.procesar_paso_diagnostico()

    def procesar_paso_diagnostico(self):
        self.limpiar_pantalla()
        
        # Evaluar el estado actual del motor de inferencia
        resultado_eval = self.motor.evaluar(self.hechos)
        estado = resultado_eval["estado"]
        camino = resultado_eval["camino"]
        
        # Barra de progreso simulada basada en el camino
        progress_val = min(len(camino) / 4.0, 1.0)
        
        # 1. Cabecera del diagnóstico
        progress_bar = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(f"Paso {len(camino) + 1}", size=14, color=self.color_accent, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{int(progress_val * 100)}% completado", size=12, color=self.color_subtext)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.ProgressBar(value=progress_val, color=self.color_accent, bgcolor="#1E293B", height=8),
            ],
            spacing=5
        )
        
        # Si requiere hacer una pregunta
        if estado == "pregunta":
            pregunta_texto = resultado_eval["pregunta"]
            atributo = resultado_eval["atributo"]
            opciones = resultado_eval["opciones"]
            
            # Tarjeta de pregunta
            pregunta_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            pregunta_texto,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=self.color_text,
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=30,
                bgcolor=self.color_card,
                border_radius=15,
                border=ft.border.all(1, "#334155"),
                alignment=ft.alignment.center
            )
            
            # Botones de opciones
            opciones_col = ft.Column(spacing=15)
            for opcion in opciones:
                def crear_on_click(opt=opcion):
                    return lambda _: self.responder_pregunta(atributo, opt)
                
                opciones_col.controls.append(
                    ft.Container(
                        content=ft.ElevatedButton(
                            content=ft.Text(opcion.capitalize(), size=16, color=self.color_text),
                            style=ft.ButtonStyle(
                                bgcolor={"": "#1E293B", "hovered": self.color_primary},
                                shape={"": ft.RoundedRectangleBorder(radius=8)},
                                padding={"": ft.padding.all(20)}
                            ),
                            on_click=crear_on_click(),
                        ),
                        width=450
                    )
                )
            
            # Panel de Camino Recorrido (Historial interactivo lateral/inferior)
            historial_list = ft.Column(spacing=8)
            for p, r in camino:
                historial_list.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(icon=ft.icons.CHECK, color=self.color_accent, size=16),
                                ft.Text(f"{p} ➜ ", size=12, color=self.color_subtext),
                                ft.Text(r, size=12, color=self.color_accent, weight=ft.FontWeight.BOLD)
                            ]
                        ),
                        bgcolor="#0F172A",
                        padding=ft.padding.symmetric(horizontal=10, vertical=8),
                        border_radius=6
                    )
                )
                
            panel_historial = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Razonamiento Acumulado:", size=14, weight=ft.FontWeight.BOLD, color=self.color_text),
                        ft.Divider(color="#334155", height=10),
                        ft.Container(content=historial_list, height=150)
                    ]
                ),
                padding=15,
                bgcolor=self.color_card,
                border_radius=10,
                border=ft.border.all(1, "#334155")
            )
            
            # Botones de Control (Atrás y Cancelar)
            btn_atras = ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                icon_color=self.color_text,
                tooltip="Regresar a la pregunta anterior",
                disabled=len(self.historial_hechos) == 0,
                on_click=lambda _: self.retroceder_pregunta()
            )
            
            btn_cancelar = ft.TextButton(
                "Cancelar Diagnóstico",
                icon=ft.icons.CLOSE,
                icon_color="red",
                on_click=lambda _: self.mostrar_bienvenida()
            )
            
            controles_flujo = ft.Row(
                [btn_atras, btn_cancelar],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            
            # Armar pantalla final de pregunta
            diagnostico_layout = ft.Column(
                [
                    progress_bar,
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    pregunta_card,
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.Container(content=opciones_col, alignment=ft.alignment.center),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    panel_historial if camino else ft.Container(),
                    ft.Divider(color="#334155"),
                    controles_flujo
                ],
                spacing=10,
                scroll=ft.ScrollMode.ADAPTIVE
            )
            
            self.main_container.content = ft.Container(
                content=diagnostico_layout,
                padding=20,
                width=800,
                alignment=ft.alignment.center
            )
            
        elif estado == "exito":
            self.mostrar_resultado_exito(resultado_eval["resultado"], camino)
            
        elif estado == "fallo":
            self.mostrar_resultado_fallo(resultado_eval["mensaje"], camino)
            
        self.page.update()

    def responder_pregunta(self, atributo, respuesta):
        # Guardar copia del estado en la pila de historial para permitir retroceder
        self.historial_hechos.append(self.hechos.copy())
        self.hechos[atributo] = respuesta
        self.procesar_paso_diagnostico()

    def retroceder_pregunta(self):
        if self.historial_hechos:
            self.hechos = self.historial_hechos.pop()
            self.procesar_paso_diagnostico()

    def mostrar_resultado_exito(self, especie, camino):
        self.limpiar_pantalla()
        
        # Tarjeta de cabecera de éxito con degradado turquesa
        resultado_header = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon=ft.icons.CHECK_CIRCLE_ROUNDED, size=60, color=self.color_accent),
                    ft.Text("ORGANISMO IDENTIFICADO", size=24, weight=ft.FontWeight.BOLD, color=self.color_text),
                    ft.Text(f"{especie['nombre_comun']}", size=22, color=self.color_accent, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Nombre científico: {especie['nombre_cientifico']}", size=16, color=self.color_subtext, italic=True),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            border_radius=15,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#1E293B", self.color_card]
            ),
            alignment=ft.alignment.center
        )
        
        # Detalles de la especie
        detalles_col = ft.Column(
            [
                ft.Text("Información Taxonómica y Ecológica", size=18, weight=ft.FontWeight.BOLD, color=self.color_text),
                ft.Divider(color="#334155"),
                ft.Row([ft.Text("Grupo:", weight=ft.FontWeight.BOLD, color=self.color_accent), ft.Text(especie['grupo'], color=self.color_text)]),
                ft.Row([ft.Text("Hábitat en Los Roques:", weight=ft.FontWeight.BOLD, color=self.color_accent), ft.Text(especie['habitat'], color=self.color_text)]),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Descripción:", weight=ft.FontWeight.BOLD, color=self.color_accent),
                ft.Text(especie['descripcion'], color=self.color_text),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Características morfológicas confirmadas:", weight=ft.FontWeight.BOLD, color=self.color_accent),
            ],
            spacing=8
        )
        
        # Lista de chips de características
        chips_row = ft.Row(wrap=True, spacing=10)
        for k, v in especie['caracteristicas'].items():
            chips_row.controls.append(
                ft.Chip(
                    label=ft.Text(f"{k.capitalize()}: {v}", color=self.color_bg),
                    bgcolor=self.color_accent,
                    disabled=True
                )
            )
        detalles_col.controls.append(chips_row)
        
        # Contenedor de detalles
        detalles_card = ft.Container(
            content=detalles_col,
            padding=20,
            bgcolor=self.color_card,
            border_radius=12,
            border=ft.border.all(1, "#334155")
        )
        
        # Explicación del razonamiento
        explicacion_pasos = ft.Column(spacing=5)
        for idx, (p, r) in enumerate(camino, 1):
            explicacion_pasos.controls.append(
                ft.Text(f" Paso {idx}: {p} ➔ {r}", size=13, color=self.color_subtext)
            )
            
        explicacion_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Lógica del Razonamiento Taxonómico", size=14, weight=ft.FontWeight.BOLD, color=self.color_text),
                    ft.Divider(color="#334155", height=10),
                    explicacion_pasos
                ]
            ),
            padding=15,
            bgcolor="#0F172A",
            border_radius=10,
            border=ft.border.all(1, "#1E293B")
        )
        
        # Botones de pie
        btn_reiniciar = ft.ElevatedButton(
            "Nuevo Diagnóstico",
            icon=ft.icons.REPLAY_ROUNDED,
            style=ft.ButtonStyle(bgcolor={"": self.color_accent}, color={"": self.color_bg}),
            on_click=lambda _: self.iniciar_diagnostico()
        )
        
        btn_salir = ft.OutlinedButton(
            "Volver al Menú",
            icon=ft.icons.HOME_ROUNDED,
            style=ft.ButtonStyle(color={"": self.color_accent}, side={"": ft.BorderSide(1.5, self.color_accent)}),
            on_click=lambda _: self.mostrar_bienvenida()
        )
        
        botones = ft.Row([btn_reiniciar, btn_salir], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        
        # Ensamblar layout final
        self.main_container.content = ft.Container(
            content=ft.Column(
                [
                    resultado_header,
                    ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                    detalles_card,
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    explicacion_card,
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    botones
                ],
                spacing=10,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            width=850,
            alignment=ft.alignment.center
        )
        self.page.update()

    def mostrar_resultado_fallo(self, mensaje, camino):
        self.limpiar_pantalla()
        
        resultado_header = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon=ft.icons.WARNING_AMBER_ROUNDED, size=60, color="orange"),
                    ft.Text("DIAGNÓSTICO INCOMPLETO", size=24, weight=ft.FontWeight.BOLD, color=self.color_text),
                    ft.Text("No se pudo clasificar el espécimen con las reglas actuales.", size=14, color=self.color_subtext),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            border_radius=15,
            bgcolor=self.color_card,
            border=ft.border.all(1, "orange")
        )
        
        motivo_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Motivo del Fallo", size=16, weight=ft.FontWeight.BOLD, color=self.color_text),
                    ft.Divider(color="#334155"),
                    ft.Text(mensaje, color="orange", weight=ft.FontWeight.BOLD),
                ]
            ),
            padding=20,
            bgcolor="#1E293B",
            border_radius=10
        )
        
        # Explicación de los pasos tomados
        explicacion_pasos = ft.Column(spacing=5)
        for idx, (p, r) in enumerate(camino, 1):
            explicacion_pasos.controls.append(
                ft.Text(f" Paso {idx}: {p} ➔ {r}", size=13, color=self.color_subtext)
            )
            
        explicacion_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Pasos de clasificación recorridos:", size=14, weight=ft.FontWeight.BOLD, color=self.color_text),
                    ft.Divider(color="#334155", height=10),
                    explicacion_pasos if camino else ft.Text("No se completó ningún paso.", color=self.color_subtext)
                ]
            ),
            padding=15,
            bgcolor="#0F172A",
            border_radius=10,
            border=ft.border.all(1, "#1E293B")
        )
        
        btn_reiniciar = ft.ElevatedButton(
            "Reintentar Diagnóstico",
            icon=ft.icons.REPLAY_ROUNDED,
            style=ft.ButtonStyle(bgcolor={"": self.color_accent}, color={"": self.color_bg}),
            on_click=lambda _: self.iniciar_diagnostico()
        )
        
        btn_salir = ft.OutlinedButton(
            "Volver al Menú",
            icon=ft.icons.HOME_ROUNDED,
            style=ft.ButtonStyle(color={"": self.color_accent}, side={"": ft.BorderSide(1.5, self.color_accent)}),
            on_click=lambda _: self.mostrar_bienvenida()
        )
        
        botones = ft.Row([btn_reiniciar, btn_salir], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        
        self.main_container.content = ft.Container(
            content=ft.Column(
                [
                    resultado_header,
                    ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                    motivo_card,
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    explicacion_card,
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    botones
                ],
                spacing=10,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            width=850,
            alignment=ft.alignment.center
        )
        self.page.update()

    def mostrar_catalogo(self):
        self.limpiar_pantalla()
        
        # Grid para las tarjetas de especies
        especies_grid = ft.ResponsiveRow(spacing=20)
        
        def renderizar_catalogo(filtro=""):
            especies_grid.controls.clear()
            for especie in self.bc.listar_especies():
                if filtro.lower() not in especie['nombre_comun'].lower() and filtro.lower() not in especie['nombre_cientifico'].lower():
                    continue
                
                # Mapear íconos según el grupo
                grupo_icono = ft.icons.BUG_REPORT
                grupo = especie['grupo'].lower()
                if "molusco" in grupo or "concha" in grupo:
                    grupo_icono = ft.icons.LEMON # Representativo
                elif "pez" in grupo:
                    grupo_icono = ft.icons.WATER
                elif "coral" in grupo:
                    grupo_icono = ft.icons.TIRE_REPAIR_ROUNDED
                elif "reptil" in grupo or "tortuga" in grupo:
                    grupo_icono = ft.icons.PETS
                elif "planta" in grupo or "hierba" in grupo:
                    grupo_icono = ft.icons.SPA
                
                # Tarjeta de Especie
                card = ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(icon=grupo_icono, color=self.color_accent, size=24),
                                    ft.Text(especie['grupo'].upper(), size=11, color=self.color_accent, weight=ft.FontWeight.BOLD),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Text(especie['nombre_comun'], size=18, weight=ft.FontWeight.BOLD, color=self.color_text),
                            ft.Text(especie['nombre_cientifico'], size=14, color=self.color_subtext, italic=True),
                            ft.Divider(color="#334155", height=10),
                                ft.Text(f"Hábitat: {especie['habitat']}", size=12, color=self.color_subtext, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                            ft.Text(especie['descripcion'], size=13, color=self.color_text, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS),
                        ],
                        spacing=8
                    ),
                    padding=20,
                    bgcolor=self.color_card,
                    border_radius=12,
                    border=ft.border.all(1, "#334155"),
                    # Definición de tamaño para ResponsiveRow
                    col={"sm": 12, "md": 6, "lg": 4}
                )
                especies_grid.controls.append(card)
            self.page.update()

        # Input de búsqueda
        search_field = ft.TextField(
            hint_text="Buscar por nombre común o científico...",
            prefix_icon=ft.icons.SEARCH_ROUNDED,
            bgcolor="#0F172A",
            border_color="#334155",
            border_radius=8,
            color=self.color_text,
            on_change=lambda e: renderizar_catalogo(e.control.value)
        )
        
        btn_volver = ft.OutlinedButton(
            "Volver al Menú",
            icon=ft.icons.ARROW_BACK_ROUNDED,
            style=ft.ButtonStyle(color={"": self.color_accent}, side={"": ft.BorderSide(1.5, self.color_accent)}),
            on_click=lambda _: self.mostrar_bienvenida()
        )
        
        # Renderizar catálogo inicial
        renderizar_catalogo()
        
        layout = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Catálogo de Especies de Los Roques", size=22, weight=ft.FontWeight.BOLD, color=self.color_text),
                        btn_volver
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(color="#334155"),
                search_field,
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                especies_grid
            ],
            spacing=15,
            scroll=ft.ScrollMode.ADAPTIVE
        )
        
        self.main_container.content = ft.Container(
            content=layout,
            padding=10
        )
        self.page.update()
