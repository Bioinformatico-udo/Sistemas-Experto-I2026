import customtkinter as ctk
from ..styles import *

HOVER_CARD = "#2A3B55"

class ComoUsarPage:
    def __init__(self, parent_frame, main_app):
        self.parent_frame = parent_frame
        self.main_app = main_app
        self.frame = ctk.CTkFrame(self.parent_frame, fg_color=COLOR_BACKGROUND_MAIN, corner_radius=15)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 5))
        ctk.CTkLabel(header, text="Como usar",
                     font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
                     text_color=COLOR_PRIMARY_LIGHT).pack(anchor="w")
        ctk.CTkLabel(header, text="Sigue estos pasos para identificar un crustaceo anomuro de la familia porcellanidae y aprovechar el resto de sus funciones:",
                     font=ctk.CTkFont(size=14), text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(5, 0))

        steps = [
            ("1", "Acceda al Identificador",
             "Haga clic en 'COMENZAR IDENTIFICACIÓN DE ESPECIE' desde la pantalla de inicio."),
            ("2", "Responda las preguntas",
             "Seleccione las características morfológicas observadas en el espécimen. Lea el glosario si desconoce algún término."),
            ("3", "Analice el resultado",
             "El sistema mostrará la especie identificada, con imagen, ficha técnica y un nivel de certeza."),
            ("4", "Verifique una especie (opcional)",
             "Use el botón 'INICIAR VERIFICACIÓN DE ESPECIE' ubicado en la pantalla de inicio, para comprobar cuántas características coinciden con una especie concreta."),
            ("5", "Agregue nuevas especies (opcional)",
             "Acceda al panel de 'ADMINISTRADOR' e inicie sesión para registrar nuevas especies en el sistema. Esta función es de uso exclusivo para administradores."),            
            ("6", "Consulte el glosario",
             "Ante cualquier duda técnica, visite la sección 'Glosario de Términos'.")
        ]

        container = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=10)

        for num, tit, descr in steps:
            self._crear_paso(container, num, tit, descr)

    def _crear_paso(self, parent, numero, titulo, descripcion):
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD_BACKGROUND, corner_radius=12)
        card.pack(fill="x", pady=6, padx=5)

        # Círculo numérico
        circulo = ctk.CTkFrame(card, width=45, height=45, fg_color=COLOR_PRIMARY_LIGHT, corner_radius=22)
        circulo.pack(side="left", padx=15, pady=12)
        circulo.pack_propagate(False)
        ctk.CTkLabel(circulo, text=numero, font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLOR_TEXT_PRIMARY).pack(expand=True)

        cont = ctk.CTkFrame(card, fg_color="transparent")
        cont.pack(side="left", fill="both", expand=True, padx=10, pady=12)

        ctk.CTkLabel(cont, text=titulo, font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=COLOR_PRIMARY_LIGHT).pack(anchor="w")
        ctk.CTkLabel(cont, text=descripcion, font=ctk.CTkFont(size=13),
                     text_color=COLOR_TEXT_SECONDARY, wraplength=700, justify="left").pack(anchor="w", pady=(5, 0))

        # Hover
        def on_enter(e):
            card.configure(fg_color=HOVER_CARD)
        def on_leave(e):
            card.configure(fg_color=COLOR_CARD_BACKGROUND)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        circulo.bind("<Enter>", on_enter)
        circulo.bind("<Leave>", on_leave)
        cont.bind("<Enter>", on_enter)
        cont.bind("<Leave>", on_leave)

    def get_frame(self):
        return self.frame